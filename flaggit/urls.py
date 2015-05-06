from django.conf.urls.defaults import patterns, url
from flaggit.views import FlagView, flag_action

urlpatterns = patterns('',
    url('^flag/$', FlagView.as_view(), name='flaggit'),
    url('^flag-action/(?P<flag_id>\d+)/(?P<action>[a-zA-Z0-9\-]+)/$', flag_action, name='flag_action'),
)
