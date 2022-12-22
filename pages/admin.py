from django.contrib import admin

from .models import Page, PageCategory, SiteSettings

admin.site.register(Page)
admin.site.register(PageCategory)
admin.site.register(SiteSettings)
