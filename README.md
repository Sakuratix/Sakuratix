<p align="center">
  <img src="assets/signature.svg" alt="sakuratox" width="100%">
</p>

<p align="center">I'm Klim (sakuratox), a DevOps engineer. I build CI/CD, run Kubernetes, write infrastructure as code and set up monitoring, so releases are boring and alerts come before complaints.</p>

<p align="center"><img src="assets/typing.svg" alt="Kubernetes, infrastructure as code, CI/CD with signed images, SLOs, tested backups" width="100%"></p>

<p align="center">
  <a href="https://sakuratox.is-a.dev"><img src="https://img.shields.io/badge/site-sakuratox.is--a.dev-8ef0c6?style=flat-square&labelColor=161b22" alt="site"></a>
  <a href="https://sakuratox.is-a.dev/cv/klimentiy-matveev-devops-en.pdf"><img src="https://img.shields.io/badge/CV-PDF-8ef0c6?style=flat-square&labelColor=161b22" alt="CV"></a>
  <a href="https://www.linkedin.com/in/klimentii-matveev-59ab38426/"><img src="https://img.shields.io/badge/LinkedIn-klimentii--matveev-8ef0c6?style=flat-square&labelColor=161b22" alt="LinkedIn"></a>
  <img src="https://komarev.com/ghpvc/?username=Sakuratix&label=profile%20views&color=8ef0c6&style=flat-square" alt="profile views">
</p>

<p align="center"><sub>CKA · Terraform Associate · MTCNA · English C1</sub></p>
<!-- stats:start -->
<p align="center"><sub>Joined GitHub this year · 16 contributions in the last 7 days</sub></p>
<!-- stats:end -->

<p align="center"><img src="assets/metrics.svg" alt="live numbers from GitHub: public repositories, contributions, releases, CI status, certifications" width="100%"></p>

## Built

<table>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Sakuratix/kubectl-why"><img src="assets/card-kubectl-why.svg" alt="kubectl-why" width="100%"></a>
<br><a href="https://github.com/Sakuratix/kubectl-why"><b>kubectl-why</b></a> <sub>Go · kubectl plugin · 0 dependencies</sub>
<br>Explains in plain words why a pod or deployment is unhealthy, with the evidence and what to try next. Tested on a real kind cluster with pods broken on purpose.
</td>
<td width="50%" valign="top">
<a href="https://github.com/Sakuratix/platform-ci"><img src="assets/card-platform-ci.svg" alt="platform-ci" width="100%"></a>
<br><a href="https://github.com/Sakuratix/platform-ci"><b>platform-ci</b></a> <sub>GitHub Actions · Trivy · cosign</sub>
<br>Reusable workflows: image build, vulnerability scan, SBOM and keyless signing, plus Terraform and Helm checks, from one <code>uses:</code> line.
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://github.com/Sakuratix/infra-lab"><img src="assets/card-infra-lab.svg" alt="infra-lab" width="100%"></a>
<br><a href="https://github.com/Sakuratix/infra-lab"><b>infra-lab</b></a> <sub>Terraform · Helm · Prometheus</sub>
<br>A service's whole path from commit to production in one repo: Terraform, Ansible, Helm chart, SLO burn-rate alerts with unit tests.
</td>
<td width="50%" valign="top">
<a href="https://github.com/Sakuratix/k3s-gitops"><img src="assets/card-k3s-gitops.svg" alt="k3s-gitops" width="100%"></a>
<br><a href="https://github.com/Sakuratix/k3s-gitops"><b>k3s-gitops</b></a> <sub>Argo CD · app of apps</sub>
<br>A k3s cluster where everything after the bootstrap comes from git, with AppProject guardrails and alerts when the cluster drifts.
</td>
</tr>
</table>

<details>
<summary><b>More things I've made</b></summary>
<br>

