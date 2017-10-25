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
    mkvirtualenv {{cookiecutter.repo_name}} -p /usr/local/bin/python3 && workon {{cookiecutter.repo_name}}
else
    python3 -m venv .venv && source .venv/bin/activate
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

pip install -r requirements.txt

# Install the linters so the versions get frozen.
pip install -q --disable-pip-version-check pylint pylint-django pylint-mccabe isort

# The requirements will now have versions pinned, so re-dump them.
pip freeze > requirements.txt

# Generate a secret key and update the base settings file.
perl -pi -e s,SECRET_KEY\ =\ \'\ \',SECRET_KEY\ =\ \'$(openssl rand -base64 50 | tr -d '\n')\',g {{cookiecutter.package_name}}/settings/base.py

# Install front-end dependencies.
#if command -v yarn >/dev/null 2>&1; then
#    yarn
#    yarn run build
#else
#    npm install
#    npm run build
#fi

{% for project in ['careers', 'events', 'faqs', 'partners', 'people', 'news', 'redirects', 'sections'] %}
    {% if cookiecutter[project] == 'no' %}
        echo "Remove the {{project}} app.";
        rm -r {{ cookiecutter.package_name }}/apps/{{ project }}
    {% endif %}
{% endfor %}

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
fi
