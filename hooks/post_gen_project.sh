#! /bin/bash

createdb {{cookiecutter.repo_name}}

# Install front-end dependencies.
npm install -g webpack
npm install
webpack

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
