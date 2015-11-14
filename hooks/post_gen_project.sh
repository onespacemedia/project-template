#! /bin/bash

# Create the database.
createdb {{cookiecutter.repo_name}}

# Make the virtual environment.
if which -s mkvirtualenv; then
    mkvirtualenv {{cookiecutter.repo_name}}
    workon {{cookiecutter.repo_name}}
else
    virtualenv -p python .venv
    . .venv/bin/activate
fi

# If GeoIP wasn't enabled, delete the GeoIP folder.
if grep -iq GeoIP "requirements.txt"; then
    rm -rf {{cookiecutter.repo_name}}/geoip/
fi

# Install Python dependencies.
pip install --upgrade pip
pip install -r requirements.txt

# The requirements will now have versions pinned, so re-dump them.
pip freeze > requirements.txt

# We disable rendering of the templates folder to avoid having to wrap everything in
# raw tags, but that causes the parent directory path to also not be parse, so we need
# to move everything into the correct location, then remove the old parent directory.
mv {{ "{{" }}cookiecutter.repo_name{{ "}}" }}/templates {{cookiecutter.repo_name}}/templates
rmdir {{ "{{" }}cookiecutter.repo_name{{ "}}" }}

# Move the project app folders into the correct locations.
mv tmp/*/apps/* example_project/apps/
mv tmp/*/templates/* example_project/templates/

# Remove the tmp directory.
rm -rf tmp/

# Generate a secret key and update the base settings file.
sed -i '' "s|SECRET_KEY = \" \"|SECRET_KEY = \"$(printf '%q' $(./manage.py generate_secret_key))\"|g" {{cookiecutter.repo_name}}/settings/base.py

# The following commands don't need to be run under CI.
if [ -z "$CI" ]; then

    # Install front-end dependencies.
    npm install -g webpack
    npm install
    webpack

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
    git push
fi
