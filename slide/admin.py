from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Slide


class SlideAdminForm(forms.ModelForm):
    config = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Slide
        fields = ('title', 'alias', 'hide', 'content', 'config', 'style')


class SlideAdmin(admin.ModelAdmin):
    form = SlideAdminForm
    list_display = ['title', 'alias', 'hide', 'created_time', 'preview']
    list_editable = ['hide']
    save_on_top = True

    def preview(self, obj):
        url = reverse('slide', args=(obj.alias, ))
        return mark_safe('<a href="{}" target="_blank">查看</a>'.format(url))
    preview.short_description = '地址'


admin.site.register(Slide, SlideAdmin)
