from django.contrib import admin
from django.db import models
from django.forms.widgets import HiddenInput

class OrderedModelAdmin(admin.ModelAdmin):
  exclude = ("order",)
  list_editable = ("order",)
  list_display = ("__unicode__","order")

class OrderedModelInline(admin.TabularInline):
  formfield_overrides = {
    models.PositiveIntegerField: {'widget': HiddenInput},
    }
  sortable_field_name = "order"

class SlugModelAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title",)}

class ColumnModelAdmin(admin.ModelAdmin):
  list_filter = ('column',)