| | |
|---|---|
| [pg-backup-s3](https://github.com/Sakuratix/pg-backup-s3) | PostgreSQL backups to S3 with age encryption and a weekly automated restore check that reports the real RTO |
| [alertmanager-telegram-relay](https://github.com/Sakuratix/alertmanager-telegram-relay) | Alertmanager → Telegram without dependencies: splits big groups, retries rate limits, exposes its own metrics |
| [mikrotik-config-backup](https://github.com/Sakuratix/mikrotik-config-backup) | RouterOS configs to git in parallel, with a guard that refuses to commit secrets |
| [sakuratix.github.io](https://github.com/Sakuratix/sakuratix.github.io) | [My site](https://sakuratox.is-a.dev): one HTML file, three.js, and an easter egg if you click the cloud three times |

</details>

## How I work

| | principle | where you can see it |
|---|---|---|
| 🧪 | **Alerts are code, so they have tests.** An alert that never fired in a test will not fire at 3 a.m. either. | [infra-lab: promtool tests](https://github.com/Sakuratix/infra-lab/tree/main/monitoring/tests) |
| 📉 | **Page on the error budget, not on noise.** Burn-rate alerts instead of fixed thresholds. | [infra-lab: SLO rules](https://github.com/Sakuratix/infra-lab/blob/main/monitoring/alerts.yml) |
| 💾 | **A backup nobody restored is not a backup.** Restored automatically every week, RTO measured. | [pg-backup-s3: restore-check](https://github.com/Sakuratix/pg-backup-s3/blob/main/restore-check.sh) |
| 🔁 | **Nothing is changed by hand.** The cluster is whatever git says; drift raises an alert. | [k3s-gitops](https://github.com/Sakuratix/k3s-gitops) |
| 🔏 | **The supply chain is part of CI.** Every image scanned, described by an SBOM and signed. | [platform-ci](https://github.com/Sakuratix/platform-ci) |
| 🔐 | **Secrets never reach git.** Guards refuse to commit them; backups are encrypted off-host. | [mikrotik-config-backup](https://github.com/Sakuratix/mikrotik-config-backup) |
| 🩺 | **Tools should explain, not dump.** Make the 3 a.m. diagnosis someone else's 30 seconds. | [kubectl-why](https://github.com/Sakuratix/kubectl-why) |

## The platform

<img src="assets/system-map.svg" alt="git push to platform-ci to GHCR to k3s-gitops; Argo CD deploys infra-lab; Prometheus scrapes it and alerts through the Telegram relay; kubectl-why explains failures; pg-backup-s3 exports metrics" width="100%">

## Break my cluster

Pick a failure. It opens an issue; press **Create** and within a minute a bot replays that failure on a recorded cluster, runs the real [kubectl-why](https://github.com/Sakuratix/kubectl-why) on it and answers you in the issue.

<p>
<!-- break-menu:start -->
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+oomkilled&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-OOMKilled-ff7b72?style=flat-square&labelColor=161b22" alt="OOMKilled"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+crashloop&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-CrashLoopBackOff-ff7b72?style=flat-square&labelColor=161b22" alt="CrashLoopBackOff"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+liveness&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Liveness_probe_kill-ff7b72?style=flat-square&labelColor=161b22" alt="Liveness probe kill"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+readiness&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Readiness_failing-ff7b72?style=flat-square&labelColor=161b22" alt="Readiness failing"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+bad-image&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-ImagePullBackOff-ff7b72?style=flat-square&labelColor=161b22" alt="ImagePullBackOff"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+private-registry&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Private_registry-ff7b72?style=flat-square&labelColor=161b22" alt="Private registry"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+missing-secret&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Missing_Secret-ff7b72?style=flat-square&labelColor=161b22" alt="Missing Secret"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+pending&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Pending_forever-ff7b72?style=flat-square&labelColor=161b22" alt="Pending forever"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+volume&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Volume_won%27t_mount-ff7b72?style=flat-square&labelColor=161b22" alt="Volume won't mount"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+stuck-terminating&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Stuck_Terminating-ff7b72?style=flat-square&labelColor=161b22" alt="Stuck Terminating"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+evicted&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Evicted-ff7b72?style=flat-square&labelColor=161b22" alt="Evicted"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+init&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Init_container_fails-ff7b72?style=flat-square&labelColor=161b22" alt="Init container fails"></a>
<a href="https://github.com/Sakuratix/Sakuratix/issues/new?title=break:+rollout&body=Just+press+%22Create%22.+A+bot+will+diagnose+your+incident+within+a+minute+and+close+this+issue."><img src="https://img.shields.io/badge/%F0%9F%92%A5-Stuck_rollout-ff7b72?style=flat-square&labelColor=161b22" alt="Stuck rollout"></a>
<!-- break-menu:end -->
</p>

<!-- break-log:start -->
**Broken 0 times so far.**
<!-- break-log:end -->

## Incident of the day

<!-- incident:start -->
**Incident of the day, 18 November 2026:** Stuck in Terminating for 38m

Every day this section picks one of the failures that [kubectl-why](https://github.com/Sakuratix/kubectl-why) recognises, replays the recorded cluster state with today's clock and lets the tool explain it. Today's fix: A controller is supposed to remove these finalizers. Check that it is running before removing them by hand.

<img src="assets/incident.svg" alt="kubectl why output: Stuck in Terminating for 38m" width="100%">
<!-- incident:end -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/snake-dark.svg">
    <img src="assets/snake-light.svg" alt="the last year of contributions, eaten by a sakura-pink snake" width="100%">
  </picture>
  <br><sub>the contribution graph, eaten daily by <a href=".github/workflows/snake.yml">a snake</a></sub>
</p>

## Stack

<img src="assets/stack.svg" alt="containers: Kubernetes, Docker, Helm, Argo CD; delivery: GitLab CI, GitHub Actions, Trivy, cosign; iac: Terraform, Ansible, Yandex Cloud; observability: Prometheus, Grafana, Loki, Zabbix; systems: Linux, Nginx, MikroTik, WireGuard; data: PostgreSQL, Redis, Kafka; code: Bash, Python, Go" width="100%">

---

<p align="center"><b>Open to remote DevOps roles.</b> Fastest way to reach me:</p>
<p align="center">
  <a href="https://t.me/MountewDew"><img src="https://img.shields.io/badge/Telegram-@MountewDew-8ef0c6?style=for-the-badge&labelColor=161b22&logo=telegram&logoColor=8ef0c6" alt="Telegram"></a>
  <a href="mailto:sakuratoxs@gmail.com"><img src="https://img.shields.io/badge/email-sakuratoxs@gmail.com-8ef0c6?style=for-the-badge&labelColor=161b22&logo=gmail&logoColor=8ef0c6" alt="email"></a>
</p>

<p align="center"><sub>Updated daily by <a href=".github/workflows/update.yml">a GitHub Action</a> · <a href="https://sakuratox.is-a.dev">sakuratox.is-a.dev</a> · numbers and the incident are refreshed by the Action, not typed by hand</sub></p>
