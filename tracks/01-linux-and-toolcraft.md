# Track 01 — Linux & Command-Line Toolcraft

> **Muscle group:** the hands. Everything else in this program is lifted with these tools.
> **Prereqs:** none. Start here.
> **Environment:** WSL2 (Ubuntu) on your Windows box, plus one cheap cloud VM (Hetzner/DigitalOcean/Oracle free tier) that you are allowed to break.

## Why this track

You said you want to be the person who can fix things at 3AM. At 3AM there is no IDE, no
Stack Overflow tab that matches your exact error, and no colleague awake. There is a
terminal on a machine you did not set up. This track is the difference between staring at
that terminal and reading it.

## Equipment

| Resource | Use it for |
|---|---|
| MIT 6.NULL **The Missing Semester of Your CS Education** (missing.csail.mit.edu) | Lectures 1–4, 6, 8, 9. The backbone of this track. |
| **The Linux Command Line** — William Shotts (free PDF) | Reference, chapters as needed |
| Julia Evans zines: *Bite Size Linux*, *Bite Size Networking*, *How Containers Work* | The "oh THAT's what it does" moments |
| `man`, `tldr`, `--help` | Primary source. Get comfortable reading man pages. |
| **Linux Performance** — Brendan Gregg (brendangregg.com) | Phase 4 |

**Proof-of-work rule for this track:** every `Rep` produces a file in `work/01-linux/`.
Scripts get committed. Notes get committed. If it is not committed, it did not happen.

---

## Phase 1 — Foundation (get the movement pattern right)

### Set 1.1 — Shell literacy
- [ ] Watch Missing Semester L1 (Course Overview + Shell) and L2 (Shell Tools & Scripting)
- [ ] Learn the navigation core cold: `cd -`, `pushd/popd`, globbing (`*`, `?`, `[]`, `{a,b}`), `~`, tab completion
- [ ] Understand quoting: single vs double vs backslash vs `$( )`. Know why `rm $file` breaks on spaces
- [ ] Learn the job control set: `&`, `Ctrl-Z`, `fg`, `bg`, `jobs`, `nohup`, `disown`
- [ ] **Rep:** write `bin/backup.sh` that takes a directory, tars it with a timestamped name, and refuses to run if the target exists. Handle spaces in filenames correctly.
- [ ] **Rep:** write a script that is *wrong* about quoting, watch it delete the wrong thing in a sandbox dir, then fix it. You must feel this once.

### Set 1.2 — The filesystem is an API
- [ ] Map the FHS: `/etc /var /usr /opt /proc /sys /dev /tmp /home`. Write one line each on what lives there
- [ ] Permissions: `rwx` for user/group/other, octal notation, `chmod`, `chown`, `umask`
- [ ] Special bits: setuid, setgid, sticky bit. Explain why `/tmp` has the sticky bit and what `passwd` needs setuid for
- [ ] Links: hard vs symbolic. Inodes. Why you cannot hard-link a directory
- [ ] **Rep:** create a hard link and a symlink to the same file, delete the original, explain both outcomes in `notes/links.md`
- [ ] **Rep:** `ls -la /proc/self/fd` — explain every entry you see

### Set 1.3 — Finding things (your "recursively find files" goal)
- [ ] `find`: `-name`, `-type`, `-mtime`, `-size`, `-maxdepth`, `-exec {} \;` vs `-exec {} +`, `-print0`
- [ ] `grep` family: `-r`, `-n`, `-i`, `-v`, `-E`, `-A/-B/-C`, `-l`
- [ ] Regex for real: character classes, anchors, greedy vs lazy, capture groups. Do 30 puzzles on regex101 or regexcrossword.com
- [ ] `xargs`: `-0`, `-n`, `-P` (parallel), and why `find ... | xargs` breaks without `-print0`
- [ ] **Rep:** one-liner that finds every file over 10MB modified in the last 7 days, excluding `node_modules`, sorted by size
- [ ] **Rep:** one-liner that finds every TODO comment in a repo with filename, line number, and author (`git blame` piped in)

