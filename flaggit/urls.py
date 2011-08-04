from django.conf.urls.defaults import patterns, url
from flaggit.views import FlagView

urlpatterns = patterns('',
    url('^flag/$', FlagView.as_view(), name='flaggit'),
)
