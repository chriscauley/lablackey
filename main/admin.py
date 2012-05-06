from django.contrib import admin

class OrderedAdmin(admin.ModelAdmin):
  readonly_fields = ("order",)
  list_editable = ("order",)
  list_display = ("__str__","order")

class OrderedInline(admin.ModelAdmin):
  sortable_field_name = "order"
