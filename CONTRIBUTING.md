# Contributing

Nirjas welcomes any form of contribution or suggestions. We believe that open source is all about collaborative working to make the project and community stronger than ever. Whether you are a beginner or an experienced developer, each and every contribution counts.

You can contribute to Nirjas by:
1. Opening a valid issue: visit https://github.com/fossology/nirjas/issues 
2. Help us in closing an [existing issue](https://github.com/fossology/nirjas/issues)
3. Open a [Pull Request](https://github.com/fossology/nirjas/pulls)
4. Suggest us some new agent for license scanning
5. Want to discuss something else: Reach out to us @ [Slack](https://fossology.slack.com/)


***


### Setting up a python virtual environment
* venv (for Python 3) allow you to manage separate package installations for different projects. 
* To create a virtual environment, go to your project’s directory and run venv. 

* On macOS and Linux:

    `python3 -m venv env`

* On Windows:

    `py -m venv env`

> The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env.


### Activating a virtual environment 
* On macOS and Linux:
    
    `source env/bin/activate`

* On Windows:

    `.\env\Scripts\activate`

* Leaving the virtual environment
If you want to switch projects or otherwise leave your virtual environment, simply run:

    `deactivate`

***


## Report a valid issue  

Nirjas uses [GitHub's issue tracker](https://github.com/fossology/nirjas/issues). All bugs and enhancements should be listed so that we don't lose track of them, can prioritize and assign them to the relevant developer or maintainer.

Consider the following recommended best practice for writing issues, which are (Recommended but not limited to):
1. More detailed description rather than one-liners
2. Screenshots 
3. Providing example files and error logs
4. How to reproduce it
5. Details of your local system or environment that you're using

## Code Guidelines

Please follow the [Coding Style](https://www.python.org/dev/peps/pep-0008/) (PEP8)

**Not Familiar with Git?**

> Invest a few minutes on our [Git Tutorial](https://github.com/fossology/fossology/wiki/Git-basic-commands) 

### Workflow

We are using the [Feature Branch Workflow (also known as GitHub Flow)](https://guides.github.com/introduction/flow/),
and prefer delivery as pull requests.

## Git Commit

The cardinal rule for creating good commits is to ensure there is only one
"logical change" per commit. Why is this an important rule?

*   The smaller the amount of code being changed, the quicker & easier it is to
    review & identify potential flaws.

*   If a change is found to be flawed later, it may be necessary to revert the
    broken commit. This is much easier to do if there are not other unrelated
    code changes entangled with the original commit.

*   When troubleshooting problems using Git's bisect capability, small well
    defined changes will aid in isolating exactly where the code problem was
    introduced.

*   When browsing history using Git annotate/blame, small well defined changes
    also aid in isolating exactly where & why a piece of code came from.

Things to avoid when creating commits

*   Mixing whitespace changes with functional code changes.
*   Mixing two unrelated functional changes.
*   Sending large new features in a single giant commit.

## Git Commit Conventions

We use git commit as per [Conventional Changelog](https://github.com/ajoslin/conventional-changelog):

```none
<type>(<scope>): <subject>
```

Example:

```none
feat(CosineSim): Implemented similarity score to approximately match headers
```

Allowed types:

*   **feat**: A new feature
*   **fix**: A bug fix
*   **docs**: Documentation only changes
*   **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, newline, line endings, etc)
*   **refactor**: A code change that neither fixes a bug or adds a feature
*   **perf**: A code change that improves performance
*   **test**: Adding missing tests
*   **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation

## Making a change with a pull request 

Pull requests with patches, improvements and new features are a great help. 

#### 1. Fork the project, clone your fork, and add the remote:

```sh
# Clone your fork of the repo into the current directory
git clone https://github.com/<USERNAME>/Nirjas.git

# Navigate to the cloned directory
cd Nirjas

# Assign the original repo to a remote called "upstream"
git remote add upstream git@github.com:fossology/Nirjas.git 
```
#### 2. Get the latest changes from upstream:

```sh
git checkout master
git pull upstream master
```

#### 3. Create a new branch from the main master branch to contain your changes:

```sh 
git checkout -b <topic-branch-name> 
```

#### 4. Add and Commit your changes

```sh
git add <path/to/modified/file/> 
git commit -m "write a commit message"
```
> Examine the status of your working tree at each step to see if everything is clean
>```sh
> git status
> ```

Push your topic branch up to your fork:
```sh
git push origin <topic-branch-name> 
```

#### 5. Open a Pull Request with a clear title and description against the master branch.

[Open a Pull Request.](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)


A maintainer/developer will review and might suggest some changes before merging them into the repository.

Success!! :tada:  Well done! :bowing_man: 


***


## A Special Note 

Thank you for reading through and we look forward to your valuable contribution! :smiley:  

We appreciate the hard work and time of our contributors who have built and maintained the project! :raised_hands:

You are Awesome! :star2: :star_struck: 