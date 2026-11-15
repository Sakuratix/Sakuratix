#!/usr/bin/env python3
"""Draws the project preview cards (assets/card-*.svg). Re-run after changing text."""
import html
from pathlib import Path

W, H = 800, 480
MINT, BG, FG, DIM, RED, AMBER, BLUE = "#8ef0c6", "#0d1117", "#e6edf3", "#8b949e", "#ff7b72", "#e3b341", "#79c0ff"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "Inter,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
OUT = Path(__file__).resolve().parent.parent / "assets"


def frame(title_bar: str, body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{MINT}" stroke-opacity=".06"/></pattern>
  <radialGradient id="glow" cx="80%" cy="0%" r="70%"><stop offset="0" stop-color="{MINT}" stop-opacity=".16"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="{H}" fill="url(#g)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>
<rect width="{W}" height="34" fill="#161b22"/>
<circle cx="20" cy="17" r="6" fill="#ff5f57"/><circle cx="40" cy="17" r="6" fill="#febc2e"/><circle cx="60" cy="17" r="6" fill="#28c840"/>
<text x="{W/2}" y="22" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{DIM}">{html.escape(title_bar)}</text>
{body}
</svg>
"""


def t(x, y, s, size=16, fill=FG, family=MONO, weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve">{s}</text>'


def esc(s):
    return html.escape(s)


def headline(lines, y=96):
    return "".join(t(40, y + i * 46, esc(l), 40, FG, SANS, 800) for i, l in enumerate(lines))


def kubectl_why():
    rows = [
        (MINT, "$ kubectl why deploy/api -n shop"),
        (RED, "✗ Rollout is stuck (progressDeadlineSeconds exceeded)"),
        (MINT, "  → kubectl rollout undo deployment/api"),
        (DIM, "pod/api-7f9c6-x2kq9  CrashLoopBackOff · restarts 7"),
        (RED, "✗ [app] OOMKilled: went over its memory limit (256Mi)"),
        (DIM, "  · last exit: OOMKilled, exit code 137, 2m ago"),
        (DIM, "pod/api-7f9c6-pp4mz  ImagePullBackOff"),
        (RED, "✗ [app] Image or tag doesn't exist: api:1.9.0"),
    ]
    body = headline(["Why is my pod broken?"], 92)
    body += t(40, 128, esc("kubectl describe shows everything. This explains it."), 17, DIM, SANS)
    body += f'<rect x="40" y="152" width="720" height="290" rx="10" fill="#010409" stroke="#30363d"/>'
    body += "".join(t(62, 188 + i * 32, esc(s), 16, c) for i, (c, s) in enumerate(rows))
    return frame("zsh · prod-cluster", body)


def platform_ci():
    stages = [("hadolint", "lint"), ("buildx", "build"), ("trivy", "scan"), ("sbom", "spdx"), ("cosign", "sign")]
    body = headline(["Shared CI for every repo:", "build, scan, sign."], 86)
    y, x0, gap = 300, 78, 160
    body += f'<line x1="{x0}" y1="{y}" x2="{x0 + gap * 4}" y2="{y}" stroke="#30363d" stroke-width="4"/>'
    for i, (name, sub) in enumerate(stages):
        x = x0 + gap * i
        last = i == len(stages) - 1
        body += f'<circle cx="{x}" cy="{y}" r="30" fill="{"#0f2a21" if not last else MINT}" stroke="{MINT}" stroke-width="2.5"/>'
        body += f'<path d="M{x-11} {y} l7 8 l15 -16" fill="none" stroke="{BG if last else MINT}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        body += t(x, y + 62, name, 17, FG, MONO, 600, "middle") + t(x, y + 86, sub, 14, DIM, MONO, 400, "middle")
    body += t(40, 448, esc("uses: Sakuratix/platform-ci/.github/workflows/docker.yml@v1"), 15, BLUE)
    return frame("github actions · infra-lab", body)


def infra_lab():
    boxes = [("git push", MINT), ("CI", MINT), ("GHCR", BLUE), ("Helm → k8s", BLUE), ("Prometheus", AMBER), ("Telegram", AMBER)]
    body = headline(["From commit to prod", "in one repository."], 86)
    x, y, w, h, gap = 40, 236, 108, 54, 15
    for i, (name, c) in enumerate(boxes):
        bx = x + i * (w + gap)
        body += f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="8" fill="#161b22" stroke="{c}" stroke-opacity=".8"/>'
        body += t(bx + w / 2, y + 33, esc(name), 14, FG, MONO, 600, "middle")
        if i < len(boxes) - 1:
            body += f'<path d="M{bx + w + 2} {y + h/2} h{gap - 4}" stroke="{DIM}" stroke-width="2"/>'
    stats = [("SLO", "99.5%"), ("burn-rate alerts", "fast + slow"), ("alert tests", "promtool"), ("network", "default deny")]
    for i, (k, v) in enumerate(stats):
        sx = 40 + i * 182
        body += t(sx, 352, esc(k), 14, DIM) + t(sx, 384, esc(v), 22, FG, SANS, 700)
    body += t(40, 446, "Terraform · Ansible · Helm · Prometheus · Grafana · Docker", 15, DIM)
    return frame("infra-lab", body)


def k3s_gitops():
    apps = [("projects", "-1"), ("ingress-nginx", "0"), ("cert-manager", "0"), ("kube-prometheus-stack", "1"),
            ("alertmanager-telegram-relay", "2"), ("argocd-monitoring", "2"), ("infra-lab", "2")]
    body = headline(["The cluster is", "whatever git says."], 86)
    body += t(40, 210, "root", 18, MINT, MONO, 700)
    for i, (name, wave) in enumerate(apps):
        y = 244 + i * 30
        body += t(52, y, "├─" if i < len(apps) - 1 else "└─", 16, DIM)
        body += t(86, y, esc(name), 16, FG) + t(420, y, f"wave {wave}", 14, DIM)
        body += t(540, y, "Synced", 14, MINT) + t(620, y, "Healthy", 14, MINT)
    return frame("argocd app tree", body)


for name, fn in [("kubectl-why", kubectl_why), ("platform-ci", platform_ci), ("infra-lab", infra_lab), ("k3s-gitops", k3s_gitops)]:
    (OUT / f"card-{name}.svg").write_text(fn())
print("cards written")


def stack():
    rows = [
        ("containers", ["Kubernetes", "Docker", "Helm", "Argo CD", "k3s", "ingress-nginx", "cert-manager"]),
        ("delivery", ["GitLab CI", "GitHub Actions", "Trivy", "cosign", "SBOM", "Vault"]),
        ("iac", ["Terraform", "Ansible", "Yandex Cloud", "tflint", "kubeconform"]),
        ("observability", ["Prometheus", "Alertmanager", "Grafana", "Loki", "Zabbix"]),
        ("systems", ["Linux", "systemd", "Nginx", "MikroTik", "WireGuard", "TrueNAS / ZFS"]),
        ("data", ["PostgreSQL", "Redis", "Kafka", "S3"]),
        ("code", ["Bash", "Python", "Go"]),
    ]
    w, rh, top = 900, 46, 34
    h = top * 2 + rh * len(rows) - 12
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
           f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{MINT}" stroke-opacity=".06"/></pattern></defs>',
           f'<rect width="{w}" height="{h}" rx="10" fill="{BG}"/><rect width="{w}" height="{h}" rx="10" fill="url(#g)"/>',
           f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="10" fill="none" stroke="{MINT}" stroke-opacity=".25"/>']
    for i, (cat, items) in enumerate(rows):
        y = top + i * rh
        out.append(t(28, y + 21, cat, 14, MINT))
        x = 170
        for it in items:
            bw = 18 + len(it) * 8.6
            out.append(f'<rect x="{x}" y="{y}" width="{bw:.0f}" height="30" rx="5" fill="#161b22" stroke="#30363d"/>')
            out.append(t(x + bw / 2, y + 20, esc(it), 14, FG, MONO, 400, "middle"))
            x += bw + 10
    out.append("</svg>")
    (OUT / "stack.svg").write_text("\n".join(out) + "\n")


stack()


def typing():
    """Role line that types itself, one phrase at a time (pure CSS, works in <img>)."""
    lines = [
        "Kubernetes · CKA · Helm · Argo CD",
        "Infrastructure as code: Terraform, Ansible",
        "CI/CD with scanning, SBOMs and signed images",
        "SLOs, burn-rate alerts, tested alert rules",
        "Backups that are restored every week",
    ]
    w, h, slot = 900, 44, 4.0
    total = slot * len(lines)
    css = [f".l{{opacity:0;animation:show {total}s infinite}}",
           f".c{{animation:type {total}s steps(1) infinite}}"]
    # each line: visible during its slot; a mask rect grows to type it out
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">', "<style>"]
    for i, l in enumerate(lines):
        a, b = i * slot / total * 100, (i + 1) * slot / total * 100
        tw = len(l) * 11.1 + 6
        type_end = a + 1.6 / total * 100
        out.append(f"@keyframes s{i}{{0%,{a:.3f}%{{opacity:0}}{a + .01:.3f}%,{b - .01:.3f}%{{opacity:1}}{b:.3f}%,100%{{opacity:0}}}}")
        out.append(f"@keyframes m{i}{{0%,{a:.3f}%{{width:0}}{type_end:.3f}%,100%{{width:{tw:.0f}px}}}}")
        out.append(f"@keyframes k{i}{{0%,{a:.3f}%{{transform:translateX(0)}}{type_end:.3f}%,100%{{transform:translateX({tw:.0f}px)}}}}")
        out.append(f"#l{i}{{opacity:0;animation:s{i} {total}s linear infinite}}#m{i}{{animation:m{i} {total}s steps({len(l)}) infinite}}#k{i}{{animation:k{i} {total}s steps({len(l)}) infinite}}")
    out.append(".blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}")
    out.append("</style>")
    for i, l in enumerate(lines):
        tw = len(l) * 11.1 + 6
        x0 = (w - tw) / 2
        out.append(f'<g id="l{i}"><clipPath id="cp{i}"><rect id="m{i}" x="{x0:.0f}" y="0" width="0" height="{h}"/></clipPath>')
        out.append(f'<text x="{x0:.0f}" y="29" clip-path="url(#cp{i})" font-family="{MONO}" font-size="18.5" fill="{FG}" xml:space="preserve">{esc(l)}</text>')
        out.append(f'<g id="k{i}"><rect class="blink" x="{x0 + 2:.0f}" y="12" width="10" height="22" fill="{MINT}"/></g></g>')
    out.append("</svg>")
    (OUT / "typing.svg").write_text("\n".join(out) + "\n")


def system_map():
    """How the projects fit together, as one platform."""
    W, H = 900, 470
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         f'<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{MINT}" stroke-opacity=".06"/></pattern>'
         f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{DIM}"/></marker></defs>',
         f'<rect width="{W}" height="{H}" rx="10" fill="{BG}"/><rect width="{W}" height="{H}" rx="10" fill="url(#g)"/>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{MINT}" stroke-opacity=".25"/>',
         "<style>.flow{stroke-dasharray:6 6;animation:f 1.2s linear infinite}@keyframes f{to{stroke-dashoffset:-12}}</style>"]

    def box(x, y, w, h, title, sub, color=MINT):
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#161b22" stroke="{color}" stroke-opacity=".75"/>')
        o.append(t(x + w / 2, y + 24, esc(title), 15, FG, MONO, 700, "middle"))
        o.append(t(x + w / 2, y + 44, esc(sub), 12, DIM, MONO, 400, "middle"))

    def arrow(d, label=None, lx=0, ly=0):
        o.append(f'<path class="flow" d="{d}" fill="none" stroke="{DIM}" stroke-width="1.6" marker-end="url(#a)"/>')
        if label:
            o.append(t(lx, ly, esc(label), 11, DIM, MONO, 400, "middle"))

    o.append(t(30, 38, "how the pieces fit", 14, MINT))
    box(30, 70, 170, 58, "git push", "any repo")
    box(260, 70, 190, 58, "platform-ci", "lint · scan · SBOM · sign")
    box(520, 70, 160, 58, "GHCR", "signed images")
    box(720, 70, 150, 58, "k3s-gitops", "Argo CD syncs git")
    arrow("M200 99 H254", "uses: @v1", 228, 62)
    arrow("M450 99 H514")
    arrow("M680 99 H714")
    box(640, 200, 230, 58, "infra-lab", "app · Helm · SLOs", BLUE)
    box(360, 200, 230, 58, "kube-prometheus-stack", "metrics · rules", AMBER)
    box(80, 200, 230, 58, "telegram-relay", "alerts to the team", AMBER)
    arrow("M795 128 V194")
    arrow("M640 229 H596", "scrape", 618, 220)
    arrow("M360 229 H316", "alert", 338, 220)
    box(80, 330, 230, 58, "kubectl-why", "explains what broke", MINT)
    box(360, 330, 230, 58, "pg-backup-s3", "age · weekly restore test", BLUE)
    box(640, 330, 230, 58, "mikrotik-config-backup", "network configs to git", BLUE)
    arrow("M195 258 V324", "then: kubectl why", 262, 298)
    arrow("M475 330 V264", "metrics + rules", 540, 300)
    o.append(t(30, 440, "How the repositories on this profile work together.", 13, DIM, SANS))
    o.append("</svg>")
    (OUT / "system-map.svg").write_text("\n".join(o) + "\n")


typing()
system_map()
