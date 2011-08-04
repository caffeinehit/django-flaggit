from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.tag
def flag_form(parser, token):
    """
    Renders the flagging form for a given object. Optionally with a custom 
    template.
    
    Usage:
    
        {% load flaggit_tags %}
        {% flag_form object %}
        {% flag_form object "flaggit/alternate_form.html" %}
    """
    
    bits = token.split_contents()
    
    return FlagFormNode(*bits[1:])

class FlagFormNode(template.Node):
    def __init__(self, obj, tpl=None):
        self.obj = template.Variable(obj)
        self.tpl = tpl[1:-1] if tpl else 'flaggit/form.html'
    
    def render(self, context):
        obj = self.obj.resolve(context)
        content_type = ContentType.objects.get_for_model(obj)
        return template.loader.render_to_string(self.tpl, {
            'object': obj,
            'content_type': content_type,
        }, context_instance=context)
