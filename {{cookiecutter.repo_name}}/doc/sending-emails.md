Included in this project is a very simple to use, and simple to integrate email system. Designed for brochureware and large applications alike.  Email templates are defined in the admin system and are able to be called from anywhere within a Django project.

## Requirements

Only really tested with Python 3.6, Django 1.11 and PostgreSQL. You're welcome to try it with other versions, but it might break.  Python versions older than 3.6 probably won't work due to the use of f-strings.  Databases other than PostgreSQL probably won't work due to the use of `JSONField`.

This app also depends on Commonmark and django-reversion being installed. The admin views are improved if you're using django-suit.

## Installation

* Ensure the emails app folder is in your project.
* Add the module to your INSTALLED_APPS setting.
* Make migrations (because the defaults use settings variables).
* Migrate.
* Ensure you have SMTP details defined. We use Mailtrap and Mandrill, but you can use whatever you want.

## Usage

* Add email templates into the admin
* In your code, use the following:

```py
from {{cookiecutter.package_name}}.apps.emails.utils import send_email

send_email('REFERENCE', 'paul.smith@example.com')
```

This simply pulls the email content from the database and sends it to the given user.

Optional kwargs are as follows:

* `title`: Replaces 'title' from the EmailTemplate object.
* `user`: Enables the mail merge feature.
* `fake`: Construct and render the email, but don't actually send it.
* `ics`: Attach an .ICS file to the email, useful for event confirmations. The value is the content.
* `fail_silently`: Allow emails to fail to send without throwing an exception (Default: false)

## Management commands

The admin provides a pretty useful preview system, but if you want to send some test emails out you can use

```bash
./manage.py send_sample_emails john.smith@devteam.com
```

Where the supplied email address is the one to send to.
