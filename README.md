<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">My JIRA Tasks</h3>

  <p align="center">
  Python script that prints open personal JIRA tasks
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
    * [Built With](#built-with)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation and Usage](#installation-and-usage)
* [Collaboration](#collaboration)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

Simple Python script that prints open personal JIRA tasks in the terminal.

```shell
$ jira
You have 4 unresolved JIRA issues

To Do:
⦿ Awesome task that has a To Do status https://yourawesomedomain.atlassian.net/browse/ISSUE-01 (Created 42 days ago)

In Progress:
⦿ Awesome task that I am working on https://yourawesomedomain.atlassian.net/browse/ISSUE-18 (Created 8 days ago)
⦿ Awesome task that I am working on https://yourawesomedomain.atlassian.net/browse/ISSUE-14 (Created 22 days ago)

Other:
⦾ Awesome task that is on hold https://yourawesomedomain.atlassian.net/browse/ISSUE-425 (Created Today)
⦿ Another awesome task that did not fit in any category https://yourawesomedomain.atlassian.net/browse/ISSUE-422 (Created Yesterday)
⦿ Yet Another awesome task that did not fit in any category https://yourawesomedomain.atlassian.net/browse/ISSUE-420 (Created Yesterday)
```

### Built With
* [Python](https://www.python.org/)
* [Jira lib](https://pypi.org/project/jira/)

<!-- GETTING STARTED -->
## Getting Started
If you want to get this script up and running, follow these steps:

### Prerequisites
#### Virtual Environment
The script is ready to work with a conda environment out-of-the-box,
so I recommend using [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html).

#### JIRA API Token
For the authentication to work, you need to obtain a token from JIRA, see: [https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)

### Installation and Usage
1. Clone the repo
```shell script
git clone https://github.com/johnunar/my-jira-tasks.git
```
2. Create a new conda environment:
```shell script
conda create --name jira --file requirements.txt python=3.9
```
3. Run the script:
```shell script
./my-jira-tasks.py
```
4. If this is the first time running the script, you will be prompted with initialization request:
```shell script
Some of the configuration is missing.
Would you like to initialize the script and set a new configuration now? [y/N]
```
Then provide the configuration data you are asked for.

**WARNING: DO NOT share the generated *.env* file with anyone. It contains your JIRA credentials.**

5. (Optional) In your .zshrc (or equivalent file) set an alias for comfortable usage:
```shell script
alias jira="~/scripts/jira/my_jira_tasks.py"
```

## Collaboration
If you want to improve this script, feel free to open a [PR](https://github.com/johnunar/my-jira-tasks/compare) or an [issue](https://github.com/johnunar/my-jira-tasks/issues/new)!

<!-- CONTACT -->
## Contact

Johnny
* [johnny@unar.dev](mailto:johnny@unar.dev)

Project Link: [https://github.com/johnunar/my-jira-tasks](https://github.com/johnunar/my-jira-tasks)