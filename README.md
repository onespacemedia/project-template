# project-template

This is the project template that the [Onespacemedia](https://www.onespacemedia.com) team use to start their projects. It uses the excellent [Cookiecutter](https://github.com/audreyr/cookiecutter) project as a foundation and uses a lot of its features in the generation process.

## Getting started

To start a project using this template, follow these steps:

1. `cd` to the directory in which your projects typically live (for us, this is `~/Workspace`).
2. Ensure you have `cookiecutter` installed globally on your system - `pip install cookiecutter` (on Linux `sudo apt-get install cookiecutter` works too)
3. Install [nvm](https://github.com/creationix/nvm)
4. Run `cookiecutter gh:onespacemedia/project-template`
5. Answer the questions.
6. That's it!

You will need to add a Git remote and probably set up a few other things. Work is ongoing to improve the initial process.

## Common issues

### Git flow missing

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

Install git-flow (`brew install git-flow` on Mac, `sudo apt-get install git-flow` on Linux).

### nvm can't be found

```
/tmp/tmpgyJsw1.sh: line 153: nvm: command not found
Removing project folder.
ERROR: Stopping generation because post_gen_project hook script didn't exit successfully
Hook script failed (exit status: 127)
```

Ubuntu uses ~/.profile instead of ~/.bash_profile, but `post_gen_project.sh` assumes the latter. Create a symlink with `ln -s ~/.profile ~/.bash_profile`.
