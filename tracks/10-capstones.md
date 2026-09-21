# Track 10 — Capstones (competition day)

> **Muscle group:** the whole body, at once, under load.
> **Prereqs:** each capstone lists its own. None of these are "read about" — they are all "build, break, measure, write up."

## Why this track

Bodybuilding has a competition. Without it, training drifts into routine and you never find
out what you actually built. These capstones are that: projects that force multiple tracks
to touch each other, produce something you can show and talk about for 45 minutes, and
expose the gaps that single-track work hides.

**The rule for every capstone:** it isn't done when it works. It's done when you have
**broken it deliberately, measured it, and written it up**. The writeup is the deliverable.
Code that works is table stakes; a writeup that shows you understand *why* it works and
where it fails is what separates levels.

Each capstone lives in `work/10-capstones/<name>/` with a `README.md` covering: the problem,
the design and the alternatives you rejected, the benchmark numbers, the failure modes you
tested, and what you'd do differently.

---

## Capstone 1 — The Instrumented Service (the spine project)

> **Tracks exercised:** 01, 03, 05, 06, 07
> **Do this one first.** It becomes the substrate you use for exercises in every other track.

A real, production-shaped service. Not a tutorial app.

- [ ] **Domain:** pick one with genuine concurrency pressure. Recommended: **event ticketing with seat reservation** (overselling is a real correctness bug you must prevent) or a **multi-tenant job board**
- [ ] FastAPI + Postgres + PgBouncer + Redis + nginx, all in Docker Compose
- [ ] Schema designed to 3NF, indexed deliberately, migrations via Alembic
- [ ] Seeded with **millions of rows** — no toy datasets
- [ ] Row-level security for tenant isolation
- [ ] Structured logging with request IDs, Prometheus metrics (RED), OpenTelemetry traces
- [ ] One Grafana dashboard that answers "is it healthy?" at a glance
- [ ] HTTPS with a real certificate and auto-renewal
- [ ] CI pipeline: lint, test, build, scan, push
- [ ] Graceful shutdown, healthcheck, non-root container under 150MB
- [ ] **Correctness proof:** run 200 concurrent clients all trying to book the last seat. **Exactly one must succeed.** Demonstrate the naive version overselling first, then fix it, then prove the fix
- [ ] **Load test:** find the breaking point with k6. Graph latency vs concurrency. Identify the actual bottleneck with evidence (not a guess)
- [ ] **Optimize:** get 3x throughput. Document every change and its measured effect
- [ ] **Writeup** with before/after numbers and the bottleneck analysis

---

## Capstone 2 — Your Own Database Engine

> **Tracks exercised:** 03, 04, 08
> A small storage engine, written by you.

