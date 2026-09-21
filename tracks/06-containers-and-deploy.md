# Track 06 — Containers, Orchestration & Deployment

> **Muscle group:** shoulders. Visible, and it carries everything you ship.
> **Prereqs:** Track 01, Track 04 Phase 1 & 4.1 (namespaces/cgroups), Track 05 Phase 1–2.
> **Rule for this track:** you are not allowed to run `docker run` in anger until you have built a container from scratch with `unshare` and `cgroups`. Otherwise Docker stays magic forever.

## Why this track

Containers are the most mystified technology in common use, and the mystification is
unnecessary — there is no such thing as a container. There is a process with namespaces
restricting what it can see and cgroups restricting what it can use. Once you have built
one by hand, every Docker and Kubernetes behavior becomes predictable rather than
memorized.

## Equipment

| Resource | Use it for |
|---|---|
| **"Containers From Scratch"** — Liz Rice (talk + code) and Julia Evans' *How Containers Work* zine | Phase 1. The demystification. |
| **Docker official docs** + *Docker Deep Dive* (Nigel Poulton) | Phase 2 |
| **Kubernetes docs** — Concepts section | Phase 3 |
| **Kubernetes The Hard Way** — Kelsey Hightower | Phase 4 (the one that actually teaches you k8s) |
| **The Twelve-Factor App** (12factor.net) | Read once, internalize forever |
| **Google SRE Book** (free, sre.google/books) — Ch. 1–6, 21–23 | Phase 4 |

---

## Phase 1 — Foundation (there is no such thing as a container)

### Set 1.1 — Namespaces
- [ ] The seven namespaces: **PID, NET, MNT, UTS, IPC, USER, CGROUP**. What each one isolates
- [ ] `unshare`, `nsenter`, `/proc/<pid>/ns/`, `clone()` flags
- [ ] **Rep:** `sudo unshare --pid --fork --mount-proc bash` then `ps aux`. You are PID 1. Explain what just happened
- [ ] **Rep:** create a network namespace with `ip netns`, give it a veth pair, assign IPs, and ping across it. **This is exactly what Docker's bridge network is.** Document in `notes/netns.md`
- [ ] **Rep:** use a mount namespace + `pivot_root` (or `chroot` as a first step) with a extracted Alpine rootfs to get a shell that sees a different filesystem
- [ ] User namespaces and rootless containers. UID mapping. Why this is the security story

### Set 1.2 — cgroups
- [ ] cgroups v1 vs v2. The unified hierarchy at `/sys/fs/cgroup`
- [ ] Controllers: `cpu` (shares/quota/period), `memory` (limit, swap, OOM), `io`, `pids`
- [ ] **Rep:** create a cgroup by hand, add a CPU-burning process to it, set `cpu.max` to 50%, and watch `htop` obey you
- [ ] **Rep:** set a `memory.max` of 100MB and run a process that allocates 200MB. Read the cgroup OOM kill in `dmesg`. Explain why this differs from a system-wide OOM
- [ ] Understand **why the JVM and Node used to ignore container memory limits** (they read `/proc/meminfo`, which is not namespaced) and how that was fixed

### Set 1.3 — Build a container runtime
- [ ] **Rep (capstone of Phase 1):** write `mycontainer` (~150 lines of Go or C) that: creates new PID/UTS/MNT/NET namespaces, `pivot_root`s into a rootfs you downloaded, mounts `/proc`, sets a hostname, applies a cgroup memory limit, and executes a shell. **When this works, containers are permanently demystified**
- [ ] Write up what your toy is missing compared to `runc`: seccomp, capabilities, AppArmor/SELinux, cgroup cleanup, OCI spec compliance, layered filesystem

---

## Phase 2 — Volume (Docker in depth)

