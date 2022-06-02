#!/usr/bin/env conda run -n jira --no-capture-output python
import json
import os
import sys
from datetime import datetime

from dateutil.tz import tzlocal
from dotenv import load_dotenv
from jira import JIRA, Issue

load_dotenv()


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


NOW = datetime.now().replace(tzinfo=tzlocal())


def sort_issues(issues: list[Issue], categories: list) -> list[dict[str, list]]:
    """
    Sort provided issues by provided categories
    :param issues: list with JIRA Issues (Issue obj.)
    :param categories: list with category names (str)
    :return: list with categories and their issues::
        [{"category: [Issue1, Issue2, Issue3, ...]}, {...}, ...]
    """
    result = [
        {
            "name": category,
            "issues": [
                issue
                for issue in issues
                if str(issue.fields.status) == category
            ],
        }
        for category in categories
    ]
    if "Other" in categories:
        result.append(
            {
                "name": "Other",
                "issues": [
                    issue
                    for issue in issues
                    if str(issue.fields.status) not in categories
                ],
            }
        )

    return result


def generate_days_count_tag(issue: Issue) -> str:
    """
    Generate "n days ago", "Today" or "Yesterday" based on the day count
    :param issue: Jira Issue to generate the tag for
    :return: string with the corresponding tag
    """
    days_ago_int = (
            NOW
            - (datetime.strptime(issue.fields.created, "%Y-%m-%dT%H:%M:%S.%f%z"))
    ).days

    days_ago = f"{days_ago_int} days ago"
    if days_ago_int == 0:
        days_ago = "Today"
    elif days_ago_int == 1:
        days_ago = "Yesterday"

    return days_ago


def print_category_summary(issues: list[Issue], name: str) -> None:
    """
    Print summary of each issue category
    :param issues: list of issues in a given category
    :param name: name of the given category
    """
    if issues:
        print(f"\n{Colors.UNDERLINE}{name}:{Colors.ENDC}")
        for issue in issues:
            days_ago = generate_days_count_tag(issue)
            print(
                f"{Colors.WARNING if str(issue.fields.priority) == 'Medium' else ''}"
                f"{Colors.FAIL if str(issue.fields.priority) == 'High' else ''}"
                f"{'⦿' if str(issue.fields.status) != 'On Hold' else '⦾'} {issue.fields.summary} "
                f"{Colors.OKCYAN}https://jlldigitalproductengineering.atlassian.net/browse/{issue.key}{Colors.ENDC} "
                f"(Created {days_ago})"
            )


def initialize() -> tuple[str, str, str, list]:
    """
    Initialize the script environment
    Asks for data in the terminal and saves them in the .env file
    :return: user (str), token (str), server (str), categories (list)
    """
    try:
        confirm_initialize = input("Would you like to initialize the script and set a new configuration now? [y/N] ")
        if confirm_initialize.lower() in ("y", "yes"):
            user = input("Username: ")
            token = input("Token: ")
            server = input("JIRA Server: ")
            categories = input(
                "Statuses you want to display [To Do, In Progress, On Hold, Other]: "
            ).replace(", ", ",").replace("[", "").replace("]", "").split(",")

            if not categories:
                categories = ["To Do", "In Progress", "On Hold", "Other"]

            current_dir = os.path.abspath(os.path.dirname(__file__))

            with open(os.path.join(current_dir, ".env"), "w+") as env_file:
                env_file.write(
                    f"USERNAME='{user}'\n"
                    f"TOKEN='{token}'\n"
                    f"SERVER='{server}'\n"
                    f"CATEGORIES=\"{categories}\"\n"
                )
            return user, token, server, categories
        else:
            exit(0)
    except (KeyboardInterrupt, EOFError):
        pass


def get_env_variables():
    # "user@domain.xyz"
    user = os.getenv("USERNAME")
    # See: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
    token = os.getenv("TOKEN")
    # "https://subdomain.atlassian.net"
    server = os.getenv("SERVER")
    # Use issue statuses you want to display, 'Other' stands for everything else:
    # "['To Do', 'In Progress', 'Other']"
    categories = (
        json.loads(os.getenv("CATEGORIES").replace("'", '"'))
        if os.getenv("CATEGORIES")
        else None
    )

    if not all((user, token, server, categories)):
        print("Some of the configuration is missing.")
        user, token, server, categories = initialize()

    return user, token, server, categories


if __name__ == "__main__":
    if "init" in sys.argv:
        initialize()
        exit(0)
    try:
        user, token, server, categories = get_env_variables()
        jira = JIRA(basic_auth=(user, token), server=server)

        my_unresolved_issues = jira.search_issues(
            "assignee = currentUser() AND resolution = Unresolved"
        )
        if my_unresolved_issues:
            print(
                f"You have {Colors.WARNING}{len(my_unresolved_issues)}{Colors.ENDC} unresolved JIRA issues."
            )

            for category in sort_issues(my_unresolved_issues, categories):
                print_category_summary(category["issues"], category["name"])
        else:
            print("You have no unresolved JIRA issues. Good job!")
    except Exception as e:
        print("There was an error with your request: ", repr(e))
