#!/usr/bin/env conda run -n jira python
import json
import os
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


# "user@domain.xyz"
USER = os.getenv("USERNAME")

# See: https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/
TOKEN = os.getenv("TOKEN")

# "https://subdomain.atlassian.net"
SERVER = os.getenv("SERVER")

# Use issue statuses you want to display, 'Other' stands for everything else:
# "['To Do', 'In Progress', 'Other']"
CATEGORIES = json.loads(os.getenv("CATEGORIES").replace("'", '"'))

NOW = datetime.now().replace(tzinfo=tzlocal())


def sort_issues(issues: list, categories: list):
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


def print_category_summary(issues: list, name: str) -> None:
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


if __name__ == "__main__":
    jira = JIRA(basic_auth=(USER, TOKEN), server=SERVER)

    my_unresolved_issues = jira.search_issues(
        "assignee = currentUser() AND resolution = Unresolved"
    )
    if my_unresolved_issues:
        print(
            f"You have {Colors.WARNING}{len(my_unresolved_issues)}{Colors.ENDC} unresolved JIRA issues."
        )

        for category in sort_issues(my_unresolved_issues, CATEGORIES):
            print_category_summary(category["issues"], category["name"])
    else:
        print("You have no unresolved JIRA issues. Good job!")
