#!/usr/bin/env python3
"""Daily refresh of the profile README (run by .github/workflows/update.yml).

* stats line: account age and contributions in the last 7 days (GitHub GraphQL);
* "Incident of the day": one recorded failure from kubectl-why's test fixtures,
  shifted to today's clock, diagnosed by the real kubectl-why binary and drawn as SVG.

  python3 scripts/update.py --kubectl-why kw/kubectl-why --repo kw
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
USER = "Sakuratix"
FIXTURE_NOW = dt.datetime(2026, 11, 14, 10, 0, tzinfo=dt.timezone.utc)  # "now" the fixtures were recorded at
ISO = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")

FAKE_KUBECTL = """#!/bin/sh
case "$2" in
  pod) cat "$FIXTURE/pod.json";; pods) cat "$FIXTURE/pods.json";;
  deployment) cat "$FIXTURE/deployment.json";; events) cat "$FIXTURE/events.json";;
  *) echo "unsupported: $*" >&2; exit 1;;
esac
"""


def replace_block(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"(<!-- {name}:start -->)(.*?)(<!-- {name}:end -->)", re.S)
    if not pat.search(text):
        sys.exit(f"README has no {name} markers")
    return pat.sub(lambda m: f"{m.group(1)}\n{body}\n{m.group(3)}", text)


def stats(now: dt.datetime) -> str | None:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None
    since = (now - dt.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    query = {"query": f'{{ user(login: "{USER}") {{ createdAt contributionsCollection(from: "{since}") '
                      f"{{ contributionCalendar {{ totalContributions }} }} }} }}"}
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps(query).encode(),
                                 {"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        u = json.load(r)["data"]["user"]
    years = (now - dt.datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))).days // 365
    joined = "this year" if years < 1 else f"{years} year{'s' if years > 1 else ''} ago"
    n = u["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    return f'<p align="center"><sub>Joined GitHub {joined} · {n} contributions in the last 7 days</sub></p>'


def api(path: str, token: str):
    req = urllib.request.Request("https://api.github.com" + path, headers={
        "Authorization": f"bearer {token}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def metrics(now: dt.datetime) -> dict | None:
    """Numbers for the 'at a glance' panel, all read live from GitHub."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return None
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&type=owner", token)
             if not r["fork"] and not r["private"] and r["name"].lower() != USER.lower()]
    releases = sum(len(api(f"/repos/{r['full_name']}/releases?per_page=100", token)) for r in repos)
    with_ci = green = 0
    for r in repos:
        runs = api(f"/repos/{r['full_name']}/actions/runs?branch={r['default_branch']}&status=completed&per_page=1", token)
        if runs.get("workflow_runs"):
            with_ci += 1
            green += runs["workflow_runs"][0]["conclusion"] == "success"
    since = (now - dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = {"query": f'{{ user(login: "{USER}") {{ contributionsCollection(from: "{since}") '
                  f"{{ contributionCalendar {{ totalContributions }} }} }} }}"}
    req = urllib.request.Request("https://api.github.com/graphql", json.dumps(q).encode(),
                                 {"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        contrib = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    return {"repos": len(repos), "releases": releases, "green": green, "with_ci": with_ci, "contrib": contrib}


def render_metrics(m: dict, now: dt.datetime) -> None:
    tiles = [
        (str(m["repos"]), "public repositories"),
        (str(m["contrib"]), "contributions, 1 year"),
        (str(m["releases"]), "releases shipped"),
        (f'{m["green"]}/{m["with_ci"]}', "CI green right now"),
        ("3", "certifications"),
    ]
    w, h, tw = 900, 120, 168
    mono = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    sans = "Inter,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
         '<style>.n{opacity:0;animation:up .8s cubic-bezier(.2,.8,.2,1) forwards}@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>']
    for i, (num, label) in enumerate(tiles):
        x = 6 + i * (tw + 9)
        green = label.startswith("CI") and m["green"] == m["with_ci"]
        o.append(f'<rect x="{x}" y="6" width="{tw}" height="{h-12}" rx="10" fill="#0d1117" stroke="#8ef0c6" stroke-opacity=".25"/>')
        o.append(f'<g class="n" style="animation-delay:{i * .12:.2f}s"><text x="{x + tw/2}" y="62" text-anchor="middle" font-family="{sans}" font-size="34" font-weight="800" fill="{"#8ef0c6" if green or i != 3 else "#e3b341"}">{num}</text></g>')
        o.append(f'<text x="{x + tw/2}" y="90" text-anchor="middle" font-family="{mono}" font-size="12" fill="#8b949e">{label}</text>')
    o.append("</svg>")
    (ROOT / "assets" / "metrics.svg").write_text("\n".join(o) + "\n")


def shift(obj, delta):
    if isinstance(obj, dict):
        return {k: shift(v, delta) for k, v in obj.items()}
    if isinstance(obj, list):
        return [shift(v, delta) for v in obj]
    if isinstance(obj, str) and ISO.match(obj):
        t = dt.datetime.strptime(obj, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc) + delta
        return t.strftime("%Y-%m-%dT%H:%M:%SZ")
    return obj


def run_case(binary: Path, case: Path, now: dt.datetime, color: bool = True):
    """Replay one recorded fixture with today's clock through kubectl-why.
    Returns (target args, output text, parsed JSON report)."""
    delta = now.replace(second=0, microsecond=0) - FIXTURE_NOW
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        fix = tmp / "fixture"
        fix.mkdir()
        for f in case.glob("*.json"):
            (fix / f.name).write_text(json.dumps(shift(json.loads(f.read_text()), delta)))
        (tmp / "bin").mkdir()
        fake = tmp / "bin" / "kubectl"
        fake.write_text(FAKE_KUBECTL)
        fake.chmod(0o755)

        if (fix / "deployment.json").exists():
            d = json.loads((fix / "deployment.json").read_text())["metadata"]
            target = [f"deploy/{d['name']}", "-n", d["namespace"]]
        else:
            p = json.loads((fix / "pod.json").read_text())["metadata"]
            target = [f"pod/{p['name']}", "-n", p["namespace"]]
        env = {**os.environ, "PATH": f"{tmp / 'bin'}:{os.environ['PATH']}", "FIXTURE": str(fix)}
        env.pop("CLICOLOR_FORCE", None)
        if color:
            env["CLICOLOR_FORCE"] = "1"
        out = subprocess.run([str(binary), *target], env=env, capture_output=True, text=True).stdout
        env.pop("CLICOLOR_FORCE", None)
        report = json.loads(subprocess.run([str(binary), *target, "-o", "json"], env=env,
                                           capture_output=True, text=True).stdout)[0]
    return target, out, report


def worst_finding(report: dict) -> dict:
    findings = report["findings"] + [f for c in report.get("pods", []) for f in c["findings"]]
    return next((f for f in findings if f["severity"] in ("critical", "warning")), findings[0])


def cases(repo: Path) -> list[Path]:
    return sorted(p for p in (repo / "testdata").iterdir() if (p / "pod.json").exists() or (p / "deployment.json").exists())


def incident(binary: Path, repo: Path, now: dt.datetime) -> str:
    all_cases = cases(repo)
    case = all_cases[now.timetuple().tm_yday % len(all_cases)]
    target, colored, report = run_case(binary, case, now)

    svg = subprocess.run([sys.executable, str(repo / "hack" / "ansi2svg.py"), "kubectl why " + " ".join(target)],
                         input=colored, capture_output=True, text=True, check=True).stdout
    (ROOT / "assets" / "incident.svg").write_text(svg)

    worst = worst_finding(report)
    what = worst["title"]
    hint = next(iter(worst.get("hints", [])), "")
    date = f"{now.day} {now:%B %Y}"
    return "\n".join([
        f"**Incident of the day, {date}:** {what}",
        "",
        "Every day this section picks one of the failures that [kubectl-why](https://github.com/Sakuratix/kubectl-why) "
        "recognises, replays the recorded cluster state with today's clock and lets the tool explain it. "
        + (f"Today's fix: {hint}" if hint else ""),
        "",
        f'<img src="assets/incident.svg" alt="kubectl why output: {what}" width="100%">',
    ])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kubectl-why", type=Path, required=True, help="built kubectl-why binary")
    ap.add_argument("--repo", type=Path, required=True, help="kubectl-why checkout (testdata/, hack/)")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    text = README.read_text()
    try:
        s = stats(now)
    except Exception as e:  # keep yesterday's line rather than fail the whole refresh
        print(f"stats skipped: {e}", file=sys.stderr)
        s = None
    if s:
        text = replace_block(text, "stats", s)
    try:
        m = metrics(now)
        if m:
            render_metrics(m, now)
    except Exception as e:
        print(f"metrics skipped: {e}", file=sys.stderr)
    text = replace_block(text, "incident", incident(a.kubectl_why.resolve(), a.repo.resolve(), now))
    README.write_text(text)
    print("README updated")


if __name__ == "__main__":
    main()
