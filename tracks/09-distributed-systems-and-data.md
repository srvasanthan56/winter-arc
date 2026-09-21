# Track 09 — Distributed Systems & Data Engineering (DDIA, end to end)

> **Muscle group:** back. The one that ties every other group together and that nobody sees you train.
> **Prereqs:** Track 03 Phase 1–3, Track 04 Phase 2, Track 05 Phase 1–2. **Do not start this track early.** DDIA read without Postgres and TCP underneath it is just vocabulary.
> **Book:** *Designing Data-Intensive Applications* — Martin Kleppmann. You own it. All 12 chapters, in order.

## Why this track

This is the track that makes you a senior engineer rather than a good one. It's the
difference between "we'll add a queue" and "here's the failure mode that introduces, here's
what our consistency guarantee becomes, and here's what the client will observe during a
partition."

**How to read DDIA:** one chapter per sitting, then write a one-page summary *from memory*
before re-skimming. Every chapter gets a corresponding hands-on rep below — DDIA is a book
that turns into vocabulary if you only read it. The reps are what make it stick.

## Equipment

| Resource | Use it for |
|---|---|
| **DDIA** — Kleppmann | The spine of this track |
| **MIT 6.5840 (formerly 6.824) Distributed Systems** (pdos.csail.mit.edu/6.824) — free video lectures, papers, labs | The labs. Raft in Go. Best distributed systems course available. |
| **Distributed Systems** — Martin Kleppmann's Cambridge lecture series (YouTube, free) | Excellent companion to DDIA |
| **The Raft paper** (*In Search of an Understandable Consensus Algorithm*) + **raft.github.io** visualization | Consensus |
| **Jepsen reports** (jepsen.io) | How real databases actually violate their claims |
| **The Amazon Dynamo paper** (2007) | Your DynamoDB item, at the source |
| **MapReduce, GFS, Bigtable, Spanner, Chubby papers** | 6.5840 reading list |
| **Kafka: The Definitive Guide** | Streaming |
| **Spark: The Definitive Guide** / **Learning Spark 2e** | Your Spark/RDD items |
| **AWS Builders' Library** | Practical distributed-systems engineering |
| **Fly.io Gossip Glomers** (fly.io/dist-sys) | Hands-on distributed challenges in any language |

---

## Phase 1 — Foundations of Data Systems (DDIA Part I, Ch. 1–4)

### Set 1.1 — Ch. 1: Reliable, Scalable, Maintainable
- [ ] Read Ch. 1. Summary written from memory
- [ ] Reliability: faults vs failures, hardware/software/human faults. Fault tolerance as a deliberate design property
- [ ] Scalability: describing load with **load parameters**, describing performance with **percentiles not averages**, the Twitter fan-out case study
- [ ] **Tail latency** and tail latency amplification. Head-of-line blocking at the service level
- [ ] Maintainability: operability, simplicity, evolvability
- [ ] **Rep:** take the load-parameter analysis and apply it to your own app from Track 03. What are *your* load parameters? Write `notes/my-app-load.md`

### Set 1.2 — Ch. 2: Data Models and Query Languages
- [ ] Read Ch. 2. Relational vs document vs graph. The object-relational impedance mismatch
- [ ] Schema-on-read vs schema-on-write. Locality. The document model's join problem
- [ ] Graph models: property graphs, triple stores, Cypher, SPARQL, Datalog
- [ ] **Rep:** model the *same* domain (say, a social network with posts, follows, and comments) three ways: relational in Postgres, document in MongoDB or Postgres JSONB, and graph in Neo4j or with a recursive CTE. Write the same three queries against each. Write up which model fits which query in `notes/data-models.md`

