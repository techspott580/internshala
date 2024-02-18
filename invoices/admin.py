from django.contrib import admin
from .models import Invoice, InvoiceDetail

class InvoiceDetailInline(admin.TabularInline):
    model = InvoiceDetail
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer_name')
    inlines = [InvoiceDetailInline]

admin.site.register(Invoice, InvoiceAdmin)
