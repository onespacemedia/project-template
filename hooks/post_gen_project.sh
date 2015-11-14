#! /bin/bash

createdb {{cookiecutter.repo_name}}

# Install front-end dependencies.
npm install -g webpack
npm install
webpack

# Install Python dependencies.
pip install -r requirements.txt

# If GeoIP wasn't enabled, delete the GeoIP folder.
if grep -iq GeoIP "requirements.txt"; then
    rm -rf {{cookiecutter.repo_name}}/geoip/
fi

# The requirements will now have versions pinned.
pip freeze > requirements.txt
