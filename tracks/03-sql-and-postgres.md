# Track 03 — SQL & PostgreSQL (from `SELECT` to the buffer manager)

> **Muscle group:** legs. The biggest, most load-bearing track in the program. Most engineers skip it. That's exactly why it separates people.
> **Prereqs:** Track 01 Phase 1 (you'll live in `psql` and the shell).
> **Runs alongside:** Track 09 (DDIA) from Phase 3 onward.

## Why this track

Your original ladder was already right. I've kept its shape and filled in the rungs:

```
Relational model → SQL → Postgres tutorial → Build an app → Indexes
   → EXPLAIN/planner → Transactions/MVCC → Internals → Storage/WAL/buffers
      → Distributed data (Track 09)
```

The rule that makes this track work: **never learn a Postgres feature without a table big
enough to feel it.** A 100-row table teaches you nothing about indexes. Everything below
assumes you're working against millions of rows.

## Equipment

| Resource | Use it for |
|---|---|
| **PostgreSQL official docs** (postgresql.org/docs/current) | The primary text. Genuinely one of the best-written manuals in software. |
| **pgexercises.com** | Phase 1–2 drills, every section |
| **Harvard CS50 SQL** | Structured intro if you want lectures, includes good psets |
| **CMU 15-445 / 15-721** — Andy Pavlo (YouTube, free) | Phase 3–4. The best database systems course that exists. |
| **The Internals of PostgreSQL** — Hironobu Suzuki (interdb.jp/pg) | Phase 4. Free, illustrated, definitive. |
| **PostgreSQL 14 Internals** — Egor Rogov (free PDF, Postgres Pro) | Phase 4. Deeper than Suzuki. |
| **Use The Index, Luke** — Markus Winand | Indexing, top to bottom |
| **DDIA** Ch. 2, 3, 7 | Concepts behind the mechanics — see Track 09 |
| `pgbench`, `pg_stat_statements`, `auto_explain`, `pgtune` | Your measuring instruments |

**Lab setup (do this first):**
- [ ] Postgres 16+ running locally in Docker, with a persistent volume
- [ ] `psql` configured: `~/.psqlrc` with `\timing on`, `\x auto`, `\set HISTSIZE 5000`
- [ ] A GUI for exploring (DBeaver or pgAdmin) — but **psql is your primary tool**
- [ ] Load a real dataset with real volume. Pick two: **Pagila** (DVD rental), **pgexercises' clubdata**, **NYC Taxi trips** (~100M rows), **Stack Overflow dump**, or **IMDb datasets**
- [ ] `pg_stat_statements` enabled in `postgresql.conf`

---

## Phase 1 — Foundation (the relational model + SQL that actually works)

### Set 1.1 — Relational model first, syntax second
- [ ] What a relation actually is: tuples, attributes, domains, and why order doesn't matter
- [ ] Keys: candidate, primary, foreign, surrogate vs natural. Composite keys
- [ ] Normalization 1NF → 2NF → 3NF → BCNF. Be able to normalize a messy spreadsheet on paper
- [ ] Denormalization: when and why you deliberately break the rules
- [ ] Relational algebra basics: selection (σ), projection (π), join (⋈), union, difference. This is what the planner actually manipulates
- [ ] **Rep:** take a real-world domain (an order system, a ticketing system) and design the schema on paper to 3NF. Then write the DDL. Save to `work/03-postgres/schema-design/`
- [ ] Read **DDIA Chapter 2** (Data Models) — relational vs document vs graph

### Set 1.2 — The SQL language (Postgres docs Ch. 4, "SQL Syntax")
- [ ] `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`/`OFFSET`, `DISTINCT`, `DISTINCT ON` (a Postgres gift)
- [ ] **Logical order of evaluation**: FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT. Memorize this. It explains why you can't use a SELECT alias in WHERE
- [ ] Joins: INNER, LEFT, RIGHT, FULL, CROSS, and `LATERAL` (the one most people never learn — learn it)
- [ ] Self-joins, anti-joins (`NOT EXISTS`), semi-joins (`EXISTS`)
- [ ] `NULL` semantics: three-valued logic. Why `NULL = NULL` is NULL, `NOT IN` with NULLs silently returns nothing, `COALESCE`, `NULLIF`, `IS DISTINCT FROM`
- [ ] **Rep:** write a query that returns the wrong answer because of a `NOT IN (subquery with NULL)`. Fix it with `NOT EXISTS`. Document in `notes/null-traps.md`
- [ ] Aggregates: `COUNT(*)` vs `COUNT(col)`, `SUM`, `AVG`, `MIN/MAX`, `STRING_AGG`, `ARRAY_AGG`, `FILTER (WHERE ...)`
- [ ] `GROUP BY`, `HAVING`, `GROUPING SETS`, `ROLLUP`, `CUBE`
- [ ] Set ops: `UNION` vs `UNION ALL` (know the performance difference), `INTERSECT`, `EXCEPT`
- [ ] Subqueries: scalar, correlated, `IN`, `ANY`/`ALL`, and when the planner flattens them

### Set 1.3 — Drills
- [ ] **pgexercises.com**: Basic + Joins and Subqueries sections, all questions, no peeking
- [ ] **pgexercises.com**: Modifying Data, Aggregates sections
- [ ] **pgexercises.com**: String and Date sections
- [ ] **Rep:** 30 queries against your large dataset, written from business questions, not from schema. E.g. "which customers rented more in the second half of the year than the first?"
- [ ] Optional: SQL Murder Mystery, Advent of SQL, or LeetCode Database (top 50)

### Set 1.4 — Your specific asks, done properly
- [ ] **`generate_series`** — series of ints, timestamps, and its killer use: generating a calendar table to left-join against so gaps in data show as zeros instead of vanishing
- [ ] **Rep:** produce a daily-count report with no missing days, using `generate_series` + `LEFT JOIN`
- [ ] **Dates and times, done right**: `date` vs `timestamp` vs `timestamptz`. Why **`timestamptz` is almost always correct** and `timestamp` is a bug waiting to happen
- [ ] `AT TIME ZONE` (it works in both directions — understand both), `date_trunc`, `extract`, `age`, `interval` arithmetic, `tstzrange` and range types
- [ ] **Rep:** write `notes/timezones.md` explaining what Postgres actually stores for a `timestamptz` (hint: it does not store the zone) and how a "report by local day per user" query must be written
- [ ] **`WITH RECURSIVE`** — the mental model: anchor term UNION ALL recursive term
- [ ] **Rep:** recursive CTE #1 — walk an org chart / category tree to arbitrary depth, with a `path` array and `depth` column
- [ ] **Rep:** recursive CTE #2 — find connected components / shortest path in a graph stored in a table, with cycle detection using the path array
- [ ] **Rep:** recursive CTE #3 — bill of materials explosion (parts containing parts)
- [ ] `CYCLE` and `SEARCH` clauses (SQL:99 features Postgres 14+ supports)
- [ ] Non-recursive CTEs, and the **materialization change in PG12** (`MATERIALIZED` / `NOT MATERIALIZED`) — know why old advice about "CTEs are optimization fences" is now wrong

### Set 1.5 — Window functions (the highest-leverage SQL skill)
- [ ] `OVER (PARTITION BY ... ORDER BY ...)` — the mental model vs `GROUP BY`
- [ ] Ranking: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK`
- [ ] Offset: `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE`
- [ ] **Frames**: `ROWS` vs `RANGE` vs `GROUPS`, `UNBOUNDED PRECEDING`, `CURRENT ROW`. Know why `LAST_VALUE` returns the "wrong" thing with the default frame
- [ ] Running totals, moving averages, period-over-period deltas, gaps-and-islands
- [ ] **Rep:** solve the classic **gaps and islands** problem (find consecutive runs) with window functions
- [ ] **Rep:** top-N-per-group three ways: window function, `LATERAL`, and `DISTINCT ON`. `EXPLAIN ANALYZE` all three and write down which wins and why
- [ ] **Cross-link:** you'll redo these exact operations in Spark in Track 09 — note the API differences

---

## Phase 2 — Volume (schema, types, and building something real)

### Set 2.1 — Data Definition (Postgres docs Ch. 5)
- [ ] `CREATE TABLE`, column constraints vs table constraints
- [ ] Constraints: `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `CHECK`, `EXCLUDE` (underrated — use it for "no overlapping bookings")
- [ ] Foreign keys and referential actions: `ON DELETE CASCADE / RESTRICT / SET NULL / NO ACTION`. Know that FKs need indexes on the *referencing* side or your deletes will crawl
- [ ] `DEFAULT`, generated columns (`GENERATED ALWAYS AS ... STORED`), identity columns
- [ ] Schemas, `search_path`, and the security implications of a mutable search_path
- [ ] Table inheritance vs **declarative partitioning** (range, list, hash), partition pruning, attaching/detaching partitions
- [ ] **Rep:** partition a 50M-row time-series table by month. Measure a range query before and after. Verify pruning in `EXPLAIN`
- [ ] Views, **materialized views**, `REFRESH MATERIALIZED VIEW CONCURRENTLY` (and its unique-index requirement)
- [ ] `ALTER TABLE` and which forms take an `ACCESS EXCLUSIVE` lock and rewrite the whole table. **This is the knowledge that prevents outages** — write the safe/unsafe list into `notes/safe-migrations.md`

### Set 2.2 — Data types (Postgres docs Ch. 8) — including your UUID question
- [ ] Numeric: `int2/4/8`, `numeric` vs `float8`. **Never store money in float** — know exactly why
- [ ] Text: `text` vs `varchar(n)` vs `char(n)`. In Postgres, `text` is the default right answer. Know why `varchar(n)` gives you nothing but a constraint
- [ ] Collation, `citext`, case-insensitive comparison, and `ICU` collations
- [ ] **`SERIAL` vs `IDENTITY` vs `UUID` vs `OID`** — your question, answered in depth:
  - [ ] `SERIAL` is not a type; it's a macro for int + sequence + default. Know what it expands to
  - [ ] `GENERATED ALWAYS AS IDENTITY` is the SQL-standard replacement. Use it for new work
  - [ ] Sequences: `nextval`, `currval`, caching, and why sequences are **non-transactional** (gaps after rollback)
  - [ ] UUIDv4: random → terrible B-tree insert locality → index bloat and cache misses
  - [ ] **UUIDv7** (time-ordered, PG18 native / `pg_uuidv7` extension) — solves the locality problem. This is the modern answer
  - [ ] `OID` — the legacy system identifier, why `WITH OIDS` was removed in PG12, and where OIDs still exist (system catalogs, large objects)
  - [ ] **Rep:** benchmark it. Insert 5M rows into three tables keyed by bigint-identity, uuidv4, and uuidv7. Compare insert throughput, index size (`pg_relation_size`), and index fragmentation. Write results into `notes/id-strategies.md` with a recommendation
  - [ ] Understand the distributed-systems argument for UUIDs (client-generated IDs, no round trip, merge-friendly) — this connects to Track 09
- [ ] `JSONB` vs `JSON`: storage difference, operators (`->`, `->>`, `#>`, `@>`, `?`), `jsonb_path_query`, GIN indexing
- [ ] Know the rule: JSONB for genuinely schemaless attributes, not as an excuse to skip schema design
- [ ] Arrays, `ENUM` (and the pain of altering one), `hstore`
- [ ] Range types + `EXCLUDE` constraints for scheduling problems
- [ ] `bytea`, and why you usually shouldn't put files in the database
- [ ] Full text search: `tsvector`, `tsquery`, `to_tsvector`, ranking, GIN index, `pg_trgm` for fuzzy matching

### Set 2.3 — Build an app against it (this is the rung your ladder had, and it matters)
- [ ] Pick a real domain with nontrivial relationships. Suggestion: a **multi-tenant job board** or **event ticketing with seat reservations** (forces you into concurrency problems later)
- [ ] Build the API with **FastAPI** (ties into Track 06) using SQLAlchemy Core or asyncpg
- [ ] **Migrations with Alembic:** autogenerate, review-the-generated-file discipline, `upgrade`/`downgrade`, branching and merge heads
- [ ] **Rep:** write a migration that is *not* safely reversible, notice it, and rewrite it to be reversible
- [ ] **Rep:** write a zero-downtime column rename (expand → backfill → contract, 3 deploys). This is a real FAANG-level skill
- [ ] **Liquibase** — read enough to compare against Alembic; write 10 lines on the changelog model vs Alembic's revision chain in `notes/migration-tools.md`
- [ ] Seed the app with realistic volume (millions of rows) using `generate_series` — you need this for the rest of the track
- [ ] **Supabase** — spin up a project, understand what it is (Postgres + PostgREST + GoTrue + Realtime + Storage). Poke at row-level security
- [ ] **Row-Level Security (RLS)** — policies, `USING` vs `WITH CHECK`, and multi-tenant isolation. Implement it in your app
- [ ] **Railway / Neon / Fly.io** — deploy your app + database somewhere real. Note connection limits, pooling mode, and cold starts
- [ ] **Rep:** write `notes/hosted-postgres.md` comparing what you actually get from Supabase vs Neon vs RDS vs self-hosted

### Set 2.4 — Client, connection, and operations
- [ ] What happens on `psql "postgres://..."`: TCP connect → startup packet → auth (`scram-sha-256`) → **backend process forked** → query loop
- [ ] Understand that Postgres is **process-per-connection**, not thread-per-connection. This single fact explains pooling, `max_connections`, and memory behavior
- [ ] `pg_hba.conf` — the order-sensitive rules, `host` vs `hostssl` vs `local`, `trust` (and why it's dangerous)
- [ ] `postgresql.conf` parameters worth knowing: `shared_buffers`, `work_mem`, `maintenance_work_mem`, `effective_cache_size`, `max_connections`, `wal_level`, `checkpoint_timeout`, `random_page_cost`
- [ ] **Rep:** run `pgtune` against your box's specs and explain every parameter it changes and why
- [ ] **Connection pooling** — your listed item:
  - [ ] Why it's mandatory: fork cost + per-backend memory + `max_connections` ceiling
  - [ ] **PgBouncer** modes: `session` vs `transaction` vs `statement`. Know exactly what breaks in transaction mode (prepared statements, `SET`, advisory locks, `LISTEN/NOTIFY`, temp tables)
  - [ ] Application-side pools (SQLAlchemy `QueuePool`, HikariCP, `pgx`) vs server-side pools. Why you often need both, and how to size them
  - [ ] Pool sizing math: `connections ≈ (core_count * 2) + effective_spindle_count`. Understand why more is usually slower
  - [ ] **Rep:** load-test your app with `pgbench` or `k6` at 500 concurrent clients, first direct, then through PgBouncer in transaction mode. Graph latency and throughput. Then deliberately break something that only breaks in transaction mode, and explain it
  - [ ] **Rep (your scenario):** "multiple connection pools hitting the same data" — run two app instances with separate pools writing the same rows. Observe lock waits in `pg_locks` and `pg_stat_activity`. Then reproduce a **deadlock** between them and read the deadlock report in the log
  - [ ] Supavisor / RDS Proxy / pgcat — know they exist and what problem each adds beyond PgBouncer
- [ ] **`pg_dump` / `pg_restore` / `pg_dumpall`** — your listed item:
  - [ ] Format flags: `-Fp` plain vs `-Fc` custom vs `-Fd` directory. Why `-Fc`/`-Fd` is almost always right
  - [ ] `-j` parallel dump/restore, `--schema-only`, `--data-only`, `-t` table, `-n` schema, `--exclude-table-data`
  - [ ] `pg_dump` runs in a repeatable-read snapshot — what that means for consistency and for long-running dumps holding back vacuum
  - [ ] `pg_restore --list` + `--use-list` for selective restore
  - [ ] **`pg_basebackup`** and why it's a *different* kind of backup (physical vs logical)
  - [ ] **Point-in-time recovery (PITR)**: base backup + WAL archive + `recovery_target_time`
  - [ ] **Rep:** do a full disaster recovery drill. Take a base backup, archive WAL, `DROP TABLE` something important, then recover the database to the moment *before* the drop. Time yourself. Document in `notes/pitr-drill.md`
  - [ ] **Rep:** dump a 10GB database and restore it into a fresh instance with `-j 4`. Record the timing difference vs single-threaded
- [ ] Useful hacks worth knowing cold: `\copy` vs `COPY` (client vs server side), `COPY ... FROM PROGRAM`, `psql -c` vs `-f`, `\watch`, `\gexec`, `\timing`, `\di+`, `\dt+`, `\d+`, `pg_stat_activity` kill switches (`pg_cancel_backend`, `pg_terminate_backend`)
- [ ] **Rep:** bulk-load 10M rows three ways — row-by-row INSERT, multi-row INSERT, and `COPY`. Measure all three. The ratio will surprise you

---

## Phase 3 — Strength (make it fast, keep it correct)

### Set 3.1 — Indexes (Postgres docs Ch. 11 + Use The Index, Luke)
- [ ] **B-tree internals**: what a page looks like, why the tree is shallow, why it stays balanced
- [ ] Index scan vs **index-only scan** (and the visibility map's role) vs bitmap heap scan vs seq scan. Know when a seq scan is *correct*
- [ ] Composite indexes and the **leftmost prefix rule**. Column order is not arbitrary
- [ ] **Rep:** build `(a, b)` and `(b, a)` indexes and demonstrate with EXPLAIN which queries each one serves
- [ ] Covering indexes with `INCLUDE`
- [ ] Partial indexes (`WHERE deleted_at IS NULL`) — huge wins, underused
- [ ] Expression indexes (`ON t (lower(email))`) and why your `WHERE lower(email)=` was doing a seq scan
- [ ] Index types beyond B-tree: **GIN** (jsonb, arrays, FTS), **GiST** (geometric, ranges, nearest-neighbour), **BRIN** (huge naturally-ordered tables — perfect for time series), **Hash**, **SP-GiST**
- [ ] `CREATE INDEX CONCURRENTLY` — why it takes two table scans, why it can leave an `INVALID` index, and why you must never build an index non-concurrently on a busy production table
- [ ] Index bloat: measure it, `REINDEX CONCURRENTLY`, and what causes it
- [ ] The costs of indexes: write amplification, HOT update prevention, disk, planning time
- [ ] **Rep:** take your 5 slowest app queries, index them properly, and record before/after timings in `notes/index-results.md`. Then find and drop an index that is never used (`pg_stat_user_indexes` where `idx_scan = 0`)
- [ ] **Rep:** demonstrate a case where adding an index makes the overall workload *slower*

### Set 3.2 — EXPLAIN and the query planner
- [ ] `EXPLAIN` vs `EXPLAIN ANALYZE` vs `EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS, WAL)`. Always use BUFFERS
- [ ] Read a plan tree correctly: **inside-out, bottom-up**. `cost=start..total rows=N width=B`, `actual time=..`, `loops=N`
- [ ] **The single most important skill: comparing estimated rows vs actual rows.** A 1000x misestimate is your root cause 80% of the time
- [ ] Scan nodes: Seq Scan, Index Scan, Index Only Scan, Bitmap Index + Bitmap Heap Scan, TID Scan
- [ ] Join nodes: **Nested Loop** (small outer, indexed inner), **Hash Join** (equality, fits in work_mem), **Merge Join** (both sorted). Know the cost model for each and when the planner picks which
- [ ] Other nodes: Sort (and `Sort Method: quicksort` vs `external merge Disk` — the signal your `work_mem` is too low), Aggregate, HashAggregate, Materialize, Memoize, Gather, Incremental Sort
- [ ] Statistics: `ANALYZE`, `pg_statistic`, `pg_stats`, `default_statistics_target`, histogram bounds, MCVs, n_distinct
- [ ] **Extended statistics** (`CREATE STATISTICS`) for correlated columns — the fix for the classic "city and state are correlated" misestimate
- [ ] Cost constants: `seq_page_cost`, `random_page_cost` (why 4.0 is wrong on SSDs), `cpu_tuple_cost`, `effective_cache_size`
- [ ] Genetic query optimization (`geqo`) and what happens past `join_collapse_limit`
- [ ] **Tools:** paste plans into **explain.dalibo.com** or **explain.depesz.com**. Enable `auto_explain` with `log_min_duration`
- [ ] `pg_stat_statements` — find your true top-10 by total time, not by the query you happen to be annoyed about
- [ ] **Rep:** for each of Seq Scan / Index Scan / Bitmap Heap Scan / Nested Loop / Hash Join / Merge Join, construct a query on your dataset that produces that node. Save all 6 plans, annotated, in `notes/plan-gallery.md`
- [ ] **Rep:** find a query where the planner makes a bad choice. Fix it three ways (add an index, add statistics, rewrite the query) and compare. Then fix it the wrong way with `enable_nestloop=off` and explain why that's a bad production fix
- [ ] **Rep:** take one genuinely slow query from your app and get it 10x faster. Write the full story in `notes/query-postmortem.md`: plan before, hypothesis, change, plan after, measured result

### Set 3.3 — Transactions and ACID (Postgres docs Ch. 13)
- [ ] ACID, each letter, with a concrete Postgres mechanism for each: **A**=WAL+abort, **C**=constraints, **I**=MVCC+locks, **D**=WAL fsync at commit
- [ ] **Rep:** demonstrate each property breaking when you remove its mechanism. E.g. set `synchronous_commit=off`, kill -9 the server mid-write, and show lost-but-committed transactions. This is how ACID stops being an acronym
- [ ] `BEGIN`/`COMMIT`/`ROLLBACK`, `SAVEPOINT`, `ROLLBACK TO SAVEPOINT`, implicit transactions
- [ ] The four anomalies: **dirty read, non-repeatable read, phantom read, write skew**
- [ ] Isolation levels in Postgres: Read Committed (default), Repeatable Read (actually snapshot isolation), Serializable (SSI). Note: Postgres has **no** Read Uncommitted in practice
- [ ] **Rep — the two-terminal lab.** Open two `psql` sessions side by side. Reproduce each anomaly, then show which isolation level prevents it. Record the exact interleaving for all of these in `notes/isolation-lab.md`:
  - [ ] Non-repeatable read under Read Committed, prevented under Repeatable Read
  - [ ] Phantom read
  - [ ] **Lost update** — two sessions doing read-modify-write on the same balance
  - [ ] **Write skew** (the doctors-on-call problem) — show Repeatable Read *allows* it and Serializable rejects it with a serialization failure
  - [ ] A **deadlock** — two sessions locking two rows in opposite order. Read the server's deadlock report
- [ ] Locking: `SELECT ... FOR UPDATE`, `FOR NO KEY UPDATE`, `FOR SHARE`, `SKIP LOCKED`, `NOWAIT`
- [ ] **Rep:** implement a correct job queue in pure SQL using `FOR UPDATE SKIP LOCKED`. Run 10 concurrent workers and prove no job is processed twice
- [ ] Table-level lock modes and the conflict matrix. Which DDL blocks which DML
- [ ] Advisory locks (`pg_advisory_lock`) — application-level mutexes, and the session vs transaction variants
- [ ] `lock_timeout`, `statement_timeout`, `idle_in_transaction_session_timeout` — **set all three in production.** Explain what each prevents
- [ ] **Rep:** your app must retry on serialization failure (SQLSTATE 40001) and deadlock (40P01). Implement and test the retry loop
- [ ] Read **DDIA Chapter 7 (Transactions)** alongside this set. It's the best written explanation of isolation levels anywhere

### Set 3.4 — MVCC and concurrency (this is where Postgres gets interesting)
- [ ] The core idea: readers never block writers, writers never block readers. Understand the cost of that promise
- [ ] Tuple headers: `xmin`, `xmax`, `ctid`, `cmin/cmax`, infomask
- [ ] **Rep:** install `pageinspect` and read the raw page. `SELECT lp, t_xmin, t_xmax, t_ctid FROM heap_page_items(get_raw_page('t', 0))`. Update a row and watch the old and new versions both sitting in the page
- [ ] Transaction IDs, snapshots (`xmin`, `xmax`, `xip_list`), and the visibility rules. `txid_current()`, `pg_current_snapshot()`
- [ ] **Row versions are copies, not in-place updates.** Implications: UPDATE is as expensive as INSERT+DELETE, indexes must be updated too
- [ ] **HOT updates** (Heap-Only Tuples) — the optimization that avoids index writes, and the `fillfactor` tuning that enables it
- [ ] **Dead tuples and bloat.** `pg_stat_user_tables.n_dead_tup`, why a table can be 10GB with 1GB of live data
- [ ] **VACUUM**: what it does, `VACUUM` vs `VACUUM FULL` (rewrite + exclusive lock) vs `VACUUM FREEZE`. The free space map
- [ ] **Autovacuum**: the trigger formula (`autovacuum_vacuum_threshold + scale_factor * n_live_tup`), `autovacuum_max_workers`, cost-based delay, and per-table overrides
- [ ] **Transaction ID wraparound** — the 2-billion-XID horizon, `age(datfrozenxid)`, freezing, and the "database is not accepting commands" emergency. Know how to monitor it *before* it happens
- [ ] What holds back vacuum: long-running transactions, idle-in-transaction sessions, abandoned replication slots, orphaned prepared transactions. **All four have caused real outages**
- [ ] **Rep:** create bloat deliberately. Update 5M rows repeatedly with autovacuum off. Measure table size growth with `pg_total_relation_size`. Then fix it with `VACUUM FULL` and separately with `pg_repack`. Compare the locking impact
- [ ] **Rep:** open a transaction and leave it idle. Watch `n_dead_tup` climb on a busy table and vacuum refuse to reclaim. This is the #1 production Postgres incident — you should have caused it once
- [ ] Compare to other engines: Oracle undo logs, MySQL InnoDB undo/purge, SQL Server. Why Postgres chose in-heap versions and what it costs

---

## Phase 4 — Peak (internals, storage, and scale)

### Set 4.1 — The architecture (Suzuki Ch. 1–2, Rogov Part I)
- [ ] The process model: postmaster, backends, background writer, checkpointer, WAL writer, autovacuum launcher/workers, stats collector, archiver, logical replication workers
- [ ] **Rep:** `ps -ef | grep postgres` on your instance and identify every single process. Annotate the output in `notes/pg-processes.md`
- [ ] Shared memory: shared buffers, WAL buffers, lock tables, `ProcArray`. Why they're in shared memory and not per-backend
- [ ] The query pipeline: **parser → analyzer → rewriter → planner/optimizer → executor**. Know what each stage produces
- [ ] The system catalogs: `pg_class`, `pg_attribute`, `pg_index`, `pg_proc`, `pg_namespace`, `pg_am`. Query them directly, don't just use `\d`
- [ ] **Rep:** reimplement `\d tablename` as a raw SQL query against the catalogs. (Hint: `psql -E` shows you the queries psql itself runs — use that to check yourself)

### Set 4.2 — Storage layer (Suzuki Ch. 1, 5, 8, 9)
- [ ] Physical layout: `$PGDATA`, `base/<dboid>/<relfilenode>`, 1GB segment files, `pg_wal/`, `global/`
- [ ] **Rep:** find the actual file on disk backing one of your tables using `pg_relation_filepath()`. Look at it with `ls -la` and `hexdump`
- [ ] **Page structure (8KB)**: PageHeader, line pointers (ItemIds), free space, tuples growing from the end, special space. Draw it
- [ ] `pageinspect` deep dive: `page_header()`, `heap_page_items()`, `bt_page_items()` for index pages
- [ ] **TOAST** — the oversized-attribute mechanism. Compression, out-of-line storage, the 2KB threshold, `PLAIN/EXTENDED/EXTERNAL/MAIN` storage strategies, and why a `SELECT *` on a TOASTed column is expensive
- [ ] **Rep:** store a 1MB text value, find its TOAST table (`pg_class.reltoastrelid`), and count the chunks
- [ ] **Buffer manager**: buffer pool, buffer tags, the clock-sweep replacement algorithm, pinning, `usage_count`, ring buffers for seq scans (so a big scan doesn't evict your hot pages)
- [ ] **Rep:** install `pg_buffercache`. Run a query, then inspect which relations occupy shared buffers and their usage counts. Run a huge seq scan and show the ring buffer protecting your cache
- [ ] Double buffering: OS page cache *under* shared_buffers. Why `shared_buffers = 25% RAM` is the rule of thumb and not 90%
- [ ] `pg_prewarm`

### Set 4.3 — WAL, durability, and replication
- [ ] **Why WAL exists**: the torn-page problem and crash recovery. Write-ahead rule: log record hits disk before the data page
- [ ] WAL record structure, LSN (Log Sequence Number), `pg_current_wal_lsn()`, WAL segments (16MB default)
- [ ] **Rep:** `pg_waldump` a segment. Read actual WAL records for an INSERT, an UPDATE, and a COMMIT. Annotate them
- [ ] **Checkpoints**: what they flush, `checkpoint_timeout`, `max_wal_size`, `checkpoint_completion_target`, and the I/O spike problem
- [ ] **full_page_writes** — why the first write to a page after a checkpoint logs the entire page, and how that interacts with checkpoint frequency and WAL volume
- [ ] Crash recovery: find the last checkpoint → REDO from there. Why Postgres needs no UNDO log (MVCC gives it that for free)
- [ ] `synchronous_commit` levels: `on`, `remote_apply`, `remote_write`, `local`, `off`. The durability/latency tradeoff, quantified
- [ ] **Rep:** benchmark `pgbench` with `synchronous_commit` on vs off. Then `kill -9` the postmaster mid-load in both modes and see what survives
- [ ] `wal_level`: `minimal`, `replica`, `logical`
- [ ] **Physical (streaming) replication**: walsender/walreceiver, replication slots, hot standby, `synchronous_standby_names`, replication lag measurement, standby query conflicts and `hot_standby_feedback`
- [ ] **Rep:** set up a primary + streaming replica with Docker Compose. Measure replication lag under load. Then promote the replica and handle the failover
- [ ] **Logical replication**: publications/subscriptions, the decoding plugin, what it can and can't replicate (no DDL, no sequences). Use cases: major-version upgrades with near-zero downtime, CDC
- [ ] **Change Data Capture**: Debezium reading the logical replication stream into Kafka. This is the bridge to Track 09
- [ ] **Rep:** the orphaned-replication-slot incident: create a slot, never consume it, watch `pg_wal` grow until the disk fills. Then fix it. (This has taken down real companies)

### Set 4.4 — Parallel query and execution
- [ ] Gather / Gather Merge nodes, workers, leader participation
- [ ] `max_parallel_workers_per_gather`, `max_parallel_workers`, `parallel_setup_cost`, `parallel_tuple_cost`, `min_parallel_table_scan_size`
- [ ] Parallel-safe vs parallel-restricted vs parallel-unsafe functions
- [ ] What can go parallel: seq scan, hash join, aggregate, index scan (btree), append. What can't
- [ ] **Rep:** take a large aggregation. Force serial (`max_parallel_workers_per_gather=0`) and then allow 4 workers. Compare. Then find a query where parallelism makes it *slower* and explain why
- [ ] JIT compilation (`jit=on`, LLVM) — when it helps, when it costs more than it saves

### Set 4.5 — TimescaleDB and time-series (your listed item)
- [ ] Why time-series is a distinct problem: append-heavy, time-ordered, recent-data-hot, aggregate-over-window queries, retention policies
- [ ] Install TimescaleDB. **Hypertables** — automatic partitioning by time (and optionally by space/hash)
- [ ] Chunks, chunk_time_interval sizing, chunk exclusion in plans
- [ ] **Continuous aggregates** — incrementally-maintained materialized views with refresh policies. The killer feature
- [ ] **Compression** — columnar compression per chunk, `segmentby` and `orderby` configuration, 10–20x ratios, and the constraint that compressed chunks are (mostly) immutable
- [ ] Retention policies, `drop_chunks`, data tiering
- [ ] Hyperfunctions: `time_bucket`, `time_bucket_gapfill`, `locf`, `interpolate`, `first`/`last`, `approx_percentile`
- [ ] **Rep:** load a real time-series dataset (IoT sensor data, crypto ticks, or NYC taxi by pickup time — at least 50M rows). Build: hypertable + continuous aggregate + compression + retention policy
- [ ] **Rep:** benchmark the same "last 30 days hourly average" query against (a) a plain table, (b) a natively-partitioned table with a BRIN index, (c) a hypertable, (d) a continuous aggregate. Four numbers, one table, in `notes/timeseries-benchmark.md`
- [ ] Compare against the alternatives: InfluxDB, ClickHouse, Prometheus. When would you *not* pick Timescale?
- [ ] **Rep (your "real-time data / CDC + CPS" item):** build a small pipeline — a producer writes sensor/market readings → Postgres/Timescale → a continuous aggregate → a dashboard (Grafana) that refreshes live. Then add Debezium CDC off the WAL into a second consumer. Document the end-to-end latency at each hop

### Set 4.6 — Sharding and scaling out (bridges to Track 09)
- [ ] The scaling ladder, in order: query tuning → indexing → hardware → read replicas → caching → partitioning → sharding. **Know that sharding is last for a reason**
- [ ] Read replicas: routing reads, and the **read-your-own-writes** problem replication lag creates
- [ ] Vertical partitioning vs horizontal partitioning vs sharding — precise definitions
- [ ] Shard key selection: cardinality, distribution, and whether your common queries can be routed to one shard. Hotspots
- [ ] Consistent hashing vs range sharding vs directory-based sharding
- [ ] Resharding: the hard part. How you add a shard without downtime
- [ ] Cross-shard problems: joins, transactions (2PC), unique constraints, aggregation, foreign keys
- [ ] **Citus** — distributed Postgres. Distributed tables, reference tables, co-location, the coordinator node
- [ ] **Rep:** stand up a 3-node Citus cluster in Docker. Distribute a table by tenant_id, co-locate a related table, and compare a single-tenant query vs a cross-shard aggregate in EXPLAIN
- [ ] `postgres_fdw` and sharding-by-hand
- [ ] Read **DDIA Chapter 6 (Partitioning)** — you said "sharding, read it first." Do it here, where you have the context to actually absorb it
- [ ] **Rep:** write `notes/scaling-decision.md` — given a hypothetical service at 50k writes/sec and 5TB, lay out your scaling plan with the reasoning at each step

### Set 4.7 — Production operations
- [ ] Monitoring: `pg_stat_activity`, `pg_stat_database`, `pg_stat_user_tables`, `pg_stat_bgwriter`, `pg_locks`, `pg_stat_replication`, `pg_stat_progress_*`
- [ ] The metrics that matter: cache hit ratio, transaction rate, replication lag, longest transaction, dead tuple ratio, connection count, checkpoint frequency, WAL generation rate
- [ ] Set up **Prometheus + postgres_exporter + Grafana** against your instance (ties into Track 07)
- [ ] Alerting thresholds you'd actually set. Write them down
- [ ] Major version upgrades: `pg_upgrade` (with `--link`) vs dump/restore vs logical replication. Downtime for each
- [ ] Extensions worth knowing: `pg_stat_statements`, `pg_trgm`, `postgis`, `pgvector`, `pg_partman`, `pg_cron`, `hypopg` (hypothetical indexes!)
- [ ] **Rep:** use `hypopg` to test whether an index would help *before* building it on a large table

### Set 4.8 — The 3AM database drills
Each drill: reproduce it, diagnose it with only `psql` and the shell, fix it, write it up.
- [ ] **Drill:** "The app is timing out." Find the blocking chain in `pg_locks` + `pg_stat_activity` and identify the root blocker
- [ ] **Drill:** "Disk is filling up." Distinguish between table bloat, WAL accumulation, an orphaned replication slot, and temp files from a spilling sort
- [ ] **Drill:** "This query was fast yesterday." Stale statistics, plan flip, parameter sniffing on a prepared statement, or bloat. Work through all four hypotheses
- [ ] **Drill:** "Connections exhausted." `max_connections` hit. Triage without restarting the database
- [ ] **Drill:** "Replica is 40 minutes behind." Find out why (long query on standby, single-threaded replay, network, I/O)
- [ ] **Drill:** "Autovacuum can't keep up." Identify what's holding the xmin horizon
- [ ] **Drill:** "We dropped the wrong table 20 minutes ago." PITR, under pressure
- [ ] **Drill:** wraparound warning in the logs. What do you do, in what order?
- [ ] **Capstone:** `notes/pg-3am-runbook.md` — the exact queries you'd run, in order, for a database incident

---

## Exit criteria for Track 03

- [ ] You can read any `EXPLAIN (ANALYZE, BUFFERS)` plan and say what's wrong with it
- [ ] You can explain MVCC, WAL, and the buffer manager on a whiteboard without notes
- [ ] You have personally recovered a database with PITR
- [ ] You have caused, diagnosed, and fixed: bloat, a deadlock, a lock queue, and a bad plan
- [ ] You can design a schema, index it, and defend every choice
- [ ] Postgres is no longer a black box you send SQL into. You know what happens to the query.