- [ ] Append-only log with a crash-safe write path (you'll need `fsync` — Track 04 Set 3.2)
- [ ] An in-memory index over it, then a **B+ tree** on disk with real 4KB/8KB pages
- [ ] A page cache with an eviction policy (clock sweep or LRU — Track 08 Set 1.2)
- [ ] A **write-ahead log** and crash recovery. **Test it by `kill -9` mid-write, repeatedly, and verify no corruption and no lost committed writes**
- [ ] MVCC: multiple versions per key with visibility rules, and a snapshot read
- [ ] Basic transactions with at least snapshot isolation
- [ ] A tiny query layer: `GET`, `PUT`, `DELETE`, `SCAN range`
- [ ] Benchmark against SQLite and against a naive file-per-key implementation
- [ ] **Stretch:** an LSM-tree backend as an alternative, with compaction. Benchmark both on write-heavy and read-heavy workloads and produce the crossover graph
- [ ] **Writeup:** every design decision, with the Postgres equivalent named. *"I did X; Postgres does Y instead, because Z."*
- [ ] **Alternative path:** CMU 15-445's **BusTub** projects (buffer pool manager, B+ tree index, query execution, concurrency control). Same learning, with autograders and a real codebase

---

## Capstone 3 — Distributed Key-Value Store

> **Tracks exercised:** 04, 05, 08, 09
> The hardest capstone. Also the most convincing one.

- [ ] Networked KV store with a wire protocol you designed (length-prefixed framing — Track 05 Set 2.3)
- [ ] Replication across 3+ nodes
- [ ] **Raft** for leader election and log replication (your 6.5840 lab work counts here)
- [ ] Persistence and crash recovery — a node restarts and rejoins correctly
- [ ] Sharding across node groups with a configuration service
- [ ] **Linearizable reads** (and know why serving reads from a follower breaks that)
- [ ] Client-side retries with **idempotent request IDs** and duplicate detection
- [ ] **Chaos testing:** partition the network with `tc`/iptables, pause nodes with `SIGSTOP`, kill leaders mid-write, introduce clock skew. **The system must never lose an acknowledged write or serve a stale linearizable read**
- [ ] Write a **linearizability checker** for your own traces, or run **Porcupine**/Jepsen's Knossos against them
- [ ] **Writeup:** the consistency model you provide, precisely stated; the failure modes you tested; and the ones you know you don't handle

---

## Capstone 4 — The Real-Time Data Pipeline

> **Tracks exercised:** 03, 06, 09
> Your Timescale/CDC/Spark items, fused.

- [ ] A producer generating a realistic high-volume event stream (IoT sensors, market ticks, or clickstream) — at least 10k events/sec
- [ ] Kafka (or Redpanda) as the log
- [ ] Stream processor doing windowed aggregations with watermarks and late-event handling
- [ ] Two sinks: **TimescaleDB** (hypertable + continuous aggregate + compression + retention) for the serving layer, and **Parquet on object storage** for the analytical layer
- [ ] **Debezium CDC** off a Postgres OLTP database feeding into the same Kafka, so you have both event-stream and database-change sources
- [ ] A Spark batch job over the Parquet lake that reconciles against the streaming results — **they should agree; when they don't, find out why** (this is the lambda-architecture problem, experienced firsthand)
- [ ] Grafana dashboard showing live data with sub-minute freshness
- [ ] **Measure end-to-end latency at every hop.** Produce a latency budget diagram
- [ ] **Failure testing:** kill the stream processor mid-window and verify correctness after recovery. Kill Kafka. Fill a disk. Replay from an offset
- [ ] **Writeup:** the latency budget, the correctness guarantees at each stage, and where exactly-once is and isn't achieved

---

## Capstone 5 — Local-First Collaborative App

> **Tracks exercised:** 05, 09
> Your Google Docs / IndexedDB items.

- [ ] A collaborative document or whiteboard, multi-user, real-time
- [ ] **CRDT** for document state (Yjs, or your own for extra credit)
- [ ] **IndexedDB** for local persistence — the app must be fully usable offline
- [ ] WebSocket sync server with presence (who's online, cursor positions)
- [ ] **Offline test:** two clients go offline, both edit heavily, both come back. They must converge to the same state, and neither may lose work
- [ ] Server crash mid-sync — clients recover without data loss
- [ ] Handle a client that has been offline for a week
- [ ] **Writeup:** why a CRDT and not OT, the convergence proof sketch, and the UX consequences of eventual consistency (what does the user *see* while converging?)

---

## Capstone 6 — Build a Small Kubernetes-Native Platform

> **Tracks exercised:** 01, 06, 07
> Optional, but it's the one that maps most directly to platform/infra roles.

- [ ] Take Capstone 1 and run it on a real (small) Kubernetes cluster
- [ ] Everything in git: Terraform for infra, Helm/Kustomize for manifests, ArgoCD reconciling
- [ ] Zero-downtime deploys, **proven** with a load generator running through the deploy
- [ ] Horizontal autoscaling that actually triggers under load
- [ ] Full observability stack in-cluster: Prometheus, Grafana, Loki, Tempo
- [ ] SLOs defined with error budgets, and alerts that fire on symptom not cause
- [ ] **GameDay:** kill a node, kill the database pod, fill a PVC, break DNS, exhaust the connection pool. **Predict the outcome before each one.** Write a real incident report for each
- [ ] **Writeup:** your SLOs, your alert rules with justification, and the GameDay results including every prediction you got wrong (those are the valuable ones)

---

## Capstone 7 — The Deep Debugging Portfolio

> **Tracks exercised:** 04, 07, and whichever track the bug lives in
> Not a project — a collection. This is the artifact that most directly demonstrates the thing you said you want to be.

Ten real, hard bugs. Found, diagnosed, and documented. They must include at least one of each:

- [ ] A **memory** bug (leak, corruption, or OOM) found with a profiler, not by guessing
- [ ] A **concurrency** bug (race or deadlock) found with a stack dump or a sanitizer
- [ ] A **performance** bug found with a flame graph, with before/after numbers
- [ ] A **database** bug (bad plan, lock contention, or bloat) found with EXPLAIN and `pg_stat_*`
- [ ] A **network** bug diagnosed from a packet capture
- [ ] A **distributed** bug that only manifests under partition, delay, or clock skew
- [ ] A bug in **someone else's code** — pick an open-source project, reproduce a real open issue, and find the root cause. **Submit the fix.** A merged PR fixing a nontrivial bug in a project you didn't write is worth more than any certificate
- [ ] Three more from your own work

Each one gets an entry in `work/10-capstones/debugging-portfolio/`: symptom, first hypothesis (**including the wrong ones — those show your method**), investigation steps with the actual tool output, root cause, fix, and prevention.

---

## Capstone 8 — Teach It

> The final test, and the cheapest one to skip.

You do not understand something until you can teach it to someone who doesn't.

- [ ] Write 5 deep technical blog posts from your own work in this program. Not tutorials — **explanations of things that confused you until they didn't.** Those are always the best posts
- [ ] Give one talk (a meetup, a work brown-bag, or a recorded screencast) on a topic from this program
- [ ] Answer 20 questions on Stack Overflow or in a community, in your strong areas
- [ ] Explain MVCC, Raft, and virtual memory to three different people at three different levels: a non-engineer, a junior engineer, and a peer. **If you can only do the peer version, you don't understand it yet**
- [ ] Mentor someone through Track 01. Their questions will find your gaps with unnerving accuracy

---

## Exit criteria for Track 10

- [ ] At least 4 capstones complete, each with a real writeup including failure analysis
- [ ] You have a merged PR fixing a real bug in a project you don't own
- [ ] You can talk about any capstone for 45 minutes, including what you'd do differently
- [ ] Someone else has learned something from your writing
