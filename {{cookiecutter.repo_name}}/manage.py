#!/usr/bin/env python
import os
import pwd
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{{cookiecutter.package_name}}.settings.local")
    os.environ.setdefault("DB_USER", pwd.getpwuid(os.getuid()).pw_name)
    os.environ.setdefault("DB_NAME", "{{cookiecutter.package_name}}")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