### Set 1.4 — Text as the universal interface
- [ ] Pipes and redirection properly: `|`, `>`, `>>`, `2>`, `2>&1`, `&>`, `<`, `<<<`, `/dev/null`
- [ ] Understand that `2>&1 > file` and `> file 2>&1` do different things. Explain why in one sentence
- [ ] `sort`, `uniq -c`, `wc`, `cut`, `tr`, `head`, `tail -f`, `tee`, `column`, `paste`, `comm`
- [ ] `sed` for substitution and deletion; `awk` for field extraction and simple aggregation
- [ ] **Rep:** given any nginx/apache access log (grab a sample), produce top 10 IPs by request count, top 10 404 paths, and requests-per-hour — using only shell tools
- [ ] **Rep:** rewrite that same pipeline as a single `awk` program

### Set 1.5 — Editor floor (you need a survival level of vim)
- [ ] Modes, `hjkl`, `w/b/e`, `0/$`, `gg/G`, `/` search, `dd/yy/p`, `u/Ctrl-R`, `:wq`, `:q!`
- [ ] `.vimrc` with line numbers, sane tabs, and search highlighting
- [ ] **Rep:** edit a config file on a remote box with vim only, no exceptions, and do not rage quit

---

## Phase 2 — Volume (the tools you listed, one at a time)

Do these in order. Each one gets a page in `notes/tools/<tool>.md` with: what problem it
solves, the 5 flags you will actually use, and one real thing you did with it.

### Set 2.1 — Search and navigation speed
- [ ] **ripgrep (`rg`)** — why it beats `grep -r` (gitignore awareness, parallelism). `-t`, `-g`, `--hidden`, `-C`, `--files`
- [ ] **fzf** — fuzzy finding. Wire up `Ctrl-R` history search and `Ctrl-T` file search in your shell
- [ ] **Rep:** build a `fzf` + `rg` function `fif` ("find in files") that greps content and opens the chosen result in your editor at the right line
- [ ] **fd** and **bat** as ergonomic `find`/`cat` replacements (optional but you will like them)

### Set 2.2 — Seeing the machine
- [ ] **htop / btop** — read every column: PID, USER, PRI, NI, VIRT, RES, SHR, S, %CPU, %MEM, TIME+. Know what `S` states mean (R, S, D, Z, T)
- [ ] Explain the difference between VIRT and RES to a junior in `notes/tools/htop.md`
- [ ] Load average: what does `1.7` mean on an 8-core box? Why is it not a percentage?
- [ ] `ps aux` vs `ps -ef`, `pstree`, `top -H` (threads)
- [ ] `free -h`, `df -h`, `du -sh *`, `iostat`, `vmstat 1`
- [ ] **Rep:** write a script that finds the top 5 memory-consuming processes and their full command lines
- [ ] **Rep:** fill a disk to 100% in a VM, then recover it. Find the culprit with `du`. Then do it again where the culprit is a *deleted but still open* file and find it with `lsof +L1`

### Set 2.3 — strace and friends (the superpower)
- [ ] **strace** basics: `strace ls`, `-e trace=openat`, `-f` (follow forks), `-p` (attach), `-c` (summary), `-o` (output file), `-s` (string length)
- [ ] Understand what a syscall IS before going deep (this dovetails with Track 04 Set 1.2)
- [ ] **Rep:** `strace -f -e trace=openat python -c "import json"` — write down every path Python probes and explain the import search order
- [ ] **Rep:** take a program that fails with a useless error message ("Permission denied", no path) and find the exact file it choked on using strace only
- [ ] `ltrace` (library calls), `lsof` (open files/sockets), `/proc/<pid>/` (maps, fd, status, cmdline, environ)
- [ ] **Rep:** dump `/proc/<pid>/maps` for a running process and identify the heap, stack, and shared libraries

