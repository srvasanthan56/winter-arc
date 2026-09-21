# Track 07 — Debugging & Observability

> **Muscle group:** the nervous system. Not a muscle — the thing that tells you which muscle is failing.
> **Prereqs:** Track 01 Phase 2, Track 04 Phase 0 (C/memory basics help).
> **This track runs continuously.** Don't wait until you "finish" other tracks. Every bug you hit anywhere in this program is a rep for this track.

## Why this track

You said you want to be someone who can fix things at 3AM. That's this track. Everything
else in the program gives you the domain knowledge; this one gives you the *method*.

The uncomfortable truth about most engineers, including senior ones: their debugging is
random. They change things and see what happens. The difference at FAANG level is that
debugging becomes a **repeatable, evidence-driven procedure** — you form hypotheses, you
design the cheapest experiment that discriminates between them, and you converge. You
should be able to explain, out loud, why your next action is the right next action.

## Equipment

| Resource | Use it for |
|---|---|
| **Debugging** — David J. Agans (the 9 rules) | Short, and the best book on the *method* |
| **Why Programs Fail** — Andreas Zeller | The scientific method applied to bugs; delta debugging |
| **Julia Evans** — *Debugging Zine*, *Profiling & Tracing*, her whole blog | The practical craft |
| **BPF Performance Tools** — Brendan Gregg | Phase 4 |
| MIT Missing Semester **Lecture 8: Metaprogramming** and **L9: Debugging & Profiling** | Tooling overview |
| **Distributed Systems Observability** — Cindy Sridharan (free) | Phase 3 |

---

## Phase 1 — Foundation (the method, before the tools)

### Set 1.1 — The nine rules
- [ ] Read Agans' *Debugging*. The rules: Understand the system / Make it fail / Quit thinking and look / Divide and conquer / Change one thing at a time / Keep an audit trail / Check the plug / Get a fresh view / If you didn't fix it, it ain't fixed
- [ ] Write `notes/debugging-method.md` in your own words, with a real bug you've fixed as an example for each rule
- [ ] **The single most important rule: "Quit thinking and look."** Most wasted debugging time is spent theorizing instead of observing. Catch yourself doing it

### Set 1.2 — Reproduce first
- [ ] Minimal reproduction: shrink the input, shrink the code, shrink the environment
- [ ] **Delta debugging** — bisect the *input*, not just the commit history. `git bisect` is the same algorithm applied to time
- [ ] **Rep:** take a bug triggered by a 10,000-line input file and mechanically reduce it to the smallest failing input
- [ ] Deterministic vs flaky: how to make a race condition reproduce (add sleeps, add load, run 1000 times, use `stress-ng`, `rr` record/replay)
- [ ] **Rep:** write a flaky test caused by a real race. Then make it fail 100% of the time

### Set 1.3 — The audit trail
- [ ] Keep a debugging log for every nontrivial bug: symptom → what you observed → hypotheses → experiment → result → next hypothesis
- [ ] **Rep:** do this for your next 5 real bugs. Files in `work/07-debugging/logs/`. Review them after and look for your own patterns — what do *you* typically waste time on?
- [ ] Read a few real public postmortems (GitLab's 2017 database incident, Cloudflare's regex outage, AWS S3 2017). Note how the root cause is never the first thing they suspected

---

## Phase 2 — Volume (tools, one per language/layer)

### Set 2.1 — Interactive debugging in VS Code (your listed item)
- [ ] `launch.json` anatomy: `type`, `request` (`launch` vs **`attach`**), `program`, `args`, `env`, `cwd`, `preLaunchTask`, `justMyCode`
- [ ] **Breakpoints beyond the basics** — this is where most people stop and shouldn't:
  - [ ] **Conditional breakpoints** (`i == 4732`) — stop on the one iteration that matters
  - [ ] **Hit count breakpoints**
  - [ ] **Logpoints** — log without modifying code or redeploying. Enormously useful
  - [ ] **Exception breakpoints** — break on caught/uncaught exceptions
  - [ ] **Data/watchpoints** — break when a variable changes (gdb `watch`; limited in VS Code)
  - [ ] Function breakpoints (break by name, no line number needed)
