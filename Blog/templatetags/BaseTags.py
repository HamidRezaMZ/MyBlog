from django import template
from ..models import Category

register = template.Library()

@register.simple_tag()
def title():
    return "وبلاگ برنامه نویسی"


@register.inclusion_tag("partials/CategoryNavbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True)
    }