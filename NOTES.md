# Assignment 1.1 - NOTES.md
## Part 1 - Written decisions
### Question 1 - What is worth its own commit?

** Category A: 
Adding a new feature: High-value because features should be reviewable on their own. A teammate can review only the search commits without having to look at the earlier setup work.

Resolving a real merge conflict: High-value because the resolution itself is a decision. Keeping it as its own commit shows exactly how the conflict was settled and makes the history honest.

Bug fixes: It is kept separate from feature work, so a fix can be cherry picked or reverted independantly of the feature it was found in.

Data changes: Data chenges often need dedicated review attention

Pure code refactoring: Refactoring carries a high risk of accidentally introduding regression bugs.

Category B: 
Fixing a one character typo right after introducing it: It should be bundled Splitting it into its own step creates an extra, tiny entry that adds no real information, which just creates unnecessary clutter for anyone reviewing your progress.

Removing  a temporary display command you just added: These fxes should be grouped rigt into the main task. Because these notes are only used for quick troubleshooting while you work, saving them as their own separate steps clutters your project's history.

Formatting changes: They should be ggrouped together on their own. Since they only fix how the text looks and do not change how the program actually works so mixing them with real changes makes it confusing to look back through your project's history later.

Category C
I'm ignoring .env, which in this project holds a password for accessing an interface or system that only I should be able to reach no one else on a team, and definitely not anyone who finds the public repo, should have that credential. I'm using a dummy placeholder value in the actual file for example: INTERFACE_PASSWORD=dummy-fake-value-123 to safely demonstrate the protection without risking a real credential. I'm also ignoring *.log for any generated output files.

If .env were committed and later needed removing, deleting it in a new commit wouldn't be enough the real password would still sit in every earlier commit in the repo's history, retrievable by anyone with access to the repo or a clone of it simply by checking out an old commit. Properly removing it requires rewriting history, then force-pushing and everyone who already cloned the repo would need to be told to re-clone, since their local copy still has the old, secret-containing history and could resurrect it if they ever pushed from it.

Beyond the technical cleanup, if this were a real credential and not a dummy value, the damage wouldn't be undone just by scrubbing git history the password itself would need to be rotated/changed on the actual system, since anyone who saw the repo before the scrub including automated bots that scan public GitHub repos for exposed secrets could already have copied it. A teammate or in this case, anyone who ever had repo access would reasonably no longer trust that old credential as safe, regardless of what the current git history shows.

## Question 2 - Merge vs Rebase
Merge: This method keeps the exact story of how your project was built. You can easily see when a teammate started working on their own, how long they worked on it, and the exact moment their work was combined back into the main project. It discards nothing, but it leaves behind extra "connection notes" that can make the project's history list look a bit messy and harder to read.

Rebase: It discards the true timeline, it rewrites commit as if they'd been written sequentially on top of the latest main, which is a fiction. What you gain is a clean, linear, easy to read history with no merge commit noise.

For what I'd use for part 3 is Merge because the whole point of that the task is to prove a conflict genuinely happened, and a merge commit is the one artifact that visibly records "these two histories diverged and were reconciled here."

## Question 3 - Remote operations inventory
git push -u origin main: Sends my local commits to GitHub and sets up upstream tracking. On GitHub's side, the new commits appear on main, and locally, my branch now knows to talk to origin/main automatically for future push/pull.

git push origin feature/add-search: sends the commits on my feature branch. On GitHub, a new branch appears in the repo, visible under the branches list.

git push origin --delete feature/add-search: sends a request to delete that branch reference. On GitHub, the branch disappears from the repo entirely.

git fetch: receives any new commits/refs from GitHub without touching my working files. Nothing changes on GitHub's side at all this is read-only; it only updates my local remote-tracking refs like origin/main so I can see what's changed before deciding what to do.

git pull --rebase origin main: fetches from GitHub, then replays my local commits on top of whatever's there. Nothing changes on GitHub's side; only my local history is rearranged.

git push: sends my rewritten commits up. GitHub's commit list updates to match my new, replayed history.

