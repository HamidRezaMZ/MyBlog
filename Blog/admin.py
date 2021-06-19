from django.utils.translation import ngettext
from django.contrib import admin
from .models import Article, Category


@admin.action(description="انتشار مقاله های انتخاب شده")
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status='p')
    modeladmin.message_user(request, ngettext(
        '%d مقاله منتشر شد.',
        '%d مقاله منتشر شدند.',
        updated,
    ) % updated)


@admin.action(description="پیش نویس  مقاله های انتخاب شده")
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status='d')
    modeladmin.message_user(request, ngettext(
        '%d مقاله پیش نویس شد.',
        '%d مقاله پیش نویس شدند.',
        updated,
    ) % updated)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'jpublish','author', 'status', 'category_to_str')
    list_filter = ('status', 'publish','author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]




admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'status', 'parent')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.site_header = "My WebSite"
