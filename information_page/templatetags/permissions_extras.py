from django import template

register = template.Library()


@register.simple_tag
def has_permission(**kwargs):
    has_permmission = False
    user = kwargs['user']
    obj = kwargs.get('obj')
    perm = kwargs.get('perm')

    if user.is_authenticated:
        if obj and obj.author == user:
            has_permmission = user.has_perm(
                perm,
                obj)
        elif obj:
            has_permmission = user.has_perm(
                perm,
                obj)
        else:
            has_permmission = user.has_perm(
                perm)

    return has_permmission
