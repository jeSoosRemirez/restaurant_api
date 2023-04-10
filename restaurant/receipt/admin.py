from django.contrib import admin
from .models import Printer, Receipt


class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'receipt_type', 'point_id')


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('id', 'printer_id', 'type', 'status', 'pdf_file')
    list_filter = ('printer_id', 'type', 'status')
    readonly_fields = ('pdf_file',)


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Receipt, ReceiptAdmin)