### Set 1.3 — Ch. 3: Storage and Retrieval (the chapter that pays for the book)
- [ ] Read Ch. 3
- [ ] **Log-structured storage**: append-only logs, hash indexes, **SSTables**, **LSM-trees**, memtables, compaction strategies (size-tiered vs leveled), Bloom filters in the read path
- [ ] **B-trees**: pages, write-ahead log, and the comparison with LSM-trees — **write amplification vs read amplification**, compaction pauses, predictable latency
- [ ] **Rep:** you implemented an LSM-tree and a B+ tree in Track 08 Set 1.2. Benchmark them against each other: write-heavy workload, then read-heavy, then mixed. **Now you can defend "why RocksDB for this and Postgres for that" from measurement rather than blog posts**
- [ ] OLTP vs OLAP. Data warehouses, star and snowflake schemas
- [ ] **Column-oriented storage**: why analytics wants columns, column compression (bitmap, run-length), vectorized processing, sort orders
- [ ] **Rep:** load the same 50M-row dataset into Postgres (row store) and DuckDB or ClickHouse (column store). Run an analytical aggregate over 3 columns on both. The ratio will be 10–100x. Then run a single-row point lookup on both and watch it invert. Document in `notes/row-vs-column.md`
- [ ] Materialized views and data cubes → connect to Track 03 Set 2.1

### Set 1.4 — Ch. 4: Encoding and Evolution
- [ ] Read Ch. 4. Language-specific serialization and why it's a trap
- [ ] JSON, XML, CSV and their problems (numbers, binary, schema)
- [ ] Binary formats: **Thrift, Protocol Buffers, Avro**. Field tags, schema evolution rules
- [ ] **Backward vs forward compatibility** — define both precisely. This is a rolling-deploy requirement, not a theoretical concern
- [ ] Dataflow modes: through databases, through services (REST/RPC/gRPC), through async messages
- [ ] **Rep:** define a protobuf schema, generate code, serialize a message. Then evolve the schema (add a field, remove a field, rename, change a type) and test each change for backward and forward compatibility. Record which changes are safe in `notes/schema-evolution.md`. Then do the same in Avro and note how the schema-registry model differs
- [ ] **Rep:** connect this to your Alembic migrations (Track 03 Set 2.3). A rolling deploy means **old code and new schema must coexist**. Write the expand/migrate/contract procedure down properly

---

## Phase 2 — Distributed Data (DDIA Part II, Ch. 5–9) — the core

### Set 2.1 — Ch. 5: Replication
- [ ] Read Ch. 5
- [ ] **Single-leader replication**: sync vs async vs semi-sync, setting up new followers, failover, and the ways failover goes wrong (**split brain**, lost writes, wrong timeout)
- [ ] Replication log implementations: statement-based (and its nondeterminism problems), WAL shipping, logical/row-based, trigger-based — **you already saw all four in Track 03 Set 4.3**
- [ ] **Replication lag problems, and the three guarantees that fix them:**
  - [ ] **Read-your-own-writes** (read-after-write consistency)
  - [ ] **Monotonic reads** (never go backwards in time)
  - [ ] **Consistent prefix reads** (causality preserved)
- [ ] **Rep:** on your Postgres primary+replica from Track 03, *reproduce* all three anomalies deliberately. Then implement a fix for read-your-own-writes in your app (route recent writers to the primary, or use LSN-based read tokens with `pg_wal_lsn_diff`). This is one of the most practically useful exercises in the whole program
- [ ] **Multi-leader replication**: use cases (multi-datacenter, offline clients, collaborative editing), and the write-conflict problem
- [ ] Conflict resolution: LWW (and why it loses data), version vectors, application-level merge, **CRDTs**, operational transformation
- [ ] **Leaderless replication** (Dynamo-style): quorums (**W + R > N**), sloppy quorums, hinted handoff, read repair, anti-entropy with Merkle trees
- [ ] **Rep:** work the quorum math. For N=3, what does W=1,R=1 give you? W=2,R=2? W=3,R=1? Build a table of the guarantees and the failure tolerance for each in `notes/quorums.md`. Then explain why **even W+R>N doesn't give you strong consistency** (concurrent writes, sloppy quorums, partial write failure)
- [ ] Detecting concurrent writes: **version vectors** and the "happens-before" relation
- [ ] **Rep:** implement version vectors in ~50 lines and use them to detect a concurrent update between two simulated replicas

