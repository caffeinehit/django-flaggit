# django-flaggit

django-flaggit enables content flagging.

## Installation
Be sure to install this fork from github

    $ pipenv install -e git+https://github.com/morenoh149/django-flaggit.git#egg=django-flaggit
	
## Usage:

* Add `flaggit` to your `INSTALLED_APPS`
```
    # settings.py
    ...
    INSTALLED_APPS = (
        ...
	'flaggit',
    )
```
* run migrations

    $ ./manage.py migrate

* Include `flaggit.urls` into your URLs if you plan on using the view and template
  tag:

		urlpatterns = patterns('',
			url('^', include('flaggit.urls')),
		)

## Test

Follow above steps and run

	python manage.py test flaggit
	

## API

### Models

* `flaggit.models.Flag`
* `flaggit.models.FlagInstance`  

### Utils

* `flaggit.utils.flag(obj, user=None, ip=None, comment=None)`:  
  Flag an `obj`, returns a `FlagInstance`

### Signals

* `flaggit.signals.flagged(flag)`:  
  Sent when something is flagged. Can be used to notify moderators.

* `flaggit.signals.review(flag)`:  
  Sent when something is in review.

* `flaggit.signals.rejected(flag)`:  
  Sent when some content was rejected.

* `flaggit.signals.approved(flag)`:  
  Sent when some content was approved.

Here's a template you can copy paste:

	import flaggit

	def handle_flagged(sender, flag, created = False, **kwargs):
		if created:
			# send emails
			pass
		else:
			pass
	
	def handle_review(sender, flag, **kwargs):
		pass
		
	def handle_rejected(sender, flag, **kwargs):
		flag.content_object.delete()
		flag.delete()
	
	def handle_approved(sender, flag, **kwargs):
		pass
	
	flaggit.signals.flagged.connect(handle_flagged)
	flaggit.signals.review.connect(handle_review)
	flaggit.signals.rejected.connect(handle_rejected)
	flaggit.signals.approved.connect(handle_approved)

### Template tags

	{% load flaggit_tags %}
	{% flag_form object %}
	{% flag_form object "your/custom/template.html" %}

* `{% flag_form object %}`:  
  Renders a form to flag `object`-

* `{% flag_form object "your/custom/template.html" %}`:  
  Renders the form with a custom template.

------------- 
  
[@flashingpumpkin](http://twitter.com/flashingpumpkin)
