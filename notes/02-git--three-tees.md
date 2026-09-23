

I am currently into Git-magic intial chapter , where git reset are learnt 
## Introduction

*working-tree* - files on disk in local repository
*pull* - 
“Pull from a branch” = fetch their history
“Pull into a branch” = merge that history into your current branch
*origin* - “origin” is a nickname given to the source repository
*upstream* - linkage of local branch and remote tracking branch (the river your branch's commits flow to/from. Set it with git push -u origin main once; after that git remembers)

## Three trees
Git always has three snapshots of the project
 What will be commited

### Working Tree
- This is where we edit files
- We can use `git restore`

Working tree
├── tracked files
│   ├── modified
│   └── deleted
└── untracked files

### Staging
- What will be commited

### HEAD
- The commit you are on

When we use `git status` , it just compares working tree and index and this can be done by git diff
Index =/ HEAD -> staged changes and the last commit (`git diff --staged`)
Working tree =/ HEAD -> all uncommited work (`git diff HEAD`)

ORIG_HEAD --> is the present future , if we use `git reset HEAD~3` it will move the head back to past but this will not show the recent commit so ORIG_HEAD is the pointer to the original HEAD 


## git reset

```
git status -v
On branch code-beauty
On branch code-beauty
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   app.py

no changes added to commit (use "git add" and/or "git commit -a")
```


```
vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (code-beauty)
$ git add app.py 

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (code-beauty)
$ git status
On branch code-beauty
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   app.py


```
`git reset --soft` is not doing anything to a staged changes 


`git reset --mixed` unstages the changes but it retains the changes in our local tree otherwise called working directory

```
vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (code-beauty)     
$ git reset --mixed
Unstaged changes after reset:
M       app.py

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (code-beauty)     
$ git status
On branch code-beauty
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   app.py

no changes added to commit (use "git add" and/or "git commit -a")
```

`git reset --hard` will unstages , and its kind of hard reset and cannot able to retain the new uncommited change we done to our working directory 


### git reset --hard to a previous old commit 
git reset--hard: load an old save and delete all saved games newer
than the one just loaded.

So I have done like this , I created 5 commits like the below

```
$ git log
commit 3dfe6cbd3dfab8293f2314790866c29f11eee67e (HEAD -> code-beauty)
Author: vasanthan <sr.vasanthan@blackstraw.ai>
Date:   Tue Sep 22 13:45:24 2026 +0530

    happy feet 5

commit d47213639be0e486a16a4fe1d9ec1c0f1fca98eb
Author: vasanthan <sr.vasanthan@blackstraw.ai>
Date:   Tue Sep 22 13:44:47 2026 +0530

    happy feet 4

commit 35841d87284c954f272b7c6db19b32e2cc91dfb3
Author: vasanthan <sr.vasanthan@blackstraw.ai>
Date:   Tue Sep 22 13:44:17 2026 +0530

    happy feet 3

commit 193782d61f5c39edb5beca7fc72ad5cde74489ce
Author: vasanthan <sr.vasanthan@blackstraw.ai>
Date:   Tue Sep 22 13:44:00 2026 +0530

    happy feet 2

commit 01ad292acb352d197e976d71fc2093ff2c94c7e6
Author: vasanthan <sr.vasanthan@blackstraw.ai>
Date:   Tue Sep 22 13:26:22 2026 +0530

    happy feet

commit d6eef4f81820f3176d4cce07d9c0c65ca4c8b895 (master)
```

*So the commits newer that the commit which we had went are lost*

```
vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (code-beauty)     
$ git reset --hard 19378
HEAD is now at 193782d happy feet 2

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (code-beauty)     
$ git log --oneline
193782d (HEAD -> code-beauty) happy feet 2
01ad292 happy feet
d6eef4f (master) Modify dbUtil which returns the age
7c002df Created a simple dbUtil file
baf3062 Initial Commit

```

Git Reset in a nutshell 

-- soft 
Keeps all the changes 

--mixed or git reset
```
vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (newest)
$ git status
On branch newest
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        helpers/tooling.py
        helpers/util.py

nothing added to commit but untracked files present (use "git add" to track)

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (newest)
$ git add helpers/tooling.py helpers/util.py 

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (newest)
$ git status
On branch newest
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   helpers/tooling.py
        new file:   helpers/util.py


vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (newest)
$ git reset

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (newest)
$ git status
On branch newest
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        helpers/tooling.py
        helpers/util.py

nothing added to commit but untracked files present (use "git add" to track)

vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo (newest)
$
```

-- hard
affects working tree

## git checkout

`git checkout master` is time travelling to the present timeline


To retrieve a file from a previous commit 

git checkout <hash> -- <file_name>
## git diff

*What must change to make the tree look like*

`git diff`
compares working tree vs staging area , but if we staged changes then it will be blank even if we have uncommited changes

`git diff HEAD~2`
this compares 


```
vasanthan.sr@Vasanthan-SR MINGW64 /d/New folder/utils/cursor-playground/git-learns/test-repo ((253bda2...))
$ git-logload
* 253bda2 (HEAD) B_Removed files
* 2413061 Refatored models folder | removed util.py under helpers
* e745833 C_Commit add Department class
* c12a615 B_Commit add address
* 2f5cc45 Added designation
| * b9df234 (sentinel) adding requiremnts and models
| | * 77e78b4 (roger-that) Add Scraper utility under utils
| |/
| * 64f9b29 (code-beauty) Added happy feets
|/  
* 193782d happy feet 2
* 01ad292 happy feet
* d6eef4f (master) Modify dbUtil which returns the age
| * 1405b5b (refs/stash) WIP on code-beauty: 7c002df Created a simple dbUtil file
|/| 
| * c95b5df index on code-beauty: 7c002df Created a simple dbUtil file
|/
* 7c002df Created a simple dbUtil file
* baf3062 Initial Commit
```

git diff 253b 2413 does not mean “show what 253b changed.” It means:
same as git diff 2413 253b
`git diff 2413..253b`

“Start at 253b. What must change to make the tree look like 2413?”

### git show

git show is same as diff but internally it is doing like git diff <commit~1> <commit>

### Restoring files from previous commit to a new commit 


* a7d9cf8 (HEAD) Added manager in models/department
* 253bda2 B_Removed files
* 2413061 Refatored models folder | removed util.py under helpers


## git blame

` git blame bug.c` 
List all the line in the file and who changed what

# Changing History 

## git rebase
topic:> git rebase master 

now origin of the topic branch will sit on the top of master branch 
if ever conflict happens we have to git diff to find the markers and edit the conflict and by telling `git add` it will resolve the commit 
to find the `git rebase --continue` 

To stop the git rebase
`git rebase --abort`

to skip the commit 
`git rebase --skip`

## git reflog

Finding HEAD
You could look at all the hash values in .git/objects and use trial and error
to find the one you want.

Git stores all the commit hashes in .git/logs , it contains the history of all activies and file HEAD shows every hash it taken , `git reflog` provides a nice interface to these files



# Misc
## git bundle
` git bundle create somefile HEAD`

## git stash


`git stash push -u -m "message"`
this will put the stashed change named Message and can we recovered using the stash number 
`git stash pop stash@{0}`

## git clean
`git clean-f-d`
To delete untracked files 

## 3 R's - restore, revert, reset

restore - good
it overwrites files in the working tree or Index by pulling content , it just file-content copy operation *nothing touched*
`git restore <file>` -> from 
`git restore --staged <file>` -> Unstage , keep working tree edits
`git restore --source=<hash> <file> -> Bring the file from source hash to Working tree 
this is same as `git checkout <hash> -- <file>


revert - bad
`git checkout -b new-branch`     # branch off from wherever you want the undo to live
`git revert <commit-hash>`
reach into any point in time, grab one file's version, and drop it into the presen

reset - ugly
it's "moving where 'now' is." The branch pointer relocates to an earlier commit

## Daring stunts
`git checkout -f HEAD^` - It will checkout a given commit , and destroys any changes 
## Doubts

- git cherry-pick  (try and implement this one )
- git stash
- difference between git branching and cloning
- Once i altered the history like using rebase , cherry pick , can I revert it 
    why to alter the history 
- filter-branch 

