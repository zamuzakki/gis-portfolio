from django import template

register = template.Library()


@register.filter(name='expertises_to_comma_separated_string')
def expertises_to_comma_separated_string(queryset):
    """
    Convert Expertise Queryset to comma-separated string
    :param queryset: Queryset of Expertise
    :return: Comma-separated string containing User Expertise
    """
    string = ", ".join(str(obj.name) for obj in queryset)
    return string