# Track 02 — Git (to actual mastery, not memorized commands)

> **Muscle group:** grip strength. You touch it every day; weakness here compounds forever.
> **Prereqs:** Track 01 Phase 1.
> **Core idea:** stop memorizing commands. Learn the object model, and every command becomes obvious.

## Why this track

Most engineers know six git commands and panic at the seventh. The difference between
"knows git" and "is the person the team asks" is one thing: understanding that git is a
content-addressed key-value store with a DAG on top, and that almost every command is just
moving refs around. Once you see that, `reflog`, `rebase`, `cherry-pick`, and `bisect` stop
being scary incantations.

## Equipment

| Resource | Use it for |
|---|---|
| **Git Magic** — Ben Lynn (you asked for this) | Fast, opinionated mental model. Read it start to finish in one sitting. |
| **Pro Git** — Chacon & Straub (free) | Ch. 2, 3, 5, 6, 7, and **Chapter 10 (Internals) — the important one** |
| MIT Missing Semester **Lecture 6: Version Control** | Best 1-hour explanation of the data model in existence |
| **Learn Git Branching** (learngitbranching.js.org) | Interactive drills, all levels including remote |
| **Oh Shit, Git!?!** (ohshitgit.com) | Recovery cookbook |
| **Build Your Own Git** (CodeCrafters / write-yourself-a-git) | Phase 3 capstone |

**Practice repo:** create `work/02-git/sandbox/` — a throwaway repo you are free to destroy.
Every dangerous experiment happens there first.

---

## Phase 1 — Foundation (the data model)

### Set 1.1 — The three trees
- [ ] Read Git Magic cover to cover
- [ ] Watch Missing Semester L6
- [ ] Draw the diagram yourself: working directory ↔ index (staging) ↔ HEAD/repository. Save as `notes/three-trees.md`
- [ ] Understand exactly what each does: `git add`, `git restore`, `git restore --staged`, `git commit`, `git checkout <file>`
- [ ] `git status` and `git diff` vs `git diff --staged` vs `git diff HEAD` — know which pair of trees each compares
- [ ] **Rep:** stage a file, modify it again, then `git diff` and `git diff --staged` and explain why they differ

### Set 1.2 — Objects (this is the whole thing)
- [ ] Read **Pro Git Chapter 10.1–10.3** (Plumbing and Porcelain, Git Objects, Git References)
- [ ] The four object types: **blob**, **tree**, **commit**, **tag**. Know what each contains
- [ ] **Rep:** in your sandbox, run `git hash-object -w`, `git cat-file -t`, `git cat-file -p` on a blob, a tree, and a commit. Paste the raw output into `notes/git-objects.md` and annotate every field
- [ ] **Rep:** walk an entire commit by hand: `git cat-file -p HEAD` → get the tree hash → `git cat-file -p <tree>` → get a blob → print it. No porcelain commands allowed
- [ ] Explore `.git/` directory: `HEAD`, `refs/heads/`, `refs/remotes/`, `objects/`, `index`, `config`, `packed-refs`, `ORIG_HEAD`
- [ ] **Rep:** `cat .git/HEAD`, `cat .git/refs/heads/main`. Explain what a branch *is* in one sentence. (Answer should be ~9 words.)
- [ ] Understand why identical content in two files = one blob. Content addressing
- [ ] `git gc`, packfiles, and why `.git` shrinks

### Set 1.3 — Refs, HEAD, and revision syntax
- [ ] `HEAD`, detached HEAD — what it means and how to get out of it safely
- [ ] Revision syntax: `HEAD~3`, `HEAD^`, `HEAD^2`, `main@{2}`, `main@{yesterday}`, `<sha>`
- [ ] Know precisely how `~` differs from `^` on a merge commit. Draw it
- [ ] Ranges: `A..B`, `A...B`, and how they differ for `log` vs `diff`
- [ ] **Rep:** on a repo with a merge, use `git log --oneline --graph --all` and predict the output of `git log main..feature` before running it

---

## Phase 2 — Volume (daily-driver fluency)

