# Track 04 — Operating Systems (OSTEP + xv6)

> **Muscle group:** the core. Nothing else is stable without it.
> **Prereqs:** Track 01 Phase 1–2. Enough C to read and write small programs (Set 0 below).
> **Book:** *Operating Systems: Three Easy Pieces* (OSTEP) — Remzi & Andrea Arpaci-Dusseau. Free at ostep.org. You named this one; it's the right choice.

## Why this track

Every "weird" bug you will ever chase — the one where the process hangs in `D` state, the
one where memory usage doesn't drop after you free it, the one where two threads corrupt a
counter, the one where the file write "succeeded" but the data is gone after a power loss —
is an operating systems bug wearing a costume. This track is what turns "the server is
acting strange" into "the server is doing exactly what it was told, and here's what."

## Equipment

| Resource | Use it for |
|---|---|
| **OSTEP** (ostep.org) — free, 3 parts, ~50 short chapters | The main text. Chapters are 10–20 pages; one per session is a sane pace. |
| **OSTEP homeworks + projects** (github.com/remzi-arpacidusseau/ostep-projects) | The simulators are the whole point. Do them. |
| **MIT 6.1810 Operating System Engineering** (pdos.csail.mit.edu/6.1810) | The xv6 labs — the best OS labs in existence, all public with autograders |
| **xv6 book** (*xv6: a simple, Unix-like teaching operating system*) | Read alongside the labs |
| **Harvard CS50** weeks 4–5 (Memory, Data Structures) + psets | If your C/pointers are shaky, start here |
| **Beej's Guide to C Programming** | C reference |
| **The Linux Programming Interface** — Kerrisk | Reference for real-world syscalls (do not read cover to cover) |
| **Computer Systems: A Programmer's Perspective** (CS:APP) | Optional deeper dive on the machine layer |

---

## Phase 0 — Set up (C, so you can actually do the labs)

### Set 0.1 — Enough C
- [ ] Harvard **CS50 Week 4 (Memory)** lecture + shorts
- [ ] Pointers: address-of, dereference, pointer arithmetic, `void*`, function pointers
- [ ] Arrays vs pointers, strings as `char*`, null termination, `strlen` vs `sizeof`
- [ ] The memory layout of a process: text, data, bss, heap, stack. Draw it
- [ ] `malloc`/`free`/`calloc`/`realloc`. Leaks, double-free, use-after-free, buffer overflow
- [ ] Structs, `typedef`, header files, the compile→assemble→link pipeline
- [ ] **Rep:** CS50 pset — **Recover** (recovering JPEGs from a raw disk image). Teaches file I/O and buffers
- [ ] **Rep:** CS50 pset — **Speller** (hash table spell checker in C). Teaches pointers, structs, and memory discipline
- [ ] Tooling: `gcc -Wall -Wextra -g`, `make` and writing a basic Makefile, `valgrind`, AddressSanitizer (`-fsanitize=address`), `gdb` basics
- [ ] **Rep:** write a program with a deliberate use-after-free. Catch it with valgrind, then with ASan. Note which gave you the better report

---

## Phase 1 — Virtualization (OSTEP Part 1, Ch. 3–24)

### Set 1.1 — Processes and the process API (Ch. 3–6)
- [ ] Ch. 4: The Abstraction — The Process. Process states: running, ready, blocked. The PCB
- [ ] Ch. 5: The Process API — **`fork()`, `exec()`, `wait()`** and why Unix split them (this design decision is worth understanding deeply)
- [ ] **Rep:** OSTEP Ch. 5 homework — answer every fork/exec question *before* running the code, then run it
- [ ] **Rep:** write a program where fork returns twice and you print the PID/PPID from both branches. Add `wait()`. Then remove `wait()` and observe the zombie in `ps`
- [ ] **Rep (project): build a shell.** OSTEP's `processes-shell` project or CS:APP's tiny shell. Must support: command execution, arguments, `cd`, redirection (`>`, `<`), pipes (`|`), background (`&`), and Ctrl-C handling. **This is the single most valuable exercise in this phase** — it makes fork/exec/wait/dup2/pipe/waitpid permanent
- [ ] Ch. 6: Limited Direct Execution — **user mode vs kernel mode**, the trap table, how a syscall actually transfers control, the timer interrupt
- [ ] **Rep:** `strace ./your-shell` and map every syscall your shell makes to the source line that caused it (ties back to Track 01 Set 2.3)
- [ ] File descriptors properly: the fd table → open file table → inode. `dup`, `dup2`, `pipe`, `close`. Why fd 0/1/2 are what they are
- [ ] **Rep:** implement `ls | wc -l` by hand with `pipe()`, `fork()`, `dup2()`, `execvp()`. No shell involved
- [ ] **Rep:** explain in `notes/fd-table.md` what happens to file descriptors across `fork` and across `exec` (and what `FD_CLOEXEC` is for)
- [ ] Signals revisited with kernel context: delivery, handlers, `sigaction` vs `signal`, async-signal-safety, `SIGCHLD`