### Set 2.1 — Images and layers
- [ ] Images vs containers vs layers. The **union filesystem** (overlayfs): lowerdir, upperdir, merged, the **copy-up** on write
- [ ] **Rep:** find the overlay2 directories for a running container on disk. Modify a file inside the container and find the copy-up in `upperdir`
- [ ] Image manifests, config, digests, content addressing. `docker image inspect`, `dive` tool
- [ ] **Dockerfile** properly: `FROM`, `RUN`, `COPY` vs `ADD`, `WORKDIR`, `ENV` vs `ARG`, `EXPOSE`, `VOLUME`, `USER`, **`ENTRYPOINT` vs `CMD`** (know both forms and how they combine), `HEALTHCHECK`
- [ ] **Layer caching** — why layer order matters, and the dependency-install-before-code-copy pattern
- [ ] **Multi-stage builds** — build in a fat image, ship a thin one
- [ ] Base image choice: `distroless` vs `alpine` (and the **musl vs glibc** performance/compat trap for Python) vs `slim` vs full
- [ ] **Rep:** take a naive 1.2GB Python or Node image and get it under 150MB with multi-stage + a slim base + `.dockerignore`. Record the before/after in `notes/image-slimming.md`
- [ ] **Rep:** rebuild after a one-line code change. Get it to under 5 seconds by fixing layer ordering
- [ ] BuildKit: cache mounts, `--mount=type=cache`, parallel stages, secrets at build time (`--mount=type=secret` — **never** `ARG` a secret; prove to yourself why with `docker history`)
- [ ] Security: run as non-root, drop capabilities, read-only root filesystem, `no-new-privileges`, scan with `trivy` or `grype`
- [ ] **Rep:** scan your images, fix the high-severity findings, and re-scan

### Set 2.2 — Running containers
- [ ] `docker run` flags that matter: `-d`, `-p` (and the difference from `EXPOSE`), `-v` vs `--mount`, `-e`, `--env-file`, `--rm`, `--name`, `--restart`, `--memory`, `--cpus`, `--network`, `--user`, `--init`
- [ ] **PID 1 problem** — why your container doesn't respond to Ctrl-C, why zombies accumulate, and what `--init`/`tini` fixes. (This is Track 04 Set 1.1 showing up in production)
- [ ] **Rep:** demonstrate the PID 1 signal problem, then fix it two ways (exec form ENTRYPOINT, and `--init`)
- [ ] Volumes: named volumes vs bind mounts vs tmpfs. Permission problems with bind mounts (UID mismatch) and how to solve them
- [ ] Networking: bridge, host, none, custom bridge (with DNS between containers), macvlan. Port publishing and iptables rules
- [ ] **Rep:** `iptables -t nat -L -n` after publishing a port. Find the DNAT rule Docker created. Now you know what `-p` does
- [ ] Logging drivers, `docker logs`, log rotation (and the classic "docker filled the disk with JSON logs" incident)
- [ ] `docker exec`, `docker inspect`, `docker stats`, `docker system df`, `docker system prune`
- [ ] **Debugging a container that won't start**: `docker logs`, `--entrypoint sh`, `docker run` the previous layer, `docker cp`. Write the checklist in `notes/container-debug.md`

### Set 2.3 — Compose and local environments
- [ ] `docker compose` — services, networks, volumes, `depends_on` with `condition: service_healthy`, profiles, env interpolation
- [ ] **Rep:** a full local stack in one `compose.yaml`: FastAPI + Postgres + Redis + PgBouncer + nginx + Prometheus + Grafana. `docker compose up` and everything works. This becomes your standard dev environment for the rest of the program
- [ ] Healthchecks that are real (not `exit 0`), startup ordering, and restart policies
- [ ] Understand why compose is not a production orchestrator

