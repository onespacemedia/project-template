#!/usr/bin/env bash

if [ -n "`$SHELL -c 'echo $ZSH_VERSION'`" ]; then
    source ~/.zshrc
else
    source ~/.bash_profile
fi

# Create the database.
createdb {{cookiecutter.package_name}}

# Make the virtual environment.
if command -v mkvirtualenv >/dev/null 2>&1; then
    mkvirtualenv {{cookiecutter.repo_name}} && workon {{cookiecutter.repo_name}}
else
    virtualenv -p python .venv && source .venv/bin/activate
fi

# If GeoIP wasn't enabled, delete the GeoIP folder.
{% if cookiecutter.geoip == "no" %}
    echo "Removing GeoIP folder";
    rm -rf {{cookiecutter.package_name}}/geoip/
{% endif %}

# If the sections app wasn't enabled, delete the utils file.
{% if cookiecutter.sections == "no" %}
    echo "Removing admin utils file."
    rm {{cookiecutter.package_name}}/utils/admin.py
{% endif %}

# Install Python dependencies.
if [ -z "$CI" ]; then
    pip install --upgrade pip
fi

# Remove anything which doesn't work on Python 3.
if [ "$(python -c 'import sys; print(sys.version_info[0])')" == "3" ]; then
    {% for requirement in ['onespacemedia-server-management'] %}
        perl -pi -e s,{{requirement}},,g requirements.txt
    {% endfor %}

    perl -pi -e s,python-memcached,python3-memcached,g requirements.txt
fi

# Work out which footer we want to include
{% if cookiecutter['footer'] == 'yes' %}
  perl -pi -e s,base/_footer.html,footer/_footer.html,g {{ "{{" }}cookiecutter.package_name{{ "}}" }}/templates/base.html
  rm {{ "{{" }}cookiecutter.package_name{{ "}}" }}/templates/base/_footer.html
{% endif %}

pip install -r requirements.txt

# Install the linters so the versions get frozen.
pip install -q --disable-pip-version-check pylint pylint-django pylint-mccabe isort

# The requirements will now have versions pinned, so re-dump them.
pip freeze > requirements.txt

# We disable rendering of the templates folder to avoid having to wrap everything in
# raw tags, but that causes the parent directory path to also not be parse, so we need
# to move everything into the correct location, then remove the old parent directory.
mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/templates {{cookiecutter.package_name}}/templates
mv {{ "{{" }}cookiecutter.package_name{{ "}}" }}/assets {{cookiecutter.package_name}}/assets
rmdir {{ "{{" }}cookiecutter.package_name{{ "}}" }}

# Move the project app folders into the correct locations.
if [ -d "tmp" ]; then
    mv tmp/*/apps/* {{cookiecutter.package_name}}/apps/
    mv tmp/*/templates/* {{cookiecutter.package_name}}/templates/

    # Remove the tmp directory.
    rm -rf tmp/

    # Replace the project_name variable in the external apps.
    if grep -ril "{{ "{{" }} project_name {{ "}}" }}" *;
    then
        perl -pi -e 's/{{ "{{" }} project_name {{ "}}" }}/{{ cookiecutter.package_name }}/g' `grep -ril "{{ "{{" }} project_name {{ "}}" }}" *`
    fi
fi

# Generate a secret key and update the base settings file.
perl -pi -e s,SECRET_KEY\ =\ \'\ \',SECRET_KEY\ =\ \'$(openssl rand -base64 50 | tr -d '\n')\',g {{cookiecutter.package_name}}/settings/base.py

# Install front-end dependencies.
if command -v yarn >/dev/null 2>&1; then
    yarn
    yarn run build
else
    npm install
    npm run build
fi

# The following commands don't need to be run under CI.
if [ -z "$CI" ]; then

    # Create a git repo and configure it for git flow.
    git init

    mkdir -p .git/hooks
    mv pre-push .git/hooks/pre-push
    chmod +x .git/hooks/pre-push

    git flow init -d

    # Add all of the project files to a Git commit and push to the remote repo.
    git add .
    git commit --amend --all --no-edit

    {% if cookiecutter.create_repo == 'yes' %}
      if command -v hub >/dev/null 2>&1; then
          hub create -p onespacemedia/{{cookiecutter.repo_name}}

          git push -u origin develop
      fi
    {% endif %}
fi
