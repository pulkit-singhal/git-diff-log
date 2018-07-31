# git-diff-log
### Find difference in commits of two branches with a single command

[![PYT](https://img.shields.io/badge/Python-%3E%3D%203.0-brightgreen.svg)]()
[![SDP](https://img.shields.io/badge/Side%20Project-True-yellow.svg)]()

`git-diff-log` is a minimalist and simple command line commit analyzer. It is written in `Python 3` and uses `sqlite3` to cache the data.

Installing git-diff-log
------------

`git-diff-log` requires [Python][] 3 or newer, and some form of UNIX-like shell (bash
works well).  It works on Linux, OS X, and Windows (with [Cygwin][]).

[Python]: http://python.org/
[Cygwin]: http://www.cygwin.com/

Installing and setting up `git-diff-log` will not take more than a minute.

First, [download][] the newest version or clone the git repository
(`git clone https://github.com/pulkit-singhal/git-diff-log.git`).  Put it anywhere you like.

[download]: https://github.com/pulkit-singhal/git-diff-log/archive/master.zip

Install the required dependencies by running

    python -m pip install -r requirements.txt
    
How to use ?
------

    python gitdifflog.py /path/to/git/repo master release
    
Replace `master` and `release` with the branches that you want to compare

Optional command line parameters -
* `-c commitCount` - By passing this parameter, you can restrict the application to compare the only `commitCount` commits  
* `-r` - This application starts the `resolution` mode, so that you can either `resolve` or `ignore` the commit. In case you
ignored the commit, it will not not show up later in the results.  
**Note**: In case you wrongly ignored some commit, just delete the `ignored_hashes.db` file created. It will clear up all the 
ignored commits 
