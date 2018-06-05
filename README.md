# project-template

This is the project template that the [Onespacemedia](http://www.onespacemedia.com) team use to start their projects. It uses the excellent [Cookiecutter](https://github.com/audreyr/cookiecutter) project as a foundation and makes use of a lot of it's features in the generation process.

## Getting started

To start a project using this template, follow these steps:

1. `cd` to the directory in which your projects typically live (for us, this is `~/Workspace`).
2. Ensure you have `cookiecutter` installed globally on your system - ```pip install cookiecutter```
3. Run `cookiecutter gh:onespacemedia/project-template`
4. Answer the questions.
5. That's it!

You will need to add a Git remote and probably set up a few other things. Work is ongoing to improve the inital process.


## Getting start for Linux (Tested on ubuntu 18.04)

1. `cd` to the directory in which your projects typically live (for us, this is `~/Workspace`).
2. Ensure you have `cookiecutter` installed globally on your system - ```sudo apt install cookiecutter```
3. Ensure nvm line is in your bash profile (~/.profile or ~/.bash_profile depending on distro)
4. Run `cookiecutter gh:onespacemedia/project-template`
5. Answer the questions.
6. That's it! .venv will be automatically setup too.

```
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" # This loads nvm
```

#### Common issues

##### Git flow missing

```
Initialised empty Git repository in /home/username/Workspace/font-g/.git/
git: 'flow' is not a git command. See 'git --help'.

The most similar commands are
	reflog
	show
Removing project folder.
ERROR: Stopping generation because post_gen_project hook script didn't exit successfully
Hook script failed (exit status: 1)
```

Install gitflow `sudo apt install git-flow`.

##### Git config missing details

```
fatal: unable to auto-detect e-mail address (got 'jin@X230.(none)')
fatal: Not a valid object name: 'master'.
error: pathspec 'develop' did not match any file(s) known to git.
Fatal: Could not check out branch 'develop'.
Removing project folder.
ERROR: Stopping generation because post_gen_project hook script didn't exit successfully
Hook script failed (exit status: 1)
```

Set config for git. `git config --global user.email "you@example.com"`
and `git config --global user.email "you@example.com"`