### Set 2.4 — Processes, daemons, and services (your "daemon process" goal)
- [ ] Process lifecycle: fork → exec → wait → exit. Zombies and orphans. Who reaps?
- [ ] Signals: SIGTERM vs SIGKILL vs SIGHUP vs SIGINT vs SIGSTOP. Which ones can be caught?
- [ ] What actually makes a daemon: fork twice, `setsid`, chdir `/`, close/redirect fds 0/1/2, write a pidfile
- [ ] **Rep:** write `daemonize.py` (or `.c`) that correctly double-forks and detaches. Verify with `ps -ef` that its PPID is 1 and it has no controlling terminal
- [ ] **Rep:** add signal handling — SIGTERM triggers a clean shutdown, SIGHUP reloads config without restarting
- [ ] **systemd** — unit file anatomy: `[Unit] [Service] [Install]`, `Type=simple/forking/notify`, `Restart=`, `After=`, `WantedBy=`
- [ ] `systemctl start/stop/status/enable/daemon-reload`, `journalctl -u <svc> -f`, `journalctl --since "1 hour ago"`
- [ ] **Rep:** ship your daemon as a systemd service that auto-restarts on crash. Kill -9 it and watch systemd bring it back
- [ ] **pm2** — the Node-world equivalent. `start/list/logs/restart/save/startup`, cluster mode, ecosystem file
- [ ] **Rep:** run the same app under both systemd and pm2. Write 5 lines in `notes/tools/pm2.md` on when you'd pick which
- [ ] `cron` / `systemd timers`: syntax, `crontab -e`, why cron jobs fail (no PATH, no env, no TTY) and how to debug them

### Set 2.5 — Moving data and remote work
- [ ] **ssh**: keys vs passwords, `~/.ssh/config` (Host aliases, IdentityFile, ProxyJump), agent forwarding and why it's risky
- [ ] `ssh -L` local forward, `-R` remote forward, `-D` SOCKS proxy. Draw all three in `notes/tools/ssh-tunnels.md`
- [ ] **Rep:** reach a database on a private network from your laptop using only an SSH tunnel through a bastion
- [ ] **rsync** — the flags that matter: `-a`, `-v`, `-z`, `-P`, `--delete`, `--dry-run`, `--exclude`, `--exclude-from`, `-e ssh`, `--bwlimit`, `--partial`
- [ ] Understand `src/` vs `src` (trailing slash). Get this wrong once in a sandbox so you never do it again
- [ ] **Rep:** build `deploy.sh` that rsyncs a project to your VM, excludes `.git`/`node_modules`/`.env`, does a `--dry-run` first and asks for confirmation, then logs the run with a timestamp to `deploy.log`
- [ ] **Rep:** build `pull-logs.sh` that rsyncs remote logs down incrementally (resumable, compressed) and rotates local copies
- [ ] `scp` vs `rsync` vs `sftp` — when each is right
- [ ] **tmux**: sessions/windows/panes, detach/attach. Why this matters when your SSH drops mid-migration
- [ ] **Rep:** start a long job in tmux, kill your network, reconnect, and find it still running

### Set 2.6 — Logs and the things that generate them
- [ ] Where logs live: `/var/log/`, journald, app-local. `dmesg` for kernel
- [ ] `logrotate` — config anatomy, why unrotated logs kill servers
- [ ] Log levels and structured logging: why `logger.info(f"user {id} failed")` is worse than structured JSON
- [ ] **Rep:** instrument your daemon with structured logs, ship them to a file, rotate with logrotate, and write one `jq` query that answers "how many errors in the last hour, grouped by error type"
- [ ] `jq` fundamentals: `.`, `.[]`, `select()`, `map()`, `group_by`, `-r`

### Set 2.7 — The question you asked: why GUI apps don't open over SSH
- [ ] Read up on X11: the X server, the X client, `$DISPLAY`, and why the naming feels backwards
- [ ] Wayland vs X11, and why `xeyes` over SSH is a different problem than `firefox` over SSH
- [ ] `ssh -X` vs `ssh -Y`, `xauth`, and the security tradeoff
- [ ] **Rep:** SSH into your VM, run `xclock` and capture the exact error. Then `ssh -X` and make it work. Write the full explanation in `notes/why-gui-over-ssh.md` — cover $DISPLAY, the client/server inversion, and the X protocol over a TCP/unix socket
- [ ] **Bonus rep:** explain why this is different from a headless server that has *no* X server at all, and what `xvfb` does about it

---

## Phase 3 — Strength (compose the tools into real capability)

