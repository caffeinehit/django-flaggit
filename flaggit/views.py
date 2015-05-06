from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from flaggit import utils
from flaggit.forms import FlagForm
from flaggit.models import Flag

class FlagView(View):
    def post(self, request):
        form = FlagForm(request.POST)
        
        if not form.is_valid():
            return HttpResponseBadRequest()
        
        user = None
        if request.user.is_authenticated():
            user = request.user
        
        utils.flag(form.cleaned_data['object'], user, request.META['REMOTE_ADDR'],
            form.cleaned_data['comment'])

        messages.success(request, 'Flagged successfully.')
        if 'next' in request.GET:
            return HttpResponseRedirect(request.GET.get('next'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def flag_action(request, **kwargs):

    user = request.user
    filter_args = {'id': kwargs['flag_id']}
    flag_obj = get_object_or_404(Flag, **filter_args)
    if kwargs['action'] == 'approved':
        flag_obj.content_object.delete()
        flag_obj.delete()
    elif kwargs['action'] == 'rejected':
        flag_obj.delete()

    messages.success(request, 'Action completed successfully successfully.')
    if 'next' in request.GET:
        return HttpResponseRedirect(request.GET.get('next'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