- [ ] The debug panes: Variables, Watch, **Call Stack**, Breakpoints, Debug Console (you can *evaluate expressions* here — use it)
- [ ] Step Over / Step Into / Step Out / Continue / **Run to Cursor** / **Restart Frame**
- [ ] **Rep:** debug a recursive function and read the whole call stack. Use Restart Frame to re-run one level without restarting the program
- [ ] **Python**: `debugpy`, launch configs for FastAPI/uvicorn, `--reload` interactions, `breakpoint()`, `pdb`/`ipdb` command set (`n s c l p pp w u d b tbreak q`), post-mortem debugging (`pdb.pm()`)
- [ ] **Rep:** attach the VS Code debugger to a FastAPI app running **inside a Docker container** (`debugpy --listen 0.0.0.0:5678 --wait-for-client` + port mapping + `pathMappings`). This is the setup that pays off constantly
- [ ] **Node.js**: `--inspect` / `--inspect-brk`, the `node` debug type, attaching to a running process, `NODE_OPTIONS`
- [ ] **Rep:** attach to a running Node process in a container and set a breakpoint in a live request handler
- [ ] **Browser/web**: Chrome DevTools — Sources panel, breakpoints, **XHR/fetch breakpoints**, **DOM mutation breakpoints**, **event listener breakpoints**, blackboxing library code, source maps
- [ ] **Rep:** debug a minified production bundle using source maps
- [ ] DevTools beyond Sources: Network (waterfall, timing breakdown, initiator chain, throttling), Performance (flame chart, long tasks, layout thrashing), Memory (heap snapshot, allocation timeline), Console (`console.table`, `console.time`, `$0`, `monitorEvents`, `debug(fn)`)
- [ ] **Rep:** find and fix a memory leak in a browser app using three heap snapshots and the comparison view
- [ ] **Rep:** find a React/JS performance problem in the Performance tab and fix it. Prove it with before/after flame charts
- [ ] Remote debugging: VS Code Remote-SSH, Dev Containers. Debug code running on your VM from your laptop

### Set 2.2 — Native debugging with gdb
- [ ] `gdb ./prog`, `run`, `break file:line`, `break func`, `continue`, `next`, `step`, `finish`, `until`
- [ ] Inspection: `print`, `p/x`, `x/16xb`, `info locals`, `info args`, `info registers`, `backtrace`, `frame N`, `ptype`
- [ ] **Watchpoints**: `watch var`, `rwatch`, `awatch` — break when memory changes. The killer feature gdb has that IDEs mostly don't
- [ ] Threads: `info threads`, `thread N`, **`thread apply all bt`** (the first command to run on a hung multithreaded process)
- [ ] **Attaching to a running process**: `gdb -p <pid>`. And `gdb -p` on a hung production process to get a stack trace
- [ ] **Core dumps**: enable with `ulimit -c unlimited` + `/proc/sys/kernel/core_pattern`, then `gdb ./prog core`. **Post-mortem debugging of a crash you didn't witness** — this is a genuine 3AM skill
- [ ] **Rep:** segfault a program, get a core dump, and find the exact line and the bad pointer value from the core alone
- [ ] `.gdbinit`, TUI mode (`gdb -tui`), and `pwndbg`/`gef` if you're doing security work
- [ ] **Rep:** attach gdb to a *deadlocked* program, get all thread stacks, and identify the lock cycle (ties to Track 04 Set 2.2)

