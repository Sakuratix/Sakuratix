#!/usr/bin/env python3
"""'Break my cluster': a visitor opens an issue titled 'break: <failure>',
kubectl-why diagnoses that failure, the bot answers in the issue and the
README shows who broke what last.

Run by .github/workflows/break.yml. Inputs come from the issue, so they are
read from the environment and checked against an allowlist, never passed to a shell.

  ISSUE_TITLE=... ISSUE_AUTHOR=... python3 scripts/break_cluster.py --kubectl-why kw/kubectl-why --repo kw --comment out.md
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from update import README, ROOT, replace_block, run_case, worst_finding  # noqa: E402

STATE = ROOT / "data" / "breaks.json"

# what visitors can pick -> kubectl-why fixture directory, label shown in the README
MENU = {
    "oomkilled": ("oomkilled", "OOMKilled"),
    "crashloop": ("crashloop", "CrashLoopBackOff"),
    "liveness": ("liveness", "Liveness probe kill"),
    "readiness": ("readiness", "Readiness failing"),
    "bad-image": ("image-notfound", "ImagePullBackOff"),
    "private-registry": ("image-unauthorized", "Private registry"),
    "missing-secret": ("missing-secret", "Missing Secret"),
    "pending": ("pending", "Pending forever"),
    "volume": ("failed-mount", "Volume won't mount"),
    "stuck-terminating": ("terminating", "Stuck Terminating"),
    "evicted": ("evicted", "Evicted"),
    "init": ("init-failing", "Init container fails"),
    "rollout": ("deployment", "Stuck rollout"),
}
LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$")


def parse(title: str) -> str | None:
    m = re.match(r"^\s*break:\s*([a-z-]+)\s*$", title or "", re.I)
    if not m:
        return None
    key = m.group(1).lower()
    return key if key in MENU else None


def menu_markdown() -> str:
    repo = "https://github.com/Sakuratix/Sakuratix/issues/new"
    body = "Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."
    badges = []
    for key, (_, label) in MENU.items():
        badge = urllib.parse.quote(label.replace("-", "--").replace(" ", "_"), safe="")
        badges.append(f'<a href="{repo}?title=break:+{key}&body={body}">'
                      f'<img src="https://img.shields.io/badge/%F0%9F%92%A5-{badge}-ff7b72?style=flat-square&labelColor=161b22" alt="{label}"></a>')
    return "\n".join(badges)


def state_markdown(state: dict) -> str:
    lines = [f"**Broken {state['total']} time{'s' if state['total'] != 1 else ''} so far.**"]
    if state["recent"]:
        lines += ["", "| when | who | what they broke | kubectl-why said |", "|---|---|---|---|"]
        for r in state["recent"]:
            lines.append(f"| {r['at']} | @{r['user']} | {MENU[r['key']][1]} | {r['title']} |")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kubectl-why", type=Path, required=True)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--comment", type=Path, required=True, help="where to write the issue reply (markdown)")
    ap.add_argument("--render-menu", action="store_true", help="only refresh the README menu and table")
    a = ap.parse_args()

    state = json.loads(STATE.read_text()) if STATE.exists() else {"total": 0, "recent": []}
    text = README.read_text()
    if a.render_menu:
        README.write_text(replace_block(replace_block(text, "break-menu", menu_markdown()), "break-log", state_markdown(state)))
        return

    key, user = parse(os.environ.get("ISSUE_TITLE", "")), os.environ.get("ISSUE_AUTHOR", "")
    if not LOGIN.match(user):
        sys.exit("bad author login")
    if key is None:
        options = ", ".join(f"`break: {k}`" for k in MENU)
        a.comment.write_text(f"Unknown failure. Title the issue as one of: {options}.\n")
        print("unknown")
        return

    now = dt.datetime.now(dt.timezone.utc)
    target, plain, report = run_case(a.kubectl_why.resolve(), a.repo.resolve() / "testdata" / MENU[key][0], now, color=False)
    worst = worst_finding(report)
    a.comment.write_text("\n".join([
        f"💥 @{user} broke `{' '.join(target)}`. Here is what `kubectl why` makes of it:",
        "",
        "```text",
        f"$ kubectl why {' '.join(target)}",
        plain.rstrip(),
        "```",
        "",
        f"**Verdict:** {worst['title']}",
        "",
        "Replayed from a recorded cluster state with the real [kubectl-why](https://github.com/Sakuratix/kubectl-why) binary. "
        "This issue closes itself; [break something else](https://github.com/Sakuratix) in the profile README.",
    ]) + "\n")

    state["total"] += 1
    state["recent"] = ([{"at": now.strftime("%Y-%m-%d %H:%M UTC"), "user": user, "key": key, "title": worst["title"]}]
                       + state["recent"])[:5]
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    README.write_text(replace_block(text, "break-log", state_markdown(state)))
    print(f"{user} broke {key}: {worst['title']}")


if __name__ == "__main__":
    main()
