# Track 08 — Algorithms & Data Structures

> **Muscle group:** the one you train year-round, in small doses, forever.
> **Prereqs:** a language you're fluent in (Python is fine and is what most people use for this).
> **Cadence:** this track is **never** done in a block. 3–5 problems a week, every week, for the whole program. It's your daily cardio, not a leg day.

## Why this track

Two separate reasons, and it's worth being honest about both:

1. **It genuinely rewires how you think.** Recognizing that a problem is a graph problem, or
   that a computation has an exploitable overlapping-subproblem structure, is a real and
   transferable skill. Every index, query planner, scheduler, and cache you studied in the
   other tracks is an algorithm and a data structure. This track is why those made sense.
2. **It's the interview filter.** FAANG and FAANG-adjacent interviews test this. Pretending
   otherwise doesn't help you.

The trap is grinding 500 LeetCode problems by pattern-matching and learning nothing. The
program below is built to avoid that: **theory first, patterns second, volume last.**

## Equipment

| Resource | Use it for |
|---|---|
| **MIT 6.006 Introduction to Algorithms** (OCW, free, full videos + psets) | The main course. Newer version is data-structure-first and excellent. |
| **MIT 6.046 Design and Analysis of Algorithms** (OCW) | Phase 3. Advanced design paradigms. |
| **CLRS** (*Introduction to Algorithms*) | Reference, not a read-through. Look things up in it. |
| **Harvard CS50** weeks 3 & 5 | Gentler entry if 6.006 feels steep; the psets are well built |
| **Algorithms** — Sedgewick (Princeton, Coursera) | Excellent alternative to 6.006, more implementation-focused |
| **NeetCode 150** / **Blind 75** | Phase 2–3 pattern drilling |
| **Competitive Programmer's Handbook** — Laaksonen (free) | Concise reference for techniques |
| **Grokking the Coding Interview** patterns | Pattern taxonomy |
| **Codeforces / AtCoder** | Phase 4, if you want real sharpness |

**Rule:** implement every data structure **from scratch, once**, before you use the library
version in interviews. You are allowed to use the library forever after.

---

## Phase 1 — Foundation (theory, so patterns aren't memorization)

### Set 1.1 — Complexity
- [ ] Big-O, Big-Θ, Big-Ω. Say precisely what each means, and stop saying "Big-O" when you mean Θ
- [ ] Best/average/worst case. Why "average case" needs a stated input distribution
- [ ] **Amortized analysis** — aggregate, accounting, and potential methods. Why a dynamic array's append is O(1) amortized despite occasional O(n) resizes
- [ ] Space complexity, and counting recursion stack space (people forget this)
- [ ] Solving recurrences: the recursion tree method and the **Master Theorem** (all three cases)
- [ ] **Rep:** derive the complexity of mergesort, quicksort (average and worst), binary search, and DFS from their recurrences. By hand, on paper
- [ ] **Rep:** write `notes/complexity-reference.md` — a table of every structure and operation you'll use, with time and space for each. Build this yourself; don't copy one