What pushing can't verify: whether your commits are logically atomic or your messages are meaningful. Git will happily accept a push where you crammed five unrelated changes into one commit, or wrote "asdasd" as a message the push succeeds with zero errors either way. Pushing only checks that the ref history is valid and connects properly; it says nothing about the quality of your commit boundaries or messages, which is a purely human judgment.

## Question 4 - Commit message as specification
a. fixed stuff: Non-descriptive. It says nothing about what was broken or what now works.
Rewrite: Fix crash when team list is empty

b. Update index.js: Non-descriptive. It just names the file that changed, not what changed about it or why.
Rewrite: Add pagination to team member list view

c. WIP: Non-descriptive, and not really a record of behaviour at all it just flags an unfinished state.
Rewrite: Add initial skeleton for search feature (incomplete) though ideally this kind of commit shouldn't be pushed to shared history until it represents a coherent unit of work.

d. Add email format validation so invalid addresses cannot be submitted. Already intent/behaviour-focused. This is the good example no rewrite needed, keep as it is.

e. asdasd: Meaningless, gives zero information.
Rewrite: Add phone number format validation.

f. Changed line 47 of notes.md: Implementation minutiae it describes where the change happened, not what changed or why it mattered.
Rewrite: Clarify setup instructions in notes.md

Diff 1 before staging team_directory.py: The diff showed the old placeholder line (print("Team Directory - coming soon")) being removed, and new content added: an import json statement, a load_team() function that opens and parses team.json, and a display_team() function that loops through the team members and prints each one's name, role, and email. This confirmed the script now actually reads real data instead of just printing a placeholder message, before I committed it.

## Part 3
Task 5: The merge of feature/add-search into main was a fast-forward. I knew because Git's own output explicitly said "Fast-forward" when I ran git merge feature/add-search, and no merge commit was created main simply moved forward to point at the branch's latest commit. This happened because no new commits had been made on main since I created the branch, so there was no divergence for Git to reconcile.

Task 7: 
The conflict happened because I edited the same line of README.md on two branches (main and feature/readme-update) starting from the same original content, so Git had no way to automatically decide which version was correct. I resolved it by combining both edits into a single sentence that captured the intent of both versions, then removed the conflict markers and completed the merge commit.

Task 9:
Comparing the two in git log --oneline --all --graph: the Task 4/7 merge conflict resolution shows a diamond shape two lines diverging from a common commit and rejoining at a merge commit with two parents. The Task 9 rebase shows a straight line instead the branch's commit was rewritten to sit directly on top of main's latest commit, so there's no visible divergence at all, even though the work was originally done in parallel. I'd choose merge when I want the history to honestly reflect that work happened concurrently, and rebase when I want a clean, linear log for a short-lived branch where the parallel timeline isn't important to preserve.


When I tried to push locally after making a commit while GitHub already had a newer commit from a direct web edit simulating a teammate, the push was rejected with a "fetch first" error, since my local main didn't include that newer commit as an ancestor. I ran git pull --rebase, which fetched the remote commit and replayed my local commit on top of it. This caused a real conflict since both edits touched README.md, so I resolved the conflict markers manually, staged the file, and ran git rebase --continue to complete it. git pull --rebase was the correct recovery because it preserves a clean, linear history and doesn't overwrite the teammate's (GitHub) commit — force-pushing instead would have discarded that commit entirely, permanently losing their work.


When I tried to push a local commit while GitHub already had a newer commit (simulating a teammate's direct web edit), the push was rejected with a "fetch first" / non-fast-forward error, since my local main didn't include that commit as an ancestor. I ran git pull --rebase, which replayed my local commit on top of the remote one this caused a real conflict in README.md since both edits touched the same area, so I resolved it manually, staged the file, and continued the rebase. Along the way I also had to clean up a commit that still had leftover conflict-marker artifacts, using git commit --amend since it hadn't diverged from GitHub in a breaking way. git pull --rebase was the correct move here rather than force-pushing, because force-pushing would have thrown away the "teammate's" commit entirely pull --rebase integrates both changes instead of discarding either one.