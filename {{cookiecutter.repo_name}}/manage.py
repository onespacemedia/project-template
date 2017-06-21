#!/usr/bin/env python3.6
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.package_name}}.settings.local")

    # Ensure we have a pre-push Git hook.
    if not os.getenv('CI', False):
        os.system("""
            cd "$(git rev-parse --show-toplevel)" || exit;

            if [ ! -f .git/hooks/pre-push ]; then
                echo "Downloading the pre-push hook..";
                curl -so .git/hooks/pre-push https://raw.githubusercontent.com/onespacemedia/project-template/develop/%7B%7Bcookiecutter.repo_name%7D%7D/pre-push;

                echo "Installing the pre-push hook..";
                chmod +x .git/hooks/pre-push;

                echo "Done!";
            fi
        """)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
