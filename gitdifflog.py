from git import Repo
from git.exc import NoSuchPathError
from termcolor import colored
import argparse
import sys
import time

class DiffCommit:
	def __init__(self, author, date, message, hexsha):
		self.author = author
		self.date = date
		self.message = message.strip()
		self.sha = hexsha

	def __lt__(self, other):
		return self.date < other.date

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("first")
parser.add_argument("second")
parser.add_argument("-c", nargs = "?", type = int)
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

commitsDifference = []
for commit in commitsInFirst:
	commitMessage = commit.message
	commitStats = commit.stats.files

	matched = False
	for secondCommit in commitsInSecond:
		if secondCommit.message == commitMessage and secondCommit.stats.files == commitStats:
			matched = True
	if not matched:
		commitsDifference.append(DiffCommit(commit.author, commit.authored_date, commit.message, commit.hexsha))
commitsDifference.sort()

for commit in commitsDifference:
	print(colored("commit {}".format(commit.sha), 'yellow'))
	print("Author: {} <{}>".format(commit.author.name, commit.author.email))
	print("Date  : {}".format(time.strftime("%c %Z", time.localtime(commit.date))))
	print()
	print("\t{}".format(commit.message))
	print()