### Set 2.1 — Branching and merging
- [ ] Complete **Learn Git Branching** — Main sequence, all levels
- [ ] Fast-forward vs three-way merge. When git can and cannot fast-forward
- [ ] `git merge --no-ff` and why some teams mandate it
- [ ] **Conflict resolution for real:** conflict markers, `git diff` during a conflict, `--ours` vs `--theirs` (and how those flip during a rebase)
- [ ] **`git merge --abort`** — your escape hatch. Also `git rebase --abort`, `git cherry-pick --abort`
- [ ] `git mergetool` and configuring VS Code as your merge tool
- [ ] `git rerere` — record and reuse conflict resolutions. Turn it on
- [ ] **Rep:** deliberately create a 3-file conflict in your sandbox, resolve it, then `--abort` a second identical one. Do this 5 times until conflicts feel boring

### Set 2.2 — Rewriting history
- [ ] `git commit --amend` (and the rule: never amend something you've pushed to a shared branch)
- [ ] `git rebase <branch>` — what actually happens to commit SHAs and why
- [ ] **`git rebase -i`** — `pick`, `reword`, `edit`, `squash`, `fixup`, `drop`, reorder
- [ ] `git commit --fixup <sha>` + `git rebase -i --autosquash` — the pro workflow
- [ ] **`git cherry-pick`** — single commit, ranges, `-x` to record provenance, `-n` to not commit
- [ ] When cherry-pick is right vs when it's a smell (duplicated commits across branches)
- [ ] `git revert` vs `git reset` — and the rule for public history
- [ ] `git reset --soft` / `--mixed` / `--hard` — map each one onto the three trees. This is the test of Set 1.1
- [ ] **Rep:** take a 6-commit branch with messy WIP commits and interactive-rebase it into 3 clean, reviewable, atomic commits with good messages
- [ ] **Rep:** cherry-pick a bugfix from `main` onto a release branch, resolve the conflict it causes, verify with `git log --cherry-mark`

### Set 2.3 — Recovery (the confidence unlock)
- [ ] **`git reflog`** — what it records, how long entries live (90 days default), `git reflog show <branch>`
- [ ] **Rep:** `git reset --hard` away 3 commits, then recover every one of them using reflog
- [ ] **Rep:** delete a branch entirely, then resurrect it from reflog
- [ ] **Rep:** lose a commit during a botched rebase, recover it
- [ ] **Rep:** recover an *unstaged* change — prove to yourself it's gone, and learn the one case where `git fsck --lost-found` saves you (stashed/added-then-lost blobs)
- [ ] `git stash`, `git stash list/pop/apply/drop/show -p`, `git stash -u` (untracked), `git stash branch`
- [ ] Know the trap: `git stash pop` on a conflict does *not* drop the stash
- [ ] Work through **Oh Shit, Git!?!** — do every scenario in your sandbox
- [ ] **Rep:** write `notes/git-recovery.md` — your own recovery playbook for the 8 scenarios you're most likely to hit

### Set 2.4 — Working with remotes
- [ ] `origin` is just a name. `git remote -v`, `add`, `rename`, `set-url`
- [ ] `git fetch` vs `git pull` vs `git pull --rebase`. Configure `pull.rebase=true` and explain why
- [ ] Remote-tracking branches: `origin/main` is a *local* ref. Why it goes stale
- [ ] `git push -u`, `git push --force-with-lease` (and why never plain `--force`)
- [ ] `git remote prune origin`, `git fetch --prune`
- [ ] Fork + upstream workflow, PR etiquette, `git request-pull`
- [ ] **Rep:** simulate a team: clone your sandbox to a second directory, make conflicting pushes, resolve as both "developers"

### Set 2.5 — Investigation
- [ ] **`git blame`** — `-L` line ranges, `-w` ignore whitespace, `-C` detect moved code, `--ignore-rev` + `.git-blame-ignore-revs` for reformat commits
- [ ] `git log` mastery: `-S` (pickaxe: when was this string added/removed), `-G` (regex), `--follow`, `-p`, `--author`, `--since`, `--grep`, `--stat`, `--format=`
- [ ] **`git bisect`** — `start/bad/good/reset`, and `git bisect run <script>` for full automation
- [ ] **Rep:** plant a bug 40 commits deep in your sandbox, write a test script that exits nonzero on the bug, and let `git bisect run` find it automatically
- [ ] **Rep:** use `git log -S "functionName"` to find when a function was introduced and deleted in a real open-source repo
- [ ] `git shortlog -sn`, `git log --graph --all --oneline --decorate` as your default alias

---

## Phase 3 — Strength

### Set 3.1 — Power tools
- [ ] **`git worktree`** — multiple branches checked out simultaneously, no stashing. `add`, `list`, `remove`
- [ ] **Rep:** use a worktree to review a PR while keeping your feature work untouched. Never stash for this again
- [ ] `git submodule` vs `git subtree` — the tradeoffs, why submodules hurt, when they're still right
- [ ] Hooks: `pre-commit`, `commit-msg`, `pre-push`. Where they live, why they aren't versioned by default
- [ ] **Rep:** write a `pre-commit` hook that runs your linter and blocks commits with debug statements
- [ ] Set up the **pre-commit** framework on a real project
- [ ] `.gitignore` precedence rules, `.gitattributes` (line endings — relevant on Windows, `text=auto`, diff drivers for binary formats)
- [ ] `git sparse-checkout` and shallow clones (`--depth`) for huge repos
- [ ] `git filter-repo` — removing a leaked secret from all of history (and why you must rotate the secret anyway)
- [ ] **Rep:** commit a fake API key, then scrub it from history with `filter-repo` and verify it's unreachable

### Set 3.2 — Workflow and team craft
- [ ] Compare trunk-based development vs GitFlow vs GitHub Flow. Write which you'd advocate for and why in `notes/git-workflows.md`
- [ ] Commit message discipline: Conventional Commits, the 50/72 rule, "why not what"
- [ ] **Rep:** rewrite your last 10 commit messages (in the sandbox) to be genuinely useful to someone reading them in 2 years
- [ ] Atomic commits: one logical change each. Practice `git add -p` (patch mode) — `y/n/s/e`
- [ ] **Rep:** take a messy working directory with 3 unrelated changes and split it into 3 clean commits using only `git add -p`
- [ ] Code review: what makes a reviewable PR. Read Google's *Code Review Developer Guide*

### Set 3.3 — Build it to understand it
- [ ] **Capstone:** implement a minimal git in Python or Go. Required commands: `init`, `hash-object`, `cat-file`, `write-tree`, `commit-tree`, `log`
- [ ] Your implementation must produce SHAs **byte-identical** to real git for the same content. This is the test that proves you understood the object format
- [ ] Bonus: implement `clone` against a real remote (smart HTTP protocol). CodeCrafters' Build Your Own Git has this stage

---

## Phase 4 — Peak (drills)

Time yourself. These should be reflexes, not research projects.

- [ ] **Drill:** "I committed to the wrong branch." Move the last 2 commits to a new branch. Under 60 seconds
- [ ] **Drill:** "I force-pushed over a colleague's work." Recover it from reflog / `origin/main@{1}`
- [ ] **Drill:** "The merge conflict is in a lockfile." Resolve correctly (regenerate, don't hand-merge)
- [ ] **Drill:** "This line is wrong. Who wrote it and why?" Blame → commit → PR → linked issue, in under 3 minutes
- [ ] **Drill:** "Production broke sometime this week." Bisect to the commit
- [ ] **Drill:** "I need to undo a merge that's already on main." `git revert -m 1`, and understand why re-merging later is then broken
- [ ] **Drill:** "Rebase went wrong halfway through, 8 commits in." Abort, or recover mid-rebase with `ORIG_HEAD`
- [ ] **Drill:** detached HEAD with 3 commits on it. Save them to a branch

---

## Exit criteria for Track 02

- [ ] You can explain what a commit object contains, byte for byte
- [ ] Nothing in git can make you lose work, and you know why
- [ ] Interactive rebase is routine, not an event
- [ ] Your mini-git produces real git SHAs
- [ ] You can teach the data model to someone else on a whiteboard in 15 minutes
