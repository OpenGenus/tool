from django import template
register = template.Library()


@register.filter(name='tool_category')
def tool_category(value, category):
    return value.filter(category=category)