### Set 2.3 — Observing without stopping
- [ ] **`strace`** (Track 01 Set 2.3 — now use it on real bugs). `strace -f -T -tt -p <pid>` on a hung process. **If it's sitting in a syscall, you just found your answer**
- [ ] `ltrace`, `lsof -p`, `/proc/<pid>/stack`, `/proc/<pid>/wchan`
- [ ] **`py-spy`** — sample a *running* Python process without modifying it. `py-spy dump -p <pid>` for an instant stack trace, `py-spy top`, `py-spy record` for a flame graph. **This is the best Python production debugging tool that exists**
- [ ] **Rep:** hang a Python process (deadlock or a slow call) and diagnose it with `py-spy dump` alone
- [ ] Equivalents elsewhere: `jstack`/`jcmd`/async-profiler (JVM), `node --inspect` + `--cpu-prof`, `delve`/`pprof` (Go), `rbspy` (Ruby)
- [ ] **Rep:** send `SIGQUIT` to a JVM (or use `jstack`) and read a thread dump. Identify a `BLOCKED` thread and what it's waiting on

### Set 2.4 — Profiling
- [ ] CPU profiling: sampling vs instrumenting. Why sampling is usually right
- [ ] **`perf`**: `perf stat` (IPC, cache misses, branch misses), `perf record -F 99 -g -p <pid>`, `perf report`, `perf top`
- [ ] **Flame graphs** — how to read them (width = time, y = stack depth, **x-order is meaningless**), how to generate them, and **differential flame graphs** for before/after
- [ ] **Rep:** profile a slow program, produce a flame graph, identify the hot path, fix it, and produce a differential flame graph showing the improvement. Save to `notes/flamegraph-case.md`
- [ ] Memory profiling: `valgrind --leak-check=full`, `massif`, AddressSanitizer, `memray`/`tracemalloc` (Python), heap snapshots (Node/browser)
- [ ] **Rep:** find a real memory leak in a long-running service, using memory profiling rather than guessing
- [ ] I/O profiling: `iotop`, `biolatency`, `blktrace`
- [ ] Off-CPU analysis — the time your program spends *not* running. Often where the latency actually is

---

## Phase 3 — Strength (observability in production)

### Set 3.1 — Logging that helps
- [ ] Structured logging (JSON), consistent field names, levels that mean something
- [ ] **Correlation IDs / request IDs** — propagate one through every log line in a request's lifetime, across services. Non-negotiable for distributed debugging
- [ ] What to log: decisions and boundaries. What not to log: PII, secrets, high-cardinality spam, anything in a hot loop
- [ ] Sampling, rate limiting, and the cost of logging (logging *is* I/O and *is* a latency source)
- [ ] **Rep:** instrument your FastAPI app with structured logs + request IDs + a middleware that logs method, path, status, and duration. Then answer, from logs alone: "what was the p99 latency of endpoint X in the last hour, and which requests were the slow ones?"
- [ ] Centralized logging: Loki, ELK, or a hosted option. Understand the index-vs-scan tradeoff (Loki indexes labels only)

### Set 3.2 — Metrics
- [ ] The **four golden signals**: latency, traffic, errors, saturation. And the **RED** (rate/errors/duration) and **USE** (utilization/saturation/errors) methods
- [ ] Metric types: counter, gauge, histogram, summary. **Why you almost always want a histogram, not an average**
- [ ] **Percentiles**: p50/p90/p99/p99.9. Why averages lie. Why you can't average percentiles across instances. Why p99 matters more as you fan out (tail latency amplification — read Dean & Barroso's *The Tail at Scale*)
- [ ] **Cardinality** — the thing that kills metrics systems. Never put a user ID in a label
- [ ] **Prometheus**: the data model, scraping, exporters, **PromQL** (`rate`, `irate`, `increase`, `histogram_quantile`, `sum by`, `topk`, `offset`), recording rules, alerting rules, Alertmanager
- [ ] **Grafana**: dashboards, variables, and the discipline of building a dashboard that answers a *question* rather than showing everything
- [ ] **Rep:** instrument your app with `prometheus-client`. Export RED metrics. Build one Grafana dashboard that shows request rate, error rate, p50/p95/p99 latency, and DB pool saturation — on a single screen
- [ ] **Rep:** write 5 alerting rules you'd genuinely want to be woken up for, and 5 you wouldn't. Explain the difference in `notes/alerting.md`. The test: **every alert must be actionable**
- [ ] Alert fatigue, symptom-based vs cause-based alerting, and why "CPU > 80%" is usually a bad alert

