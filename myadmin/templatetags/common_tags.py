from django import template

from unlimitedstudio.utils import checkRolePermission

register = template.Library()


@register.simple_tag
def showMenu(request, permission):
    return checkRolePermission(request, permission, 0)
