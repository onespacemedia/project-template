import os
import re
import subprocess
import sys
import time

import jwt
from github import Github, GithubIntegration


# Custom class to fix this: https://github.com/PyGithub/PyGithub/issues/627
class Py3GithubIntegration(GithubIntegration):
    def create_jwt(self):
        """
        Creates a signed JWT, valid for 60 seconds.
        :return:
        """
        now = int(time.time())
        payload = {
            "iat": now,
            "exp": now + 60,
            "iss": self.integration_id
        }
        return jwt.encode(
            payload,
            key=self.private_key,
            algorithm="RS256"
        ).decode('utf-8')


def main():
    compare_url = os.getenv('CIRCLE_COMPARE_URL')
    project_user = os.getenv('CIRCLE_PROJECT_USERNAME')
    project_repo = os.getenv('CIRCLE_PROJECT_REPONAME')
    private_key = os.getenv('ISSUE_NOTIFY_PRIVATE_KEY').replace('*newline*', '\n')
    remote = sys.argv[1]

    assert compare_url
    assert project_user
    assert project_repo
    assert private_key

    diffs = compare_url.split('/compare/')[-1]

    try:
        logs = subprocess.check_output(f'git log --pretty="%s %b" {diffs}', shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        print('Unable to get logs, exiting.')
        return

    # Search through the commit messages for resolved issues.

    # List of keywords taken from here:
    # https://help.github.com/articles/closing-issues-using-keywords/
    close_regex = re.compile(r'\b((close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved) #(\d+))\b', flags=re.IGNORECASE)
    matches = re.findall(close_regex, logs)
    issue_numbers = set([match[2] for match in matches])

    if not issue_numbers:
        print('No issues closed in this build.')
        return

    integration = Py3GithubIntegration(6214, private_key)
    access_token = integration.get_access_token(62607)
    gh = Github(login_or_token=access_token.token)

    repo = gh.get_repo(f'{project_user}/{project_repo}')

    for issue_id in issue_numbers:
        issue = repo.get_issue(int(issue_id))
        print(f'Sending notification for issue #{issue_id}.')
        issue.create_comment(f'@{issue.user.login}: The fix for this issue is now live on {remote}.')


if __name__ == '__main__':
    main()