### Set 2.2 — Ch. 6: Partitioning (you said "sharding, read it first")
- [ ] Read Ch. 6
- [ ] Partitioning by key range vs by hash of key. The tradeoff: range queries vs hotspot avoidance
- [ ] **Skewed workloads and hot spots.** The celebrity problem, and the key-salting fix
- [ ] **Secondary indexes**: local (document-partitioned, scatter/gather reads) vs global (term-partitioned, expensive writes). **Know which one each real system uses and why**
- [ ] Rebalancing: fixed number of partitions, dynamic partitioning, partition-per-node. **Why mod-N hashing is wrong** and what consistent hashing actually solves (and its limits)
- [ ] Request routing: the three approaches (client-aware, routing tier, any-node forwarding). ZooKeeper's role
- [ ] **Rep:** you set up Citus in Track 03 Set 4.6. Now deliberately create a hot shard (a tenant with 80% of the data). Observe it. Fix it. Document in `notes/hotspot.md`
- [ ] **Rep:** implement consistent hashing with virtual nodes (Track 08 Set 3.2). Then measure key redistribution when you add a node — compare against mod-N. The numbers make the argument

### Set 2.3 — Ch. 7: Transactions
- [ ] Read Ch. 7. **You did the isolation-level lab in Track 03 Set 3.3 — re-read that lab notebook alongside this chapter.** The combination is what makes it permanent
- [ ] ACID revisited, and why "ACID" is nearly meaningless as a marketing term. BASE
- [ ] Single-object vs multi-object operations. Why "we don't need transactions, we use a document DB" is usually wrong
- [ ] The weak isolation levels and exactly what each permits: Read Committed, Snapshot Isolation / Repeatable Read, and the anomalies
- [ ] Preventing lost updates: atomic operations, explicit locking, automatic detection, compare-and-set
- [ ] **Write skew and phantoms** — the subtle one. The doctors-on-call example. Materializing conflicts
- [ ] **Serializability**: actual serial execution (VoltDB/Redis), **2PL** (and its performance/deadlock cost), **SSI** (serializable snapshot isolation — optimistic, what Postgres uses)
- [ ] **Rep:** implement the doctors-on-call write skew in your app. Fix it four ways — `SELECT FOR UPDATE`, `SERIALIZABLE` + retry, a unique constraint that materializes the conflict, and an advisory lock. Compare throughput of all four under concurrency. Write up in `notes/write-skew-fixes.md`

