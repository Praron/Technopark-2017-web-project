from django import template

register = template.Library()

@register.filter(name='add_css')
def add_css(value, arg):
    strings = arg.split(',')
    d = {string.split('=')[0]: string.split('=')[1] for string in strings}
    return value.as_widget(attrs=d)