### Set 1.2 — Core data structures (implement each from scratch)
- [ ] **Dynamic array** — growth factor, amortized append, why 2x (or 1.5x)
- [ ] **Linked list** — singly, doubly. And a clear-eyed note on why they're rarely the right choice in practice (cache locality)
- [ ] **Stack** and **queue**. Queue from two stacks. Circular buffer / ring buffer
- [ ] **Hash table** — hash functions, **collision resolution: chaining vs open addressing (linear probing, robin hood)**, load factor, resizing, and why worst case is O(n)
- [ ] **Rep:** implement a hash table from scratch with chaining and with open addressing. Benchmark both at load factors 0.5, 0.75, 0.95. Graph it. Then go re-read Track 03's index chapter — this is what a hash index is
- [ ] **Binary search tree** — insert/delete/search, and why it degenerates to a list
- [ ] **Balanced BSTs**: AVL (rotations) and **red-black** (know the invariants and why they're weaker but cheaper). Implement one of them fully
- [ ] **B-tree / B+ tree** — implement one. **This is the single highest-value structure for you** given Track 03: node fanout, why disks want high fanout, leaf-linked B+ trees for range scans
- [ ] **Rep:** after implementing a B+ tree, write `notes/btree-to-postgres.md` connecting your implementation to what `bt_page_items()` showed you in Track 03 Set 4.2
- [ ] **Heap / priority queue** — binary heap, sift up/down, heapify in O(n), `heapq`. Then implement a **d-ary heap** and know where a Fibonacci heap matters (and why it rarely does in practice)
- [ ] **Trie / prefix tree** — and its compressed form (radix tree). Where it beats a hash map
- [ ] **Union-Find (Disjoint Set Union)** — path compression + union by rank, and the inverse-Ackermann bound
- [ ] **LRU cache** — hash map + doubly linked list. Then **LFU**. (And connect to the clock-sweep algorithm from Track 03 Set 4.2 and the page replacement policies from Track 04 Set 1.3)
- [ ] **Bloom filter** — false positives, no false negatives, the math for sizing. Where real systems use it (LSM-trees, CDNs)
- [ ] **Skip list** — the probabilistic alternative to a balanced tree. Used in Redis sorted sets and LevelDB memtables
- [ ] **LSM-tree** — memtable + SSTables + compaction. Implement a toy one. (This is DDIA Ch. 3 made concrete — Track 09)

### Set 1.3 — Core algorithms
- [ ] Sorting: insertion, merge, quick (+ pivot choice and 3-way partitioning), heap, counting, radix, bucket. **Timsort** — what Python and Java actually use and why
- [ ] Stability, in-place, comparison lower bound Ω(n log n) and why counting sort escapes it
- [ ] **Rep:** implement mergesort, quicksort, and heapsort. Benchmark on random, sorted, reverse-sorted, and all-duplicate inputs. The results will teach you something no article will
- [ ] **Binary search** — and its variants: lower bound, upper bound, first true in a monotonic predicate, **binary search on the answer**. Write it once, correctly, with a template you trust, and never fight off-by-ones again
- [ ] **Rep:** implement binary search 4 ways (find, lower_bound, upper_bound, search-on-answer) and add a property-based test with `hypothesis` comparing against a brute-force reference
- [ ] Graph representations: adjacency list vs matrix, and when each wins
- [ ] **BFS** — shortest path in unweighted graphs, level-order, multi-source BFS, 0-1 BFS
- [ ] **DFS** — recursive and iterative, discovery/finish times, cycle detection in directed and undirected graphs
- [ ] **Topological sort** — Kahn's algorithm and DFS-based. Cycle detection as a byproduct. (Your build system, your Airflow DAG, your Spark stages — all this)
- [ ] **Dijkstra** (and why it fails on negative edges), **Bellman-Ford** (and negative cycle detection), **Floyd-Warshall**, **A\***
- [ ] MST: **Kruskal** (with union-find) and **Prim**
- [ ] Connected components, strongly connected components (Kosaraju or Tarjan), bipartite checking
- [ ] MIT 6.006 problem sets — do them. They are better than LeetCode for building the foundation

---

## Phase 2 — Volume (patterns and deliberate practice)

**Method that actually works — follow it:**
1. Read the problem. Restate it in your own words. State the constraints out loud.
2. **Think for 20–30 minutes before looking at anything.** Brute force first, then optimize.
3. If stuck past 30 min: read the *hint* only, not the solution. Another 15 min.
4. Still stuck: read the solution, then **close it and re-implement from scratch**.
5. Log the problem in `work/08-dsa/log.md`: pattern, what you missed, the key insight.
6. **Re-solve every problem you failed after 7 days, and again after 30.** Spaced repetition is the whole trick.

### Set 2.1 — The patterns (work through NeetCode 150 organized this way)
- [ ] **Two pointers** — sorted arrays, opposite ends, fast/slow (cycle detection)
- [ ] **Sliding window** — fixed and variable size, with a hashmap for counts
- [ ] **Prefix sums** and difference arrays. 2D prefix sums
- [ ] **Binary search on the answer** — "minimize the maximum," "can we do it in K?"
- [ ] **Hashing** — frequency maps, seen-sets, grouping, complement lookups
- [ ] **Stack patterns** — monotonic stack (next greater element, largest rectangle in histogram), parentheses, expression evaluation
- [ ] **Heap patterns** — top-K, merge K sorted, median from a stream (two heaps), scheduling
- [ ] **Intervals** — merge, insert, sweep line, meeting rooms
- [ ] **Linked list** — reversal, cycle detection, merge, reorder, LRU
- [ ] **Trees** — traversals (all four), BST properties, LCA, diameter, path sums, serialize/deserialize, tree DP
- [ ] **Tries** — word search, autocomplete, prefix matching
- [ ] **Graphs** — BFS/DFS on grids, islands, topological sort problems, shortest path, union-find problems
- [ ] **Backtracking** — subsets, permutations, combinations, N-queens, sudoku, word search. **Learn the one template and the pruning discipline**
- [ ] **Greedy** — and, crucially, **how to prove a greedy choice is correct** (exchange argument). Most people use greedy by feel and get burned
- [ ] **Bit manipulation** — XOR tricks, masks, subsets via bitmask, `n & (n-1)`
- [ ] **Math** — GCD/LCM, modular arithmetic, primes/sieve, fast exponentiation, combinatorics

### Set 2.2 — Dynamic programming (its own set, because it's the wall)
- [ ] The two ingredients: **optimal substructure** + **overlapping subproblems**. Verify both before reaching for DP
- [ ] The procedure: define the state → write the recurrence → identify base cases → decide memo (top-down) or tabulation (bottom-up) → optimize space
- [ ] **Always start top-down recursive + memo.** Convert to bottom-up only if you need to. This is the practical advice that unblocks most people
- [ ] 1D DP: climbing stairs, house robber, decode ways, word break, LIS (both O(n²) and the O(n log n) patience-sorting version)
- [ ] 2D DP: grid paths, edit distance, LCS, longest palindromic substring, regex matching
- [ ] Knapsack family: 0/1, unbounded, subset sum, partition equal subset, coin change (both variants). **Know why the loop order differs between 0/1 and unbounded** — this is the real test
- [ ] Interval DP: burst balloons, matrix chain multiplication
- [ ] Tree DP, bitmask DP, digit DP (the last only if you're going for competitive)
- [ ] State-machine DP: stock-trading problems as a family (I, II, III, IV, with cooldown, with fee — all one framework)
- [ ] **Rep:** solve 25 DP problems. Then write `notes/dp-framework.md` — your own procedure for attacking an unseen DP problem
- [ ] MIT 6.006 has four full DP lectures. Watch all four

### Set 2.3 — Volume targets
Quality over quantity, but volume is still required. Track these in `work/08-dsa/log.md`.
- [ ] 25 Easy (get fast and clean; these should take <15 min each)
- [ ] 75 Medium (this is the interview band — most of your time goes here)
- [ ] 25 Hard (for the ceiling; you don't need to be fast, you need to not panic)
- [ ] Complete **NeetCode 150**
- [ ] Re-solve every failed problem at +7 days and +30 days

---

## Phase 3 — Strength (advanced design and the harder course)

### Set 3.1 — MIT 6.046 design paradigms
- [ ] **Divide and conquer** — the master theorem revisited, Karatsuba multiplication, closest pair of points, FFT (conceptually)
- [ ] **Randomized algorithms** — randomized quicksort, hashing (universal hashing), Monte Carlo vs Las Vegas, reservoir sampling
- [ ] **Amortized analysis** applied — splay trees, dynamic tables
- [ ] **Network flow** — max-flow/min-cut, Ford-Fulkerson, Edmonds-Karp, Dinic's. Bipartite matching as a flow problem. **Learning to *reduce* a problem to max-flow is the real skill here**
- [ ] **Linear programming** conceptually, and duality
- [ ] **NP-completeness** — P vs NP, reductions, SAT, and the canonical NP-complete problems. **What you do when your problem is NP-hard**: approximation algorithms, heuristics, exact solvers on small inputs, or changing the problem
- [ ] **Rep:** prove one problem NP-complete by reduction. Once is enough, but do it once
- [ ] Approximation algorithms: vertex cover 2-approx, set cover greedy log-n

### Set 3.2 — Algorithms in the systems you're studying
This set is what makes this track *not* interview-prep-shaped. Write each up in `notes/algorithms-in-the-wild.md`.
- [ ] **B+ trees** in Postgres indexes → you implemented one in Set 1.2
- [ ] **LSM-trees** in RocksDB/Cassandra → DDIA Ch. 3
- [ ] **Consistent hashing** in shard routing, caches, DynamoDB → implement it with virtual nodes
- [ ] **HyperLogLog** for cardinality estimation → why `COUNT(DISTINCT)` is expensive and how approximation works
- [ ] **Count-Min Sketch** for heavy hitters
- [ ] **Merkle trees** in git (you built this in Track 02!), Dynamo anti-entropy, blockchains
- [ ] **Bloom filters** in LSM-tree read paths and CDN caches
- [ ] **Raft/Paxos** as distributed consensus algorithms → Track 09
- [ ] **Clock sweep / LRU** in the Postgres buffer manager and OS page cache
- [ ] **Topological sort** in build systems, task schedulers, Spark DAGs, and query plans
- [ ] **Dynamic programming** in the Postgres join order optimizer (System-R style) — read about it, then look at a plan differently
- [ ] **Rate limiting algorithms**: token bucket, leaky bucket, sliding window log, sliding window counter. Implement all four
- [ ] **CRDTs** for collaborative editing → Track 09 (your Google Docs question)

### Set 3.3 — Code quality under pressure
- [ ] Write solutions that are **readable**: meaningful names, early returns, no cleverness for its own sake
- [ ] Always state the complexity out loud before coding, and verify after
- [ ] **Test your own code before saying "done"** — happy path, empty input, single element, duplicates, negatives, overflow, max constraints
- [ ] **Rep:** record yourself solving a Medium, out loud, in 35 minutes, with no IDE autocomplete. Watch it back. This is uncomfortable and extremely effective

---

## Phase 4 — Peak (interview conditions)

### Set 4.1 — Mock interviews
- [ ] 10 mock interviews on **Pramp** / **interviewing.io** / with a peer. Real time pressure, real human, talking the whole time
- [ ] Practice the frame: clarify → examples → brute force → optimize → **confirm approach before coding** → code → test → complexity
- [ ] **Practice narrating while coding.** Silent problem solving reads as "stuck" to an interviewer
- [ ] Practice getting stuck gracefully: state what you've tried, state your hypothesis, ask a targeted question
- [ ] Practice taking a hint without deflating

### Set 4.2 — Timed sets
- [ ] 5 sessions of: 2 Mediums in 45 minutes, cold, no hints
- [ ] 3 sessions of: 1 Hard in 45 minutes
- [ ] Weekly contest on LeetCode or Codeforces Div 3/4 — the time pressure is the point
- [ ] **Rep:** a full mock loop in one day — 4 × 45-minute technical rounds. Measure your degradation across the day. **Stamina is a real and trainable variable**

### Set 4.3 — Maintenance mode (after Phase 4, forever)
- [ ] 2–3 problems per week, indefinitely
- [ ] Revisit `notes/dp-framework.md` and your weak patterns quarterly
- [ ] One "algorithms in the wild" writeup per month, from something you encountered at work

---

## Exit criteria for Track 08

- [ ] You implemented every core data structure from scratch, including a B+ tree
- [ ] You can solve an unseen Medium in 25 minutes, talking the whole time
- [ ] DP is a procedure you execute, not a wall you hit
- [ ] You can state the complexity of anything you write, immediately and correctly
- [ ] You can point at five algorithms inside the systems you use daily and explain why they're there
