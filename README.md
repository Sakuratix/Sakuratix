<p align="center">
  <img src="assets/signature.svg" alt="sakuratox" width="100%">
</p>

<p align="center">I'm Klim (sakuratox), a DevOps engineer. I build CI/CD, run Kubernetes, write infrastructure as code and set up monitoring, so releases are boring and alerts come before complaints.</p>

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

## Stack

<img src="assets/stack.svg" alt="containers: Kubernetes, Docker, Helm, Argo CD; delivery: GitLab CI, GitHub Actions, Trivy, cosign; iac: Terraform, Ansible, Yandex Cloud; observability: Prometheus, Grafana, Loki, Zabbix; systems: Linux, Nginx, MikroTik, WireGuard; data: PostgreSQL, Redis, Kafka; code: Bash, Python, Go" width="100%">

## Incident of the day

<!-- incident:start -->
**Incident of the day, 15 November 2026:** Stuck creating: a volume can't be mounted

Every day this section picks one of the failures that [kubectl-why](https://github.com/Sakuratix/kubectl-why) recognises, replays the recorded cluster state with today's clock and lets the tool explain it. Today's fix: A ReadWriteOnce volume is still attached to another node (often the old pod during a rollout). Use strategy Recreate or wait for the old pod to go.

<img src="assets/incident.svg" alt="kubectl why output: Stuck creating: a volume can't be mounted" width="100%">
<!-- incident:end -->

<p align="center"><sub>Updated daily by <a href=".github/workflows/update.yml">a GitHub Action</a> · <a href="https://sakuratox.is-a.dev">sakuratox.is-a.dev</a> · <a href="https://t.me/MountewDew">Telegram</a> · sakuratoxs@gmail.com</sub></p>
