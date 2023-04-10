from django.db import models


class Printer(models.Model):
    PRINTER_TYPES = [
        ('client', 'Client'),
        ('kitchen', 'Kitchen'),
    ]
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=64, unique=True)
    receipt_type = models.CharField(max_length=7, choices=PRINTER_TYPES)
    point_id = models.IntegerField()

    def __str__(self):
        return self.name


class Receipt(models.Model):
    RECEIPT_TYPES = [
        ('client', 'Client'),
        ('kitchen', 'Kitchen'),
    ]

    ORDER_STATUS = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    ]

    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=RECEIPT_TYPES)
    order = models.JSONField()
    status = models.CharField(max_length=11, choices=ORDER_STATUS, default='new')
    pdf_file = models.FileField(blank=True, null=True, upload_to='./media/pdf')

    def __str__(self):
        return self.name