### Set 3.3 — Tracing
- [ ] Distributed tracing concepts: trace, span, parent/child, context propagation, baggage, sampling (head vs tail)
- [ ] **OpenTelemetry** — the SDK, auto-instrumentation, the collector, exporters. Trace context via W3C `traceparent` headers
- [ ] **Rep:** instrument a 3-service call chain (API → service → database) with OTel. View the trace in Jaeger or Tempo. Find the slow span
- [ ] **Rep:** add a deliberate N+1 query in one service. Find it purely from the trace waterfall. This is the canonical thing tracing is for
- [ ] Exemplars — linking a metric spike to a specific trace
- [ ] The three pillars and why they're really one thing: high-cardinality structured events. Read Charity Majors on observability vs monitoring

### Set 3.4 — Debugging distributed systems
- [ ] Why distributed bugs are different: partial failure, no global clock, nondeterministic interleavings, the network lies
- [ ] The "unknown unknowns" problem — you can't dashboard for a failure mode you didn't predict. This is the argument for high-cardinality exploration
- [ ] **Rep:** debug a problem across your whole stack (nginx → FastAPI → PgBouncer → Postgres) using correlation IDs to stitch logs from all four layers into one timeline
- [ ] Clock skew, retries causing duplicate work, cascading failures, and the difference between "slow" and "down" (a slow dependency is worse)

---

## Phase 4 — Peak (eBPF and the 3AM synthesis)

### Set 4.1 — eBPF
- [ ] What eBPF is: safe, verified programs running in the kernel, attached to tracepoints/kprobes/uprobes. Why it changed observability
- [ ] **bcc** and **bpftrace** tools: `execsnoop`, `opensnoop`, `tcpconnect`, `tcpretrans`, `biolatency`, `runqlat`, `offcputime`, `profile`
- [ ] **Rep:** use `execsnoop` to catch a short-lived process that `ps` can never see (the classic "something is spawning processes and I don't know what")
- [ ] **Rep:** use `tcpretrans` and `tcplife` to diagnose a network issue that `tcpdump` would have drowned you in
- [ ] **Rep:** write one custom `bpftrace` one-liner for a question you actually have about your own system
- [ ] Know that this is what Cilium, Pixie, and modern APM agents are built on

### Set 4.2 — The synthesis
- [ ] **Capstone:** consolidate the per-track runbooks (Linux, Postgres, network, k8s) into one `RUNBOOK.md` at the repo root. Organized by *symptom*, not by technology — because at 3AM you know the symptom, not the cause
- [ ] The runbook must cover, for each symptom: first 3 commands, what each possible output means, and the branch to take next
- [ ] **Rep:** have someone (or an AI) break something in your stack without telling you what. Fix it using only your runbook. Then improve the runbook based on where it failed you
- [ ] Do this **five times** with five different injected faults. Each round, the runbook gets better and you get faster
- [ ] **Rep:** write `notes/how-i-debug.md` — your personal, explicit debugging procedure. If you can hand this to a junior and they get measurably better, it's good enough

---

## Exit criteria for Track 07

- [ ] Your debugging is a procedure you can articulate, not intuition
- [ ] You can get a stack trace out of any hung process in any of your languages, in under a minute
- [ ] You can profile and prove a performance improvement with data, not vibes
- [ ] Your services emit useful logs, metrics, and traces by default
- [ ] `RUNBOOK.md` exists, is symptom-organized, and has survived five injected-fault drills
