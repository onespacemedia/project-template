#!/usr/bin/env python2.7
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "imperial.settings.local")

    # Ensure we have a pre-push Git hook.
    os.system("""
        if [ ! -f .git/hooks/pre-push ]; then
            wget -qO .git/hooks/pre-push https://raw.githubusercontent.com/onespacemedia/project-template/develop/%7B%7Bcookiecutter.repo_name%7D%7D/pre-push;
            chmod +x .git/hooks/pre-push;
        fi
    """)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
