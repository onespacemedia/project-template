#!/bin/bash

# Ensure we don't have a tmp directory already.
# XXX: Alternatively, rm the individual app folder names.
rm -rf tmp/

# Pull in any optional project apps from their respective git repos.
# They will have their contents rendered as part of the generation
# process, then we'll move the files to their final destination.
{% for project in ['jobs', 'faqs', 'people', 'news'] %}
    {% if cookiecutter[project] == 'yes' %}
        echo "Cloning the {{project}} repo.";
        git clone --depth 1 -q https://github.com/onespacemedia/cms-{{project}}.git tmp/{{project}}/
    {% endif %}
{% endfor %}
