import os
import tempfile
from celery import shared_task
from django.template.loader import render_to_string
from django.conf import settings
from .models import Receipt


@shared_task
def generate_pdf(receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    if not receipt:
        return
    receipt_type = receipt.type
    template_name = f'receipts/{receipt_type}.html'
    context = {'order': receipt.order}
    html = render_to_string(template_name, context)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(html.encode('utf-8'))
        tmp.flush()
        output_filename = f'{receipt_id}_{receipt_type}.pdf'
        output_path = os.path.join(settings.MEDIA_ROOT, 'pdf', output_filename)
        command = f'wkhtmltopdf -q {tmp.name} {output_path}'
        os.system(command)
    receipt.status = 'rendered'
    receipt.pdf_file.name = f'pdf/{output_filename}'
    receipt.save()
