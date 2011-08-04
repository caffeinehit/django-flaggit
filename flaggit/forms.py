from django import forms
from django.contrib.contenttypes.models import ContentType

class FlagForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content_type = forms.ModelChoiceField(widget=forms.HiddenInput,
        queryset=ContentType.objects.all())
    comment = forms.CharField(widget=forms.Textarea, required=False)
    
    def clean(self):
        content_type = self.cleaned_data['content_type']
        Model = content_type.model_class()
        id = self.cleaned_data['object_id']
        try:
            obj = Model.objects.get(id=id)
        except Model.DoesNotExist:
            raise forms.ValidationError("No such %s object with id %s" % (Model, id))
        
        self.cleaned_data['object'] = obj
        return self.cleaned_data
    