### Set 1.2 — Scheduling (Ch. 7–11)
- [ ] Metrics: turnaround time vs response time. The fundamental tension
- [ ] FIFO, SJF, STCF, Round Robin. The convoy effect
- [ ] **MLFQ** (Multi-Level Feedback Queue) — the rules, gaming the scheduler, priority boost
- [ ] Lottery/stride scheduling — proportional share
- [ ] **CFS** (Linux's Completely Fair Scheduler) — vruntime, red-black tree, nice values, and `sched_latency`. Also know that **EEVDF** replaced CFS in Linux 6.6+
- [ ] Multiprocessor scheduling: cache affinity, load balancing, per-CPU runqueues
- [ ] **Rep:** OSTEP scheduler simulators — `scheduler.py` and `mlfq.py`. Predict the output before running each configuration
- [ ] **Rep:** connect it to reality — `nice`, `renice`, `chrt`, `taskset`, and cgroup CPU limits. Run a CPU hog, pin it with `taskset`, and watch it in `htop`

### Set 1.3 — Memory and virtual memory (Ch. 12–24) — the heart of this track
- [ ] Ch. 13: The address space abstraction. Why every process thinks it starts at 0
- [ ] Ch. 14–17: The memory API, `malloc` internals, free-space management (splitting, coalescing, best/worst/first fit, segregated lists, buddy allocator)
- [ ] Ch. 15–16: Address translation, base+bounds, segmentation, external fragmentation
- [ ] **Ch. 18–20: Paging.** Page tables, PTEs, valid/present/dirty/accessed bits, the page table's own memory cost
- [ ] **Multi-level page tables** — why a 4-level table on x86-64 and what each level indexes
- [ ] **Ch. 19: The TLB.** Why it exists, hit/miss cost, TLB reach, context switch flushes, ASIDs. **A TLB miss can cost more than the instruction it serves**
- [ ] **Rep:** OSTEP `tlb.c` measurement homework — write the program that measures TLB size and miss cost empirically by striding through arrays at page boundaries. Graph the results. You will see the TLB in the graph
- [ ] Ch. 21–22: Swapping, page faults, the page replacement policies (OPT, FIFO, LRU, clock, random), Belady's anomaly, working sets, thrashing
- [ ] **Demand paging, copy-on-write, and `mmap`** — the three things that explain why `fork()` on a 10GB process is fast and why `free` doesn't show memory returning
- [ ] **Rep:** write a program that `mmap`s a large file and reads it randomly. Watch page faults with `/usr/bin/time -v` (minor vs major faults). Explain the difference
- [ ] **Rep:** fork a process holding a 1GB array. Measure the memory *before* and *after* the child writes to it. You just observed copy-on-write
- [ ] `RSS` vs `VSZ` vs `PSS` — now explain them properly and go update your Track 01 `htop.md` notes
- [ ] The **OOM killer**: `/proc/<pid>/oom_score`, overcommit (`vm.overcommit_memory`), and why `malloc` can succeed and the write can still kill you
- [ ] **Rep:** `cat /proc/<pid>/maps` and `/proc/<pid>/smaps` for a real process (try your Postgres backend). Identify: text segment, heap, stack, shared libs, and the shared memory segment
- [ ] **Rep:** OSTEP `paging-linear-translate.py`, `paging-multilevel-translate.py`, `vm-beyondphys.py` homeworks
- [ ] **Rep (project):** implement your own `malloc`/`free` with a free list and coalescing (CS:APP malloc lab or OSTEP's). Benchmark against libc's

### Set 1.4 — xv6 labs, part 1
Set up the xv6 environment (RISC-V toolchain + QEMU) and work the MIT 6.1810 labs:
- [ ] **Lab: Util** — write `sleep`, `pingpong`, `primes` (a pipeline of processes!), `find`, `xargs` in xv6 userland. Note: `find` here is literally your "recursively find files in a path" goal, implemented from scratch
- [ ] **Lab: Syscall** — add `trace` and `sysinfo` system calls to the kernel. You will touch the syscall table, the trap path, and user/kernel memory copying. **After this lab, syscalls stop being magic**
- [ ] **Lab: Page tables** — print a page table, implement per-process kernel page tables / `sbrk` lazy allocation depending on the year's variant
- [ ] **Lab: Traps** — backtrace and alarm (user-level interrupt handlers). Teaches the stack frame and trap frame
- [ ] **Lab: Copy-on-write fork** — implement COW in the kernel. This is the lab that makes VM click permanently

---

## Phase 2 — Concurrency (OSTEP Part 2, Ch. 25–34)

### Set 2.1 — Threads and locks (Ch. 26–29)
- [ ] Ch. 26: Concurrency intro. Why the shared counter increments incorrectly — trace it at the assembly level (load, add, store)
- [ ] Ch. 27: The thread API — `pthread_create`, `join`, `mutex`, `cond`
- [ ] **Rep:** write the broken counter. Run it with 2 threads × 1M increments. Observe the wrong total. Fix with a mutex. Measure the cost of the mutex
- [ ] Ch. 28: Locks — how they're built. Test-and-set, compare-and-swap, fetch-and-add, ticket locks, spin vs block, futexes, two-phase locks
- [ ] Understand **atomicity, visibility, and reordering** as three distinct problems. Memory barriers. `volatile` is not a synchronization primitive in C
- [ ] Ch. 29: Lock-based concurrent data structures — a concurrent counter (naive vs sloppy), list, queue, hash table. **Lock granularity** and why fine-grained locking isn't automatically faster
- [ ] **Rep:** implement a thread-safe hash table two ways — one global lock vs per-bucket locks. Benchmark at 1/2/4/8 threads. Graph it. Find the crossover point

### Set 2.2 — Condition variables, semaphores, and bugs (Ch. 30–33)
- [ ] Ch. 30: Condition variables — `wait`/`signal`/`broadcast`. **Why you always wait in a `while` loop, never an `if`** (spurious wakeups + the Mesa semantics argument)
- [ ] **Rep:** producer/consumer with a bounded buffer using a mutex + 2 condition variables. Get it right. Then break it (use `if` instead of `while`, or one CV instead of two) and demonstrate the failure
- [ ] Ch. 31: Semaphores — binary and counting. Implement a mutex with a semaphore and a semaphore with a mutex+CV
- [ ] The classic problems: reader-writer (and writer starvation), dining philosophers (and the ordering fix), sleeping barber
- [ ] Ch. 32: **Concurrency bugs** — atomicity violations, order violations, deadlock. The **four conditions for deadlock** (mutual exclusion, hold-and-wait, no preemption, circular wait) and how to break each one
- [ ] **Rep:** write a deliberate deadlock between two threads. Find it with `gdb` (`thread apply all bt`). Then find it with ThreadSanitizer (`-fsanitize=thread`)
- [ ] Livelock and starvation. Why "just add a retry" sometimes makes it worse
- [ ] Ch. 33: Event-based concurrency — the event loop, `select`/`poll`/`epoll`, and why blocking calls destroy an event loop
- [ ] **Rep:** write a single-threaded `epoll` echo server handling 1000 concurrent connections. Then compare it to a thread-per-connection version at the same load. Measure memory and latency
- [ ] Connect it up: this is exactly why **Node.js**, **nginx**, and **asyncio** are built the way they are. And exactly why **Postgres** (process-per-connection) needs PgBouncer — go re-read Track 03 Set 2.4 with this understanding
- [ ] `async`/`await` in Python and JS: understand that it's cooperative scheduling over an event loop, and what a "blocking call in an async function" actually does to you
- [ ] **Rep:** write `notes/concurrency-models.md` comparing process-per-request, thread-per-request, event loop, and green threads/goroutines. With one real system as an example of each

### Set 2.3 — xv6 labs, part 2
- [ ] **Lab: Multithreading** — build a user-level thread package (context switching in assembly), plus a parallel hash table and a barrier
- [ ] **Lab: Locks** — remove lock contention from the kernel memory allocator and buffer cache. **This is a real performance-engineering exercise**: measure, find contention, redesign, re-measure

---

## Phase 3 — Persistence (OSTEP Part 3, Ch. 35–45)

### Set 3.1 — I/O and storage devices (Ch. 36–38)
- [ ] I/O: polling vs interrupts vs DMA. Memory-mapped I/O. Why interrupts aren't always better (interrupt storms, and why NAPI polls)
- [ ] Hard disks: geometry, seek + rotational latency + transfer time. Compute the actual cost of a random read
- [ ] Disk scheduling: FCFS, SSTF, SCAN/elevator, and why Linux's `noop`/`mq-deadline` is right for SSDs
- [ ] **SSDs and flash**: pages vs blocks, erase-before-write, the FTL, wear leveling, **write amplification**, TRIM, and why SSD random writes degrade over time
- [ ] **Rep:** benchmark your disk with `fio` — random vs sequential, read vs write, various block sizes and queue depths. Graph IOPS and latency. Now you understand why `random_page_cost` exists in Postgres
- [ ] RAID 0/1/4/5/6/10 — capacity, performance, fault tolerance. The RAID-5 write hole

### Set 3.2 — Filesystems (Ch. 39–43)
- [ ] The file API: `open`, `read`, `write`, `lseek`, `close`, `stat`, `link`, `unlink`, `rename`, `fsync`
- [ ] **`rename` is atomic; this is the foundation of every safe-file-write pattern.** Learn the write-temp-then-rename idiom and when you also need to fsync the directory
- [ ] Inodes, directories as files, hard vs symbolic links revisited with full understanding
- [ ] Ch. 40: FS implementation — superblock, inode bitmap, data bitmap, inode table, data blocks. Direct/indirect/double-indirect pointers and the resulting max file size
- [ ] **Rep:** OSTEP `vsfs.py` simulator. Predict the state after each operation
- [ ] Ch. 41: FFS — cylinder groups, locality. Ch. 43: LFS — log-structured, and how **this is the same idea as an LSM-tree** (bridge to DDIA Ch. 3, Track 09)
- [ ] Ch. 42: **Crash consistency** — the problem, `fsck`, and **journaling** (data vs ordered vs writeback modes in ext4). Why metadata-only journaling can leave you with garbage in a file
- [ ] The **fsync story**: page cache, write-back, `fsync` vs `fdatasync` vs `O_DIRECT` vs `O_SYNC`. Read about the "fsync-gate" incident in Postgres (2018) — `fsync` errors on Linux used to be reported once and then the dirty page was dropped
- [ ] **Rep:** write a program that appends to a file, and demonstrate data loss by killing the machine/container without fsync. Then add fsync and show durability. Measure the cost of fsync in ops/sec
- [ ] Now go back to Track 03 Set 4.3 (WAL) and re-read it. It will read completely differently
- [ ] Modern filesystems: ext4, XFS, btrfs, ZFS — copy-on-write, snapshots, checksums
- [ ] Ch. 44–45: NFS and AFS — distributed filesystems, statelessness, idempotency, and cache consistency. This is your on-ramp to Track 09

### Set 3.3 — xv6 labs, part 3
- [ ] **Lab: File system** — add large files (doubly-indirect blocks) and symbolic links to xv6
- [ ] **Lab: Mmap** — implement `mmap`/`munmap` in the kernel. Ties Phase 1 (VM) and Phase 3 (files) together, which is exactly the point
- [ ] **Lab: Networking** (optional but excellent) — write a driver for an E1000 NIC. Bridges into Track 05

---

## Phase 4 — Peak (systems thinking)

### Set 4.1 — Security and isolation
- [ ] OSTEP Ch. 53–56 (security section) or equivalent
- [ ] Buffer overflow → stack smashing → shellcode. Then the mitigations: stack canaries, NX/DEP, ASLR, PIE, RELRO
- [ ] **Rep:** do 3–5 levels of **pwn.college** or **OverTheWire Narnia/Protostar**. Actually smash a stack once, with mitigations disabled. Then turn them on and see them stop you
- [ ] Privilege separation, setuid dangers, capabilities, seccomp
- [ ] **Namespaces and cgroups** — read this here, apply it in Track 06. A container is not a thing; it's a process with lies told to it

### Set 4.2 — Performance engineering
- [ ] Latency numbers every engineer should know (Jeff Dean's table). Memorize the orders of magnitude, not the digits
- [ ] The memory hierarchy: register → L1 → L2 → L3 → RAM → SSD → network → disk. Cache lines, spatial/temporal locality
- [ ] **False sharing** — two threads on separate variables in the same cache line. **Rep:** demonstrate it and fix it with padding. Measure the speedup
- [ ] `perf stat`, `perf record`/`report`, **flame graphs** (Brendan Gregg's tooling)
- [ ] **Rep:** profile a real program, find the hot path, optimize it, and prove the improvement with before/after flame graphs
- [ ] Amdahl's law and Universal Scalability Law. Why your 32-core box doesn't go 32x
- [ ] Brendan Gregg's **USE method** (Utilization, Saturation, Errors) — apply it to CPU, memory, disk, network on a real box

### Set 4.3 — Synthesis
- [ ] **Capstone:** write `notes/what-happens-when.md` — trace, end to end and in real depth, what happens when you type `./myprogram > out.txt` and hit Enter. Shell parse → fork → open+dup2 → exec → ELF load → dynamic linker → page faults → main → write syscall → page cache → fsync-or-not → exit → SIGCHLD → wait. **Every layer of this track appears in that one sentence.** This document is your proof of understanding
- [ ] **Capstone (optional, big):** work through **Nand2Tetris** parts 1 & 2, or build a small emulator/VM. Closes the loop from transistor to program

---

## Exit criteria for Track 04

- [ ] You built a shell, and you understand every syscall it makes
- [ ] You completed at least the Util, Syscall, Page Tables, Traps, and COW xv6 labs
- [ ] You can explain virtual memory, page faults, and the TLB from first principles
- [ ] You can look at a hung process and reason about *why* it's hung from its state and stack
- [ ] You understand fsync deeply enough that database durability makes obvious sense
- [ ] `what-happens-when.md` is written and you could defend every line of it
