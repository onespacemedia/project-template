{{cookiecutter.project_name}}
==================

Live domain: https://www.{{cookiecutter.domain_name}}/<br>
Staging domain: https://www.{{cookiecutter.staging_subdomain}}.onespace.media/


### Redis & Celery

We use Redis and Celery to handle running various tasks asynchronously to avoid bogging down the request/response workers.

Some good examples of this would be:

* Sending emails.  If you want an asynchronous version of `utils/send_email_by_reference`, then take a look at [Cambridge Wireless](https://github.com/onespacemedia/cambridge-wireless/blob/develop/cambridge_wireless/utils/emails.py#L132-L136), which has it.
* Generating exports.
* Calling third-party APIs when submitting contact forms.

Basically anything which can take a while to run, but isn't depended on for future bits of code should probably be made into a Celery task to improve performance.

For examples of internal projects which make use of Celery, please refer to [this search](https://github.com/search?utf8=%E2%9C%93&q=org%3Aonespacemedia+shared_task+language%3APython+language%3APython&type=Code).

#### Locally

* `brew install redis`
* `brew services start redis`
* `pip install celery[redis]`

Then to run the worker you want

* `DJANGO_SETTINGS_MODULE={{cookiecutter.package_name}}.settings.local celery -A {{cookiecutter.package_name}} worker -E --loglevel=info`

#### In production

This will eventually be handled by server-manangement, but for now if you need it then use this as a guide:

* `sudo add-apt-repository ppa:chris-lea/redis-server`
* `sudo apt-get update`
* `sudo apt-get install redis-server`
* `sudo ln -s /var/www/{{cookiecutter.package_name}}/config/celery.conf /etc/supervisor/conf.d/celery.conf`
* `sudo supervisorctl reread`

# Useful resources:

* http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#first-steps
