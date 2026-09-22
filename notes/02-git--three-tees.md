

I am currently into Git-magic intial chapter , where git reset are learnt 
## Introduction

*working-tree* - files on disk in local repository
*pull* - 
“Pull from a branch” = fetch their history
“Pull into a branch” = merge that history into your current branch

## Three trees
Git always has three snapshots of the project
 What will be commited

### Working Tree
- This is where we edit files
- We can use `git restore` 

### Staging
- What will be commited

### HEAD
- The commit you are on

When we use `git status` , it just compares working tree and index and this can be done by git diff
Index =/ HEAD -> staged changes and the last commit (`git diff --staged`)
Working tree =/ HEAD -> all uncommited work (`git diff HEAD`)


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

## git checkout

`git checkout master` is time travelling to the present timeline

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
# same as git diff 2413 253b
`git diff 2413..253b`

“Start at 253b. What must change to make the tree look like 2413?”

### git show

git show is same as diff but internally it is doing like git diff <commit~1> <commit>

### Restoring files from previous commit to a new commit 


* a7d9cf8 (HEAD) Added manager in models/department
* 253bda2 B_Removed files
* 2413061 Refatored models folder | removed util.py under helpers