### Set 2.4 — Ch. 8: The Trouble with Distributed Systems
- [ ] Read Ch. 8. **This is the chapter that changes how you think.** Take your time
- [ ] **Partial failure** and why it's categorically different from a single machine
- [ ] Unreliable networks: timeouts, and the fundamental problem that **you cannot distinguish a slow node from a dead node**. Sit with that
- [ ] Network congestion, queueing delay, and why timeouts must be adaptive
- [ ] **Unreliable clocks**: time-of-day vs monotonic clocks, NTP, clock skew, leap seconds
- [ ] **Why you must never use wall-clock timestamps for ordering events across machines.** LWW conflict resolution depends on exactly this and is therefore broken. Spanner's TrueTime and its uncertainty interval as the exception that proves the rule
- [ ] **Rep:** demonstrate clock skew causing wrong data. Two "nodes" with clocks 500ms apart doing LWW on the same key. Show the older write winning
- [ ] Process pauses: GC pauses, VM live migration, swap thrashing, `SIGSTOP`. **A process can be paused for seconds after it checked that it was still the leader** — this is the fencing token argument
- [ ] **Fencing tokens** — the correct fix for the "zombie leader still holding a stale lock" problem. Understand why a lock alone is insufficient
- [ ] The truth is defined by the majority. Byzantine faults (and why you usually don't need to handle them)
- [ ] System models: synchronous / partially synchronous / asynchronous; crash-stop / crash-recovery / Byzantine. Safety vs liveness
- [ ] **Rep:** write `notes/eight-fallacies.md` — the 8 fallacies of distributed computing, each with a specific bug from your own experience or reading that it caused

### Set 2.5 — Ch. 9: Consistency and Consensus
- [ ] Read Ch. 9
- [ ] **Linearizability** — define it precisely (recency guarantee, the appearance of a single copy). What it is *not*: not serializability. **Know the difference cold; it's a classic interview discriminator**
- [ ] Where linearizability is required: leader election, uniqueness constraints, cross-channel dependencies
- [ ] The cost: **CAP properly stated** (during a network *partition*, choose consistency or availability — not "pick 2 of 3", which is the sloppy version everyone repeats). **PACELC** as the better framing
- [ ] **Ordering guarantees**: total order, causal order, and the fact that causality is a *partial* order
- [ ] **Lamport timestamps** vs **vector clocks** — what each can and can't tell you
- [ ] **Rep:** implement Lamport timestamps and vector clocks for 3 simulated nodes. Demonstrate a case where Lamport timestamps give a total order that *violates* your intuition about causality, and vector clocks correctly report concurrency
- [ ] Total order broadcast, and its equivalence to consensus
- [ ] **Two-phase commit (2PC)** — the coordinator, the prepare phase, and the **blocking problem when the coordinator dies holding locks**. Why 2PC has a bad reputation. XA transactions
- [ ] **Consensus**: FLP impossibility (and why it doesn't mean consensus is impossible in practice), Paxos, **Raft**, Zab, Viewstamped Replication
- [ ] **Rep:** read the **Raft paper**. Then play with **raft.github.io's visualization** until leader election, log replication, and split-vote behavior are intuitive
- [ ] Membership and coordination services: ZooKeeper, etcd. What they're actually used for (locks, leader election, service discovery, config) and why you should use one rather than build one
- [ ] **Rep:** use etcd (or ZooKeeper) to implement correct leader election with a lease and a **fencing token**. Then kill the leader with `SIGSTOP`, let another take over, resume the old one, and prove the fencing token protects you. **This exercise is the whole chapter in code**

### Set 2.6 — MIT 6.5840 labs (the real strength work)
- [ ] Set up Go if you don't have it. Watch 6.5840 Lectures 1–8
- [ ] **Lab 1: MapReduce** — build a working MapReduce with a coordinator and workers, handling worker failure
- [ ] **Lab 2: Key/Value server** — linearizability with duplicate-request detection on an unreliable network
- [ ] **Lab 3A: Raft — leader election**
- [ ] **Lab 3B: Raft — log replication**
- [ ] **Lab 3C: Raft — persistence and crash recovery**
- [ ] **Lab 3D: Raft — log compaction / snapshots**
- [ ] **Lab 4: Fault-tolerant KV service on top of your Raft**
- [ ] **Lab 5: Sharded KV with configuration changes** (the hardest one — shard migration without losing linearizability)
- [ ] **Honest note:** implementing Raft correctly is one of the hardest things in this entire program and will take weeks. It is also the single strongest signal on a resume that you actually understand distributed systems. Getting through 3A–3C alone puts you ahead of most engineers
- [ ] **Alternative/warm-up:** **Fly.io Gossip Glomers** — 6 challenges (echo, unique IDs, broadcast, counter, kafka-log, txn) in any language. Do these first if Raft feels too steep

---

## Phase 3 — Derived Data (DDIA Part III, Ch. 10–12) + data engineering

### Set 3.1 — Ch. 10: Batch Processing
- [ ] Read Ch. 10
- [ ] The Unix philosophy as the origin story — **this is Track 01's pipes, at cluster scale**
- [ ] MapReduce: the model, the shuffle, reduce-side joins vs **map-side joins** (broadcast hash join, partitioned hash join, merge join). **These are the same joins as Track 03 Set 3.2** — note that
- [ ] Handling skew in joins. Materialization of intermediate state vs dataflow engines
- [ ] Dataflow engines (Spark, Flink, Tez), graph processing (Pregel model), high-level APIs
- [ ] Read the **MapReduce** and **GFS** papers

### Set 3.2 — Ch. 11: Stream Processing
- [ ] Read Ch. 11
- [ ] Events and streams. Messaging systems: direct, message brokers, **log-based brokers**. The crucial difference between a **queue** (message deleted on ack) and a **log** (offset-based, replayable)
- [ ] **Kafka**: topics, partitions, offsets, consumer groups, rebalancing, replication and ISR, retention, compaction, exactly-once semantics
- [ ] **Rep:** run Kafka (or Redpanda) in Docker. Produce and consume. Then: add a second consumer in the same group and watch rebalancing. Kill a consumer mid-stream and observe redelivery from the last committed offset. Reset offsets and replay history
- [ ] **Change Data Capture** — you already built this with Debezium off the Postgres WAL in Track 03 Set 4.5. **Re-read that work now, with Ch. 11's framing of "the database as a stream."** The insight — that a replication log and an event log are the same thing — is the payoff for doing the tracks in this order
- [ ] **Event sourcing** and CQRS. Commands vs events. Deriving current state by folding the log
- [ ] Time in streams: event time vs processing time, **windowing** (tumbling, hopping, sliding, session), **watermarks**, handling late events
- [ ] Stream joins: stream-stream, stream-table, table-table. The state they require
- [ ] Fault tolerance: microbatching, checkpointing, idempotence, and rebuilding state after failure
- [ ] **Rep:** build a streaming pipeline: producer → Kafka → a stream processor (Flink, Kafka Streams, or Spark Structured Streaming) → a sink. It must do a windowed aggregation, tolerate the processor being killed and restarted, and produce correct results. Then deliberately send late events and observe the watermark behavior

### Set 3.3 — Spark, RDDs, and window operations (your listed items)
- [ ] **RDD** — the paper's actual idea: an immutable, partitioned, **lineage-tracked** distributed collection. Why lineage means you don't need replication for fault tolerance. Read the RDD paper (*Resilient Distributed Datasets*, NSDI 2012)
- [ ] **Transformations vs actions**, lazy evaluation, the DAG
- [ ] **Narrow vs wide dependencies** — and why wide dependencies (shuffles) define stage boundaries. **This is the single most important Spark performance concept**
- [ ] `persist`/`cache`, storage levels, and when caching hurts
- [ ] RDD → DataFrame → Dataset. **Catalyst** optimizer and **Tungsten** execution. Why DataFrames beat RDDs (the optimizer can see into them; with an RDD lambda it cannot)
- [ ] **Rep:** write the same job as an RDD job and a DataFrame job. Compare `explain()` output and runtime. Then explain why the DataFrame version won
- [ ] Partitioning, `repartition` vs `coalesce`, partition sizing, `spark.sql.shuffle.partitions`
- [ ] Joins in Spark: broadcast hash join, sort-merge join, shuffle hash join. Broadcast thresholds and hints. **Adaptive Query Execution** (AQE) and dynamic skew handling
- [ ] **Spark window operations** (your listed item): `Window.partitionBy().orderBy()`, `rowsBetween`/`rangeBetween`, `row_number`, `rank`, `lag`/`lead`
- [ ] **Rep:** take the 6 window-function queries you wrote in Postgres (Track 03 Set 1.5) and port every one to Spark. Write `notes/sql-vs-spark-windows.md` covering: API differences, where the frame semantics differ, and the crucial operational difference — **a window without `partitionBy` collapses all data to one executor.** Understanding *why* that happens is the point of the exercise
- [ ] Spark SQL, UDFs (and why Python UDFs are slow — serialization across the JVM/Python boundary), **pandas UDFs / Arrow**
- [ ] Structured Streaming: micro-batch vs continuous, output modes, watermarks, stateful operations
- [ ] Delta Lake / Iceberg / Hudi — ACID on object storage, time travel, schema evolution, the lakehouse idea
- [ ] **Rep:** you built the cluster in Track 06 Set 4.3. Now run a real job on it: read a large dataset, do a skewed join and a windowed aggregation, and tune it using the Spark UI until you've halved the runtime. Document every change and its effect

### Set 3.4 — Ch. 12: The Future of Data Systems
- [ ] Read Ch. 12
- [ ] Data integration: combining specialized tools, the "unbundled database," derived data vs system of record
- [ ] Lambda vs Kappa architecture
- [ ] End-to-end argument: **exactly-once is a fiction without idempotence at the endpoint**. Idempotency keys again (Track 05 Set 4.2)
- [ ] Enforcing constraints in a distributed system without a coordinator: uniqueness via partitioning by the constrained key, and compensating transactions / **sagas**
- [ ] Timeliness vs integrity. Auditability, and designing for the fact that the data *will* be wrong sometimes
- [ ] Ethics of data systems (Kleppmann's section — read it, it's short and it matters)

---

## Phase 4 — Peak (the specific systems you named + system design)

### Set 4.1 — DynamoDB and the Dynamo lineage (your listed item)
- [ ] Read the original **Amazon Dynamo paper** (2007). Note: **DynamoDB the product is not the Dynamo paper** — it's leaderless-inspired but is actually a single-leader replicated, strongly-consistent-capable managed service. Know the difference; this catches people out
- [ ] The Dynamo techniques: consistent hashing, vector clocks, quorums, hinted handoff, Merkle-tree anti-entropy, gossip membership. **You have now implemented four of these** in Sets 2.1–2.2 and Track 08 Set 3.2
- [ ] DynamoDB data modeling: **partition key + sort key**, and the fact that **single-table design** is the idiomatic pattern. Why that feels so wrong after Track 03 and why it's right here
- [ ] Access patterns *first*, schema second — the exact inversion of relational design
- [ ] GSIs and LSIs, their consistency guarantees, and their cost
- [ ] Capacity: on-demand vs provisioned, RCU/WCU math, hot partitions, adaptive capacity
- [ ] Eventually consistent vs strongly consistent reads, transactions (`TransactWriteItems`), conditional writes for optimistic concurrency
- [ ] DynamoDB Streams → Lambda. (Same pattern as CDC again)
- [ ] **Rep:** take the schema you built in Postgres (Track 03 Set 2.3) and redesign it for DynamoDB single-table. Write down the access patterns first. Then implement it with DynamoDB Local and run both. Write `notes/relational-vs-dynamo.md` on what you gained and what you gave up
- [ ] Read Alex DeBrie's *The DynamoDB Book* summary material, or Rick Houlihan's re:Invent talk
- [ ] Compare the family: Cassandra (Dynamo-style, wide column), MongoDB (document, single-leader), Redis (in-memory), Spanner (globally distributed, TrueTime, externally consistent). For each: what problem was it built for?

### Set 4.2 — Collaborative editing, offline-first, and IndexedDB (your Google Docs item)
- [ ] The problem statement: multiple users, concurrent edits, offline capability, eventual convergence, intention preservation
- [ ] **Operational Transformation (OT)** — the classic approach. What Google Docs actually uses. Transform functions, the central server requirement, and why OT is notoriously hard to get right
- [ ] **CRDTs** — Conflict-free Replicated Data Types. State-based (CvRDT) vs operation-based (CmRDT). The lattice/monotonic-merge idea
- [ ] The CRDT zoo: G-Counter, PN-Counter, G-Set, 2P-Set, LWW-Register, OR-Set, and **sequence CRDTs** (RGA, Logoot, **YATA**) for text
- [ ] **Rep:** implement a G-Counter and an OR-Set from scratch. Merge them from three replicas in random orders and prove convergence
- [ ] **Yjs** and **Automerge** — the production CRDT libraries. Read Kleppmann's work on Automerge and local-first software
- [ ] Read the **"Local-first software"** essay (Kleppmann et al.) — the seven ideals. It reframes what a "cloud app" has to be
- [ ] **IndexedDB** (your item): the browser's transactional object store. Object stores, indexes, transactions and their **auto-commit gotcha** (transactions die if you await something non-IDB inside them), versioning and `onupgradeneeded`, cursors
- [ ] Why IndexedDB and not localStorage: async, structured, indexed, large quota, transactional. Storage quotas and eviction
- [ ] The offline sync problem: local writes queued, conflict on reconnect, tombstones for deletes, sync protocols
- [ ] **Rep (capstone for this set):** build a **collaborative notes app**. Two browser tabs editing the same document. Yjs (or your own CRDT) for the document state, IndexedDB for local persistence, a WebSocket server for sync. Requirements: go offline, edit in both tabs, come back online, and converge correctly. Then kill the server mid-edit and recover
- [ ] **Rep:** write `notes/ot-vs-crdt.md` — the honest comparison, including why Google chose OT and why new systems mostly choose CRDTs

### Set 4.3 — Caching and the rest of the toolkit
- [ ] Cache strategies: cache-aside, read-through, write-through, write-behind, refresh-ahead
- [ ] Invalidation: TTL, explicit, event-driven. **"There are only two hard things..."** — understand exactly why it's hard
- [ ] **Cache stampede / thundering herd** and the fixes: locking, probabilistic early expiration, stale-while-revalidate
- [ ] Redis: data structures (strings, hashes, lists, sets, sorted sets, streams, HyperLogLog), persistence (RDB vs AOF), eviction policies, pipelining, Lua scripts, pub/sub, Redis Cluster
- [ ] **Rep:** add Redis caching to your app. Measure the hit rate and the latency improvement. Then deliberately cause a cache stampede under load and fix it. Then introduce a cache-invalidation bug (stale data after a write) and design the fix properly
- [ ] Distributed locks with Redis, **and read Kleppmann's critique of Redlock**. Then re-read the fencing token section (Set 2.4). This debate is a masterclass in distributed-systems reasoning
- [ ] API gateways, service meshes, service discovery
- [ ] Message queues beyond Kafka: RabbitMQ, SQS, NATS. Delivery semantics (at-most-once, at-least-once, effectively-once) and **why at-least-once + idempotent consumers is the standard practical answer**

### Set 4.4 — System design
- [ ] Study the framework: requirements (functional + non-functional) → capacity estimation → API design → data model → high-level design → deep dive on 1–2 components → bottlenecks and tradeoffs
- [ ] **Back-of-the-envelope estimation** — memorize the orders of magnitude: QPS, storage per row, bytes on the wire, latency numbers, what one machine can do
- [ ] Resources: **System Design Interview** (Alex Xu) vols 1–2, **ByteByteGo**, **github.com/donnemartin/system-design-primer**, and **Jordan Has No Life** on YouTube for depth
- [ ] **Read real engineering blogs** — Netflix, Uber, Stripe, Discord, Figma, Cloudflare. Discord's "how we store trillions of messages" and Figma's sharding post are particularly good
- [ ] **Rep:** design and write up 12 systems. For each: 2 pages, a diagram, explicit tradeoffs, and a named failure mode with its mitigation. Files in `work/09-distributed/designs/`:
  - [ ] URL shortener (start here — it's the "hello world" and it's still full of real decisions)
  - [ ] Rate limiter (distributed, with the four algorithms from Track 08 Set 3.2)
  - [ ] Twitter/news feed (fan-out on write vs read, and the celebrity problem — DDIA Ch. 1 again)
  - [ ] Chat system (WebSockets, presence, ordering, delivery receipts, offline)
  - [ ] Distributed ID generator (Snowflake, and the clock-skew problem from Ch. 8 — and UUIDv7 from Track 03)
  - [ ] Web crawler (politeness, dedup with Bloom filters, frontier prioritization)
  - [ ] Notification system (multi-channel, retries, idempotency, dedup)
  - [ ] Search autocomplete (tries, ranking, updating)
  - [ ] Payment system (idempotency, exactly-once as a business requirement, reconciliation, ledgers, sagas)
  - [ ] Google Docs (your item — OT/CRDT, from Set 4.2)
  - [ ] Metrics/monitoring system (time-series storage — this is Track 03's TimescaleDB work)
  - [ ] Distributed job scheduler (leader election, at-least-once execution, fencing)
- [ ] **Rep:** do 5 mock system design interviews, spoken aloud, 45 minutes each
- [ ] **The habit that matters most:** for every design, state the **tradeoff** and the **failure mode**. A design without a stated failure mode reads as junior, no matter how good the diagram is

### Set 4.5 — Learn from real failures
- [ ] Read 10 **Jepsen** reports. Notice the pattern: almost every system has violated its own advertised guarantee at some point
- [ ] Read 10 public **postmortems** (github.com/danluu/post-mortems is a good index)
- [ ] Read Dan Luu's blog broadly — particularly the posts on hardware failure rates and "normalization of deviance"
- [ ] **Rep:** write `notes/failure-patterns.md` — the recurring root causes you noticed across all 20. (You'll find: retry storms, cascading failure, config changes, capacity cliffs, and a *lot* of DNS)

---

## Exit criteria for Track 09

- [ ] All 12 DDIA chapters read, each with a written-from-memory summary
- [ ] Raft implemented and passing at least 6.5840 labs 3A–3C (or Gossip Glomers complete)
- [ ] You can explain linearizability vs serializability without hesitating
- [ ] You built something with a CRDT and something with Kafka, and both survive a restart
- [ ] 12 system designs written up, each with tradeoffs and failure modes
- [ ] You instinctively ask "what happens during a partition?" about every design you see
