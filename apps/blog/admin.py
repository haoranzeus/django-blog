from django.contrib import admin

# Register your models here.

from .models import ArticleModel, TagModel, Classify


@admin.register(ArticleModel)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_time', 'modify_time')
    ordering = ('create_time', 'modify_time')


@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ('tag', )


@admin.register(Classify)
class ClassifyModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
