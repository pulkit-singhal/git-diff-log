from termcolor import colored
from githelper import GitHelper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("first")
parser.add_argument("second")
parser.add_argument("-c", nargs = "?", type = int)
parser.add_argument("-r", action = "store_true")
args = parser.parse_args()

print(colored("Starting Git-Diff-Log", "green"))
print("Searching for Git Repo in", args.directory)

git = GitHelper(args.directory)
git.validate_branches_are_present(args.first, args.second)

commits_in_first = git.commits(args.first, max_count = args.c)
commits_in_second = git.commits(args.second)

different_commits = git.different_commits(commits_in_first, commits_in_second)
different_commits.sort(key = lambda commit: commit.authored_date)

for commit in different_commits:
	if git.should_print_commit(commit):
		git.print_commit_info(commit)
		git.resolve_commit(commit, args.r)