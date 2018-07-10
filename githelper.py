from git import Repo
from git.exc import NoSuchPathError
from termcolor import colored
from hashstore import HashStore
import sys
import functools
import time

class GitHelper:
	def __init__(self, directory):
		self.directory = directory
		try:
			repo = Repo(directory)
		except NoSuchPathError as e:
			print(colored("Specified directory does not exists", "red"))
			sys.exit(0)

		if repo.bare:
			print(colored("The directory does not contains the .git folder", "red"))
			sys.exit(0)
		self.repo = repo
		self.ignored_hashes = HashStore()

	@functools.lru_cache(maxsize = None)
	def branches(self):
		return [branch.name for branch in self.repo.branches]

	def validate_branches_are_present(self, *args):
		for branch in args:
			if branch not in self.branches():
				print(colored("Specified branch {} does not exists".format(branch), "red"))
				sys.exit(0)

	def commits(self, branch_name, max_count = None):
		if max_count is not None:
			return list(self.repo.iter_commits(branch_name, max_count = max_count))
		else:
			return list(self.repo.iter_commits(branch_name))

	def different_commits(self, commits_in_first, commits_in_second):
		different_commits = []
		for commit in commits_in_first:
			matched = False
			for second_commit in commits_in_second:
				if second_commit.message == commit.message and second_commit.stats.files == commit.stats.files:
					matched = True
			if not matched:
				different_commits.append(commit)
		return different_commits

	def should_print_commit(self, commit):
		return not self.ignored_hashes.is_present(commit.hexsha)

	def resolve_commit(self, commit, resolve):
		if resolve:
			while True:
				inp = input("Resolve[R] / Ignore[I] : ")
				if inp.upper() == 'I':
					ignoredHashes.insert(commit.hexsha)
					break
				elif inp.upper() == 'R':
					break
				else:
					print("Invalid choice. Please try again.")

	@staticmethod
	def print_commit_info(commit):
		print(colored("commit {}".format(commit.hexsha), 'yellow'))
		print("Author: {} <{}>".format(commit.author.name, commit.author.email))
		print("Date  : {}".format(time.strftime("%c %Z", time.localtime(commit.authored_date))))
		print()
		print("\t{}".format(commit.message.strip()))
		print()