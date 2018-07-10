from git import Repo
from git.exc import NoSuchPathError
from termcolor import colored
from hashstore import HashStore
import argparse
import sys
import time

ignoredHashes = HashStore()

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("first")
parser.add_argument("second")
parser.add_argument("-c", nargs = "?", type = int)
parser.add_argument("-r", action = "store_true")
args = parser.parse_args()

print(colored("Starting Git-Diff-Log", "green"))
print("Searching for Git Repo in", args.directory)
try:
	repo = Repo(args.directory)
except NoSuchPathError as e:
	print(colored("Specified directory does not exists", "red"))
	sys.exit(0)

if repo.bare:
	print(colored("The directory does not contains the .git folder", "red"))
	sys.exit(0)

branches = [branch.name for branch in repo.branches]
if args.first not in branches or args.second not in branches:
	print(colored("Specified branches does not exists", "red"))
	sys.exit(0)

if args.c:
	commitsInFirst = list(repo.iter_commits(args.first, max_count=args.c))
else:
	commitsInFirst = list(repo.iter_commits(args.first))
commitsInSecond = list(repo.iter_commits(args.second))

def printCommitInformation(commit):
	print(colored("commit {}".format(commit.hexsha), 'yellow'))
	print("Author: {} <{}>".format(commit.author.name, commit.author.email))
	print("Date  : {}".format(time.strftime("%c %Z", time.localtime(commit.authored_date))))
	print()
	print("\t{}".format(commit.message.strip()))
	print()

commitsDifference = []
for commit in commitsInFirst:
	commitMessage = commit.message
	commitStats = commit.stats.files

	matched = False
	for secondCommit in commitsInSecond:
		if secondCommit.message == commitMessage and secondCommit.stats.files == commitStats:
			matched = True
	if not matched:
		commitsDifference.append(commit)
commitsDifference.sort(key = lambda c: c.authored_date)

if not args.r:
	for commit in commitsDifference:
		if not ignoredHashes.isPresent(commit.hexsha):
			printCommitInformation(commit)
else:
	for commit in commitsDifference:
		if not ignoredHashes.isPresent(commit.hexsha):
			printCommitInformation(commit)
			while True:
				inp = input("Resolve[R] / Ignore[I] : ")
				if inp.upper() == 'I':
					ignoredHashes.insert(commit.hexsha)
					break
				elif inp.upper() == 'R':
					break
				else:
					print("Invalid choice. Please try again.")