### Set 3.1 — Shell scripting that doesn't embarrass you
- [ ] `set -euo pipefail` and what each flag prevents
- [ ] Functions, `local`, arrays, `[[ ]]` vs `[ ]`, arithmetic `(( ))`
- [ ] Argument parsing with `getopts`, usage/help text, exit codes that mean something
- [ ] Traps: `trap cleanup EXIT INT TERM` for temp-file cleanup
- [ ] **shellcheck** — run it on every script you have written so far and fix every warning
- [ ] **Rep:** rewrite your Phase 1 `backup.sh` to production quality: strict mode, arg parsing, trap cleanup, logging, dry-run flag, exit codes, shellcheck-clean
- [ ] Know where bash ends: if it's over ~100 lines or needs data structures, switch to Python

### Set 3.2 — Users, packages, networking basics on a box
- [ ] Users and groups, `sudo` and `/etc/sudoers`, `su -` vs `sudo -i`
- [ ] Package managers: `apt` (dpkg), what a PPA is, why `apt` and `pip install` fighting over the same package is a real problem
- [ ] `ss -tulpn` (who's listening), `ip addr`, `ip route`, `ping`, `traceroute`, `dig`
- [ ] Firewall floor: `ufw` / `iptables -L`. Know enough to not lock yourself out
- [ ] **Rep:** provision a fresh VM from scratch: non-root user with sudo, SSH key-only auth, password auth disabled, ufw allowing only 22/80/443, fail2ban installed. Document every step in `notes/vm-hardening.md`
- [ ] **Rep:** now write that entire provisioning as one idempotent script you can rerun safely

### Set 3.3 — Understanding what a "distribution" is
- [ ] Boot sequence at a high level: BIOS/UEFI → bootloader → kernel → init (systemd) → getty/login
- [ ] Kernel vs userspace. Where the line is. What `uname -a` is telling you
- [ ] `/etc/environment`, `.bashrc` vs `.bash_profile` vs `.profile` — which runs when, and why your PATH works interactively but not in cron
- [ ] **Rep:** debug a "works in my shell, fails in cron" problem end to end and write up the root cause

---

## Phase 4 — Peak (3AM readiness drills)

These are *drills*, not reading. Set them up, break them, fix them under time pressure.
Log each one in `work/01-linux/drills/<name>.md` with symptom → hypotheses → investigation → root cause → fix → what you'd add to prevent it.

- [ ] **Drill: the disk is full.** Service down, `df` shows 100%. Find and fix. Variant: the space is held by a deleted-but-open file
- [ ] **Drill: the port is taken.** "Address already in use." Find the process, understand TIME_WAIT, decide whether to kill or wait
- [ ] **Drill: the process is a zombie.** Understand why kill -9 does nothing and what actually fixes it
- [ ] **Drill: CPU is at 100%.** Identify the thread, not just the process. Use `top -H` and then get a stack
- [ ] **Drill: the box is out of memory.** Read the OOM killer message in `dmesg`. Explain the oom_score
- [ ] **Drill: "it's slow."** Walk Brendan Gregg's USE method and his 60-second checklist. Memorize the checklist
- [ ] **Drill: too many open files.** Hit the fd limit, read `ulimit -n`, fix it properly (systemd `LimitNOFILE`, not just `ulimit` in a shell)
- [ ] **Drill: clock skew.** Break NTP, watch something downstream fail, fix it
- [ ] **Drill: the config change that didn't take.** Service reloaded but old behavior persists. Find out why (cached, wrong file, wrong unit, SIGHUP not handled)
- [ ] **Capstone:** write `notes/3am-runbook.md` — your personal triage checklist, in the order you'd actually run it, with the exact commands. This is the artifact that makes you the person they call.

---

## Exit criteria for Track 01

You can mark this track done when all of the following are true:

- [ ] You can drive a bare Linux box over SSH with no GUI and no notes, comfortably
- [ ] Given a misbehaving process, you can determine what it is doing without its source code
- [ ] You have a shellcheck-clean script library in `work/01-linux/bin/` that you actually use
- [ ] Your `3am-runbook.md` exists and you have used it at least twice on a real problem
- [ ] You can explain fork/exec/wait, file descriptors, and signals without hedging
