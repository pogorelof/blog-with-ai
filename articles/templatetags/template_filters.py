from django.template import Library


register = Library()

@register.filter
def get_item(dict, key):
    return dict.get(key)