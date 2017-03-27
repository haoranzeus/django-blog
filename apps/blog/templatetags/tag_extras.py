from django import template

register = template.Library()


def update_variable(value):
    data = value
    return data


register.filter('update_variable', update_variable)
