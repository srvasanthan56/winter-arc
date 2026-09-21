# Winter Is Coming

**A training program to become a FAANG-level engineer.**

Not a course. Not a 90-day bootcamp. A **training program** — the kind you follow for a
year, where progress comes from consistent volume and honest tracking rather than
motivation. There is no daily schedule here on purpose. Open this file, see where you are,
pick up the next rep, put it down when you're done. The checkboxes are the whole system.

> **The goal, in your words:** *someone who can fix it at 3AM.* Everything in here is
> organized around that. Not knowing *about* things — being able to walk into a broken
> system with a terminal and a hypothesis, and come out the other side.

---

## Progress

<!-- PROGRESS:START -->
### Overall: 0 / 1255 reps complete — **0.0%**

`░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░`

| # | Track | Progress | Done | Status |
|---|-------|----------|------|--------|
| 01 | [Linux & Command-Line Toolcraft](tracks/01-linux-and-toolcraft.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/107 | not started |
| 02 | [Git](tracks/02-git.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/91 | not started |
| 03 | [SQL & PostgreSQL](tracks/03-sql-and-postgres.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/249 | not started |
| 04 | [Operating Systems](tracks/04-os-internals.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/112 | not started |
| 05 | [Networking](tracks/05-networking.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/111 | not started |
| 06 | [Containers, Orchestration & Deployment](tracks/06-containers-and-deploy.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/113 | not started |
| 07 | [Debugging & Observability](tracks/07-debugging-and-observability.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/96 | not started |
| 08 | [Algorithms & Data Structures](tracks/08-algorithms-and-dsa.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/110 | not started |
| 09 | [Distributed Systems & Data Engineering](tracks/09-distributed-systems-and-data.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/188 | not started |
| 10 | [Capstones](tracks/10-capstones.md) | `░░░░░░░░░░░░░░░░░░░░`   0.0% | 0/78 | not started |

_Regenerate with_ `python progress.py`
<!-- PROGRESS:END -->

```bash
python progress.py           # update this table and print the summary
python progress.py --detail  # per-phase breakdown for every track
python progress.py --next    # the next open rep in each track
```

---

## How to use this

**1. Check boxes only when you can prove it.**
The checkbox means "I did it and I could do it again," not "I read about it." A rep marked
**Rep:** produces an artifact. A rep marked **Drill:** is something you broke and fixed.
The honest failure mode of every self-study plan is checking boxes for reading — don't.

**2. Everything you build goes in `work/`.**
`work/<track>/` holds code, `notes/` holds writeups. If it isn't committed, it didn't
happen. In a year this directory *is* your evidence, for interviews and for yourself.

**3. Train 2–3 tracks at a time, never all ten.**
See the training blocks below. Tracks have prerequisites, and the order is load-bearing:
DDIA lands differently after you've run `EXPLAIN` on a real query and watched TCP
retransmit. That ordering is most of the value of this document.

**4. Depth beats coverage.**
One topic understood to the bottom is worth twenty skimmed. When you hit something you
half-understand, stop and go down. That instinct *is* the skill you're building.

**5. Write it down.**
Every phase ends in a writeup. This is not busywork — explaining something is the only
reliable test of whether you know it. Most `notes/` files listed here will be more useful
to you six months later than the exercise that produced them.

**6. Deload when you need to.**
Some weeks you'll do two boxes. That's fine — this is a marathon and burnout is the only
real failure mode. Missing a week costs nothing. Quitting costs everything.

---

## The tracks

| # | Track | What it makes you |
|---|-------|-------------------|
| 01 | [Linux & Command-Line Toolcraft](tracks/01-linux-and-toolcraft.md) | Able to drive any machine over SSH with no GUI |
| 02 | [Git](tracks/02-git.md) | Unable to lose work; the person the team asks |
| 03 | [SQL & PostgreSQL](tracks/03-sql-and-postgres.md) | Able to read a query plan and fix a database |
| 04 | [Operating Systems](tracks/04-os-internals.md) | Able to explain any process's behavior from first principles |
| 05 | [Networking](tracks/05-networking.md) | Able to say which of DNS/TCP/TLS/HTTP is actually broken |
| 06 | [Containers & Deployment](tracks/06-containers-and-deploy.md) | Able to ship and operate, not just build |
| 07 | [Debugging & Observability](tracks/07-debugging-and-observability.md) | Systematic under pressure — **the 3AM track** |
| 08 | [Algorithms & Data Structures](tracks/08-algorithms-and-dsa.md) | Sharp, and interview-ready |
| 09 | [Distributed Systems & Data](tracks/09-distributed-systems-and-data.md) | Senior. This is the one that changes your level |
| 10 | [Capstones](tracks/10-capstones.md) | Able to prove all of the above |

Each track is split into four phases with the same shape:

| Phase | Bodybuilding analogue | What it means here |
|---|---|---|
| **Phase 1 — Foundation** | Learning the movement | Core concepts and correct form. Don't add weight yet. |
| **Phase 2 — Volume** | Hypertrophy | Breadth, tool fluency, lots of reps |
| **Phase 3 — Strength** | Heavy compound lifts | Hard, integrative work. Build things. |
| **Phase 4 — Peak** | Competition prep | Internals, performance, and drills under pressure |

---

## Training blocks (the order to do it in)

Not dates — **sequence**. Move to the next block when the current one's gate is met. Some
people take four months on Block 1, some take six weeks. Both are fine.

### Block 1 — Base
**Tracks 01 (P1–2), 02 (P1–2), 03 (P1), 08 (ongoing)**

Get the hands working. Shell, git's data model, SQL that returns correct answers. Track 08
starts now and never stops — 3 problems a week, forever.

> **Gate:** you can navigate and debug a Linux box over SSH, you can explain what a git
> commit object contains, and you can write a correct multi-join query with window functions.

### Block 2 — Build
**Tracks 03 (P2), 06 (P1–2), 05 (P1–2), 07 (P1–2)**

Build the app that everything else hangs off ([Capstone 1](tracks/10-capstones.md)).
Containerize it. Understand the network underneath it. Learn to debug it properly.

> **Gate:** [Capstone 1](tracks/10-capstones.md) is running with metrics, logs, and traces,
> and you can explain every packet between your browser and it.

### Block 3 — Depth
**Tracks 04 (P0–2), 03 (P3), 01 (P3–4), 02 (P3)**

The heavy block. OSTEP and xv6 in parallel with Postgres internals and indexing. These two
reinforce each other constantly — page caches, WAL, and fsync are the same ideas at
different layers. **This is where the level change actually happens.**

> **Gate:** you built a shell, you finished the xv6 syscall and page-table labs, and you can
> read any `EXPLAIN ANALYZE` plan and say what's wrong with it.

### Block 4 — Distributed
**Tracks 09 (P1–2), 04 (P3), 05 (P3), 06 (P3)**

DDIA Parts I and II, with Raft. Kubernetes. TLS and DNS properly. Everything gets bigger
than one machine.

> **Gate:** DDIA Ch. 1–9 read and summarized, Raft leader election and log replication
> working, and your app running on a real cluster with zero-downtime deploys.

### Block 5 — Scale
**Tracks 09 (P3–4), 03 (P4), 06 (P4), 07 (P3–4)**

Streaming, Spark, Timescale, sharding, CDC, system design. Observability in production.

> **Gate:** [Capstone 4](tracks/10-capstones.md) running end to end, and 6 system designs
> written up with failure modes.

### Block 6 — Peak
**Tracks 10, 08 (P4), and the Phase 4 drills everywhere**

Finish the capstones. Interview conditions. Teach it. All the 3AM drills, repeatedly, until
triage is reflex.

> **Gate:** the exit criteria at the bottom of this file.

---

## The rep scheme

Four kinds of item appear in the tracks. They're weighted differently on purpose.

| Marker | Means | Done when |
|---|---|---|
| plain checkbox | learn it | you can explain it without notes |
| **Rep:** | build/measure it | the artifact is committed in `work/` |
| **Drill:** | break it and fix it | you caused it, diagnosed it, and wrote it up |
| **Capstone:** | integrate it | it works, you broke it, and the writeup exists |

**The two rules that make this work:**

- **You must break things on purpose.** Roughly a third of the reps here are "cause this
  failure deliberately." This is the actual differentiator. Reading about transaction ID
  wraparound teaches you nothing; causing it once means you'll recognize it in a log line
  at 3AM three years from now.
- **Measure before and after.** "I optimized it" is worthless. "p99 went from 840ms to
  95ms, here's the flame graph and here's the line I changed" is an interview answer, a
  promotion case, and actual knowledge.

---

## Repository layout

```
winter_is_coming/
├── README.md              <- you are here: dashboard and training blocks
├── LOG.md                 <- weekly training log
├── RUNBOOK.md             <- your 3AM triage doc (built up in Track 07 Phase 4)
├── progress.py            <- reads the checkboxes, writes the table above
├── tracks/                <- the syllabus, one file per track
│   ├── 01-linux-and-toolcraft.md
│   ├── 02-git.md
│   ├── 03-sql-and-postgres.md
│   ├── 04-os-internals.md
│   ├── 05-networking.md
│   ├── 06-containers-and-deploy.md
│   ├── 07-debugging-and-observability.md
│   ├── 08-algorithms-and-dsa.md
│   ├── 09-distributed-systems-and-data.md
│   └── 10-capstones.md
├── work/                  <- everything you build, per track
│   ├── 01-linux/
│   ├── 02-git/
│   └── ...
└── notes/                 <- the writeups the tracks ask for
```

---

## Where the exercises come from

Every exercise in here is either from, or modeled on, a course that is known for being
hard in the right way. Nothing is invented for the sake of having an exercise.

| Source | Used in |
|---|---|
| **MIT 6.1810** Operating System Engineering — the xv6 labs | Track 04 |
| **MIT 6.5840 (6.824)** Distributed Systems — MapReduce, Raft, sharded KV | Track 09 |
| **MIT 6.006 / 6.046** Algorithms | Track 08 |
| **MIT 6.NULL** The Missing Semester | Tracks 01, 02, 07 |
| **Harvard CS50** — Speller, Recover, and the memory psets | Track 04 Phase 0 |
| **Harvard CS50 SQL** | Track 03 Phase 1 |
| **Stanford CS144** Networking — build a working TCP | Track 05 |
| **CMU 15-445** Database Systems (Pavlo) — BusTub projects | Tracks 03, 10 |
| **Wisconsin OSTEP** — *Three Easy Pieces* + its simulators | Track 04 |
| **pgexercises.com** | Track 03 |
| **Fly.io Gossip Glomers** | Track 09 |
| **Jepsen** reports and public postmortems | Tracks 07, 09 |
| **Google SRE Book**, **AWS Builders' Library** | Tracks 06, 07 |

Everything listed is free except the books (DDIA, which you own; OSTEP and Pro Git are free
online; Agans' *Debugging* is cheap and short).

---

## What "FAANG-level" actually means here

Not a job title — a set of capabilities. You're done when these are true:

- [ ] **You can debug anything.** Given a broken system in a domain you don't know, you have
      a method that converges. You look before you theorize.
- [ ] **You understand at least one layer below where you work.** Writing SQL? You know the
      buffer manager. Writing a service? You know the syscalls it makes.
- [ ] **You can measure.** Every performance claim you make has a number behind it, and you
      know which number to look at.
- [ ] **You design for failure.** "What happens during a partition?" is your reflex, not an
      afterthought. You state failure modes before someone asks.
- [ ] **You ship and operate.** You've run what you built, been paged by it, and fixed it.
- [ ] **You can teach it.** Three levels of audience: non-engineer, junior, peer.
- [ ] **You have proof.** Working systems in `work/`, writeups in `notes/`, and at least one
      merged PR fixing a real bug in code you don't own.

The interview is a side effect of these, not the goal. Get these and the interview is a
conversation about things you've actually done.

---

## Start here

1. `python progress.py` — see the table above populate with zeros. That's the baseline.
2. Open [Track 01](tracks/01-linux-and-toolcraft.md), Phase 1, Set 1.1.
3. Set up WSL2 and a throwaway cloud VM.
4. Do one rep.
5. Come back tomorrow.

> The winter arc isn't about intensity. It's about still being here in March.
