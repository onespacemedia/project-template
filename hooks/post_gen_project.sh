#!/bin/bash

# Create the database.
createdb {{cookiecutter.repo_name}}

# Make the virtual environment.
if [ -z "$CI" ]; then

    {
        mkvirtualenv {{cookiecutter.repo_name}} &&
        workon {{cookiecutter.repo_name}}
    } || {
        virtualenv -p python .venv &&
        . .venv/bin/activate
    }
fi

# If GeoIP wasn't enabled, delete the GeoIP folder.
cat requirements.txt

if ! grep -iq GeoIP "requirements.txt"; then
    echo "Removing GeoIP folder";
    rm -rf {{cookiecutter.repo_name}}/geoip/
fi

# Install Python dependencies.
if [ -z "$CI" ]; then
    pip install --upgrade pip
fi

# Remove anything which doesn't work on Python 3.
if [ "$(python -c 'import sys; print(sys.version_info[0])')" == "3" ]; then
    {% for requirement in ['onespacemedia-server-management', 'python-memcached'] %}
        perl -pi -e s,{{requirement}},,g requirements.txt
    {% endfor %}
fi

pip install -r requirements.txt

# The requirements will now have versions pinned, so re-dump them.
pip freeze > requirements.txt

# We disable rendering of the templates folder to avoid having to wrap everything in
# raw tags, but that causes the parent directory path to also not be parse, so we need
# to move everything into the correct location, then remove the old parent directory.
mv {{ "{{" }}cookiecutter.repo_name{{ "}}" }}/templates {{cookiecutter.repo_name}}/templates
rmdir {{ "{{" }}cookiecutter.repo_name{{ "}}" }}

# Move the project app folders into the correct locations.
if [ -d "tmp" ]; then
    mv tmp/*/apps/* example_project/apps/
    mv tmp/*/templates/* example_project/templates/

    # Remove the tmp directory.
    rm -rf tmp/
fi

# Generate a secret key and update the base settings file.
perl -pi -e s,SECRET_KEY\ =\ \"\ \",SECRET_KEY\ =\ \"$(printf '%q' $(./manage.py generate_secret_key))\",g {{cookiecutter.repo_name}}/settings/base.py

# Install front-end dependencies.
npm install -g webpack
npm install
webpack

# The following commands don't need to be run under CI.
if [ -z "$CI" ]; then

    # Create a git repo and configure it for git flow.
    git init

    # If Git flow isn't installed, install it. This isn't optional.
    if ! which -s git-flow; then
        brew install git-flow
    fi

    git flow init -d

    # Add all of the project files to a Git commit and push to the remote repo.
    git add .
    git commit -am "Initial commit."

    # We can't push yet because we don't have a remote..
    # git push
fi
