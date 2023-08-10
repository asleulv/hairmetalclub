from django import forms
from django.contrib import admin
from django.templatetags.static import static
from django.utils.html import format_html
from .models import TextBlock, TagGroup, Tag, Album

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_group')

class TagGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_color')
    
    def display_color(self, obj):
        return format_html('<div style="width: 20px; height: 20px; background-color: {};"></div>', obj.color)

    display_color.short_description = 'Color'

class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ['artist_slug', 'title_slug']  # Exclude the slug fields from the form

class AlbumAdmin(admin.ModelAdmin):
    form = AlbumAdminForm

admin.site.register(TextBlock)
admin.site.register(TagGroup, TagGroupAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Album, AlbumAdmin)
