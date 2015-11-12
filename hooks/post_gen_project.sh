#! /bin/bash

npm install -g webpack
npm install
webpack
pip freeze > requirements.txt

# TODO: If geoip wasn't enabled, delete the geoip folder.