### Set 2.4 — nerdctl / containerd / the ecosystem (your listed item)
- [ ] The layering: **OCI spec** → `runc` (low-level runtime) → `containerd` (high-level runtime) → Docker Engine / Kubernetes CRI
- [ ] Why Kubernetes dropped dockershim, and why that was a non-event for most people
- [ ] **nerdctl** — Docker-compatible CLI over containerd. Install it, run your images with it, and note what's different
- [ ] `ctr` (containerd's raw CLI) — use it once to see the layer below nerdctl
- [ ] **Podman** — daemonless, rootless, pods. `podman generate systemd` (ties into Track 01's systemd work)
- [ ] **Buildah** / **Kaniko** — building images without a Docker daemon (matters in CI)
- [ ] **Rep:** run the same image under docker, nerdctl, and podman. Write `notes/runtimes.md` on what differs and when you'd pick each

### Set 2.5 — Ship your app (FastAPI + uvicorn — your listed item)
- [ ] ASGI vs WSGI. Why FastAPI is ASGI and what that buys you (link to Track 04 Set 2.2 — event loops)
- [ ] **uvicorn** vs **gunicorn + uvicorn workers** vs **hypercorn**. Worker counts, `--workers` vs an external process manager
- [ ] **Rep:** know when to use `async def` vs `def` in FastAPI, and prove it: write a FastAPI endpoint doing a blocking DB call inside `async def`. Load test it, watch throughput collapse. Fix it (threadpool or async driver) and re-measure. **This single experiment teaches more about async than any article**
- [ ] Containerize it properly: non-root user, multi-stage, `--no-cache-dir`, healthcheck endpoint, graceful shutdown on SIGTERM, correct worker count
- [ ] **Graceful shutdown** — draining in-flight requests on SIGTERM before exit. Test it under load
- [ ] Config via environment (12-factor), secrets not in the image, `pydantic-settings`
- [ ] **pm2** for the Node side of things (already covered in Track 01 Set 2.4) — deploy a Node service under pm2 in cluster mode and compare it with running N containers
- [ ] **Rep:** load test your containerized API with `k6` or `locust`. Find the bottleneck (it will be the database connection pool). Fix it. Re-test

---

## Phase 3 — Strength (Kubernetes)

### Set 3.1 — The mental model
- [ ] **Declarative, not imperative.** The control loop / reconciliation model. `desired state` vs `actual state`. This one idea explains 80% of Kubernetes
- [ ] Control plane: API server, etcd, scheduler, controller manager. Node: kubelet, kube-proxy, container runtime
- [ ] **Rep:** draw the full flow for `kubectl apply -f deploy.yaml` — what each component does, in order. Save as `notes/k8s-apply-flow.md`

### Set 3.2 — Workload objects
- [ ] **Pod** — the atom. Multiple containers, shared network namespace and volumes. Init containers. Sidecars
- [ ] **ReplicaSet** → **Deployment** — rolling updates, `maxSurge`/`maxUnavailable`, rollback, revision history
- [ ] **StatefulSet** — stable identity, ordered rollout, per-pod PVCs. Why databases need this
- [ ] **DaemonSet**, **Job**, **CronJob**
- [ ] **Service** types: ClusterIP, NodePort, LoadBalancer, ExternalName. Headless services
- [ ] **How a Service actually works** — kube-proxy, iptables/IPVS rules, endpoints, cluster DNS (CoreDNS). Not magic; it's the iptables from Set 2.2 again
- [ ] **Ingress** and **Gateway API** — L7 routing, TLS termination, ingress controllers (nginx, Traefik)
- [ ] **ConfigMap** and **Secret** (and knowing Secrets are just base64, not encrypted at rest by default)
- [ ] Volumes, PersistentVolume, PersistentVolumeClaim, StorageClass, dynamic provisioning
- [ ] **Resource requests and limits** — and the crucial distinction: requests drive scheduling, limits drive throttling/OOM-kill. **CPU throttling** from limits is a top-5 production mystery
- [ ] **Rep:** set a CPU limit too low, observe throttling in metrics (`container_cpu_cfs_throttled_seconds_total`), and correlate it with latency spikes
- [ ] **Probes**: liveness vs readiness vs startup. **Get this wrong and a slow-starting app gets killed in a restart loop.** Configure all three correctly for your FastAPI app
- [ ] Namespaces, labels and selectors, annotations, RBAC (Role, RoleBinding, ServiceAccount)
- [ ] `kubectl` fluency: `get -o yaml`, `describe`, `logs -f --previous`, `exec`, `port-forward`, `top`, `apply --dry-run=server`, `diff`, `events --sort-by`, `debug`

### Set 3.3 — Run something real
- [ ] Local cluster: **kind** or **k3d** (fast, disposable). Then try k3s on your VM
- [ ] **Rep:** deploy your FastAPI + Postgres stack to the cluster. Deployment for the app, StatefulSet + PVC for Postgres, Services, Ingress with TLS, ConfigMap + Secret, HPA
- [ ] **Rep:** do a rolling update with zero dropped requests. Prove it with a load generator running throughout. You will need: readiness probes, `preStop` hooks, graceful shutdown, and `terminationGracePeriodSeconds`. **Getting to actually-zero is the exercise**
- [ ] HorizontalPodAutoscaler on CPU, then on a custom metric
- [ ] PodDisruptionBudget, node affinity/anti-affinity, taints and tolerations, topology spread
- [ ] **Helm** — charts, values, templating, `helm diff`. Or **Kustomize** — overlays. Know both, pick one
- [ ] **Rep:** package your app as a Helm chart with dev/staging/prod values

### Set 3.4 — Kubernetes debugging drills
- [ ] **Drill:** Pod stuck in `Pending`. (Insufficient resources / no matching node / PVC unbound / taints)
- [ ] **Drill:** `CrashLoopBackOff`. Get the logs from the *previous* container instance
- [ ] **Drill:** `ImagePullBackOff`. Registry auth, wrong tag, wrong arch (arm64 vs amd64 — a common one on Apple Silicon)
- [ ] **Drill:** `OOMKilled`. Find it in the pod status, correlate with the limit, decide whether to raise the limit or fix the leak
- [ ] **Drill:** Service returns nothing. Walk it: endpoints populated? → selector matches labels? → readiness passing? → port names right? → DNS resolving?
- [ ] **Drill:** "It's slow." CPU throttling, noisy neighbor, or DNS (CoreDNS is a shockingly common culprit — `ndots:5` and search-domain amplification)
- [ ] **Capstone:** `notes/k8s-3am-runbook.md`

---

## Phase 4 — Peak (production engineering)

### Set 4.1 — CI/CD
- [ ] Pipeline stages: lint → test → build → scan → push → deploy → smoke test
- [ ] **GitHub Actions** — workflows, jobs, steps, matrix builds, caching, reusable workflows, OIDC auth to a cloud provider (no long-lived secrets)
- [ ] **Rep:** full pipeline for your app: on PR run tests + lint + build; on merge to main build, scan, push a tagged image, and deploy to your cluster
- [ ] Deployment strategies: rolling, blue/green, canary, feature flags. Progressive delivery (Argo Rollouts / Flagger)
- [ ] **GitOps** — ArgoCD or Flux. Git as the source of truth, the cluster reconciles toward it
- [ ] **Rep:** set up ArgoCD to watch your manifests repo. Change an image tag in git, watch the cluster follow. Then change something in the cluster by hand and watch Argo revert it

### Set 4.2 — Infrastructure as code
- [ ] **Terraform/OpenTofu** — providers, resources, state (and why state is the whole game), `plan` vs `apply`, modules, remote state with locking
- [ ] **Rep:** provision your VM + firewall rules + DNS record entirely in Terraform. Destroy it. Recreate it. It should be identical
- [ ] Drift, `import`, and the danger of manual changes
- [ ] Ansible as the config-management complement (or just use your idempotent script from Track 01 Set 3.2 and understand what Ansible adds)

### Set 4.3 — Spark clusters (your listed item)
- [ ] Spark architecture: driver, cluster manager, executors, tasks, stages, shuffle
- [ ] Deployment modes: local, standalone, YARN, **Kubernetes**, and `client` vs `cluster` deploy mode
- [ ] **Rep:** run a Spark standalone cluster in Docker Compose — 1 master + 3 workers. Submit a job with `spark-submit`
- [ ] **Spark UI** — Jobs, Stages, Tasks, Storage, Environment, Executors, SQL tabs. Read a DAG. Find a **shuffle**. Find **skew** (one task taking 10x the others)
- [ ] **Rep:** write a job with deliberate data skew. Find it in the Spark UI. Fix it (salting / repartitioning / broadcast join). Document before/after stage timings in `notes/spark-skew.md`
- [ ] **Rep:** run Spark on your Kubernetes cluster (`spark-submit --master k8s://...`). Watch executor pods get created and destroyed
- [ ] The RDD / DataFrame / window-function content lives in **Track 09 Set 3.3** — this set is about *operating* the cluster

### Set 4.4 — Reliability engineering
- [ ] Read **Google SRE Book** Ch. 1–6 (SLIs, SLOs, error budgets, eliminating toil, monitoring) and Ch. 21–23
- [ ] Define real SLIs and SLOs for your own app. Write them down with the measurement query
- [ ] Capacity planning, load shedding, graceful degradation, backpressure
- [ ] **Chaos engineering**: kill a pod, kill a node, partition the network (`tc netem`, Chaos Mesh), fill a disk. Every time, predict the outcome *first*, then run it
- [ ] **Rep:** run a GameDay on your own stack. Write the incident report as if it were real: timeline, impact, root cause, action items, and what monitoring would have caught it sooner
- [ ] Postmortem culture: blameless, the 5 whys and its limits, action items with owners

---

## Exit criteria for Track 06

- [ ] You built a container from scratch with namespaces and cgroups
- [ ] Your app ships as a <150MB image, runs as non-root, and shuts down gracefully
- [ ] You did a zero-downtime rolling update and *proved* zero dropped requests
- [ ] You can debug Pending / CrashLoop / ImagePull / no-endpoints without looking anything up
- [ ] Your whole environment is reproducible from git — no manual steps anywhere
- [ ] You ran a GameDay and wrote a real postmortem
