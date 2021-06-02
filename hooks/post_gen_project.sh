#!/usr/bin/env bash

if [ -f ~/.zshrc ]; then
    source ~/.zshrc
else
    source ~/.bash_profile
fi

if [ -z "$CI" ]; then
    set -eo pipefail

    function cleanup {
        echo 'Removing project folder.'
        if [ -d "{{cookiecutter.package_name}}" ]; then
            rm -r "{{cookiecutter.package_name}}"
        fi

        if [ -d "{{ "{{" }}cookiecutter.package_name{{ "}}" }}" ]; then
            rm -r "{{ "{{" }}cookiecutter.package_name{{ "}}" }}"
        fi
    }

    trap cleanup ERR
    trap cleanup INT
else
    set -exo pipefail
fi

# Check if the database already exists
DB_NAME="{{cookiecutter.package_name}}"
if psql {{cookiecutter.package_name}} -c '' -h localhost -p 5432; then
    NEW_DB_NAME="${DB_NAME}_$(date +"%Y%m")"
    echo "You are trying to create a new database '$DB_NAME' which already exists; we can't do that (the database name needs to be available)."
    echo 'Please select a fix:'
    echo " 1) Use an automatically generated name ($NEW_DB_NAME)"
    echo ' 2) Provide a new name now'
    echo ' 3) Drop the existing database'
    echo ' 4) Quit, and let me sort it out'
    echo 'Please note: The replacement database name is not validated, please ensure it is valid and available.'
    read -p 'Select an option [1]: '

    case "$REPLY" in
        "1")
            DB_NAME=$NEW_DB_NAME
            ;;
        "2")
            read -p 'Please enter the database name you would like to use: ' DB_NAME
            ;;
        "3")
            dropdb $DB_NAME
            ;;
        "4")
            exit 1
            ;;
        *)
            DB_NAME=$NEW_DB_NAME
            ;;
    esac
fi

# Create the database.
createdb $DB_NAME -h localhost -p 5432

# Make the virtual environment.
if command -v mkvirtualenv >/dev/null 2>&1; then
    mkvirtualenv {{cookiecutter.repo_name}} -p /usr/local/bin/python3 && workon {{cookiecutter.repo_name}}
else
    python3 -m venv .venv && source .venv/bin/activate
fi

# If GeoIP wasn't enabled, delete the GeoIP folder.
{% if cookiecutter.geoip == "no" %}
    echo "Removing GeoIP folder";
    rm -rf {{cookiecutter.package_name}}/geoip2/
{% endif %}

# Install Python dependencies.
if [ -z "$CI" ]; then
    pip install --upgrade pip
fi

# Upgrade setuptools to avoid issues with python-memcached
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt

# The requirements will now have versions pinned, so re-dump them.
pip freeze > requirements.txt

# Generate a secret key and update the base settings file.
perl -pi -e s,SECRET_KEY\ =\ \'\ \',SECRET_KEY\ =\ \'$(openssl rand -base64 50 | tr -d '\n')\',g {{cookiecutter.package_name}}/settings/base.py

mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/apps/components/templates {{cookiecutter.package_name}}/apps/components/templates

{% for project in ['careers', 'contact', 'events', 'faqs', 'news', 'partners', 'people', 'redirects', 'resources', 'sections'] %}
    {% if cookiecutter[project] == 'no' %}
        echo "Remove the {{project}} app.";
        rm -r {{ cookiecutter.package_name }}/apps/{{ project }}
    {% else %}
        if [ -d "{{ "{{" }}cookiecutter.package_name{{ "}}" }}/apps/{{ project }}/templates" ]; then
            mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/apps/{{ project }}/templates {{cookiecutter.package_name}}/apps/{{ project }}/templates
        fi
    {% endif %}
{% endfor %}

mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/assets {{cookiecutter.package_name}}
mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/templates {{cookiecutter.package_name}}
mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/apps/emails/templates {{cookiecutter.package_name}}/apps/emails/templates
mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/apps/users/templates {{cookiecutter.package_name}}/apps/users/templates

rm -r {{ "{{" }}cookiecutter.package_name{{ "}}" }}

# Install front-end dependencies.
. ~/.nvm/nvm.sh
nvm install
nvm use

# The following commands don't need to be run under CI.
if [ -z "$CI" ]; then

    # Create a git repo and configure it for git flow.
    git init

    mkdir -p .git/hooks
    mv pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push
    git flow init -d

# We run this after initalising the git repo so the hooks are added correctly
yarn
yarn run build

if [ -z "$CI" ]; then

    # Add all of the project files to a Git commit and push to the remote repo.
    git add .
    git commit --amend --all --no-edit
fi
