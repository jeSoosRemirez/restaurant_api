import os
import tempfile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from models import Receipt


class Command(BaseCommand):
    help = 'Generate PDF files for receipts'

    def add_arguments(self, parser):
        parser.add_argument('receipt_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for receipt_id in options['receipt_ids']:
            receipt = Receipt.objects.get(id=receipt_id)

            if receipt.pdf_file:
                # Receipt already has a PDF file, skip it
                continue

            # Render the receipt template
            context = {'receipt': receipt}
            html = render_to_string('receipt_template.html', context)

            # Generate a PDF file from the HTML using wkhtmltopdf
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False) as f:
                f.write(os.popen('wkhtmltopdf - -'.split(), 'wb').communicate(input=html.encode())[0])
                pdf_file = default_storage.save(f.name, f)

            # Update the receipt with the PDF file path
            receipt.pdf_file = pdf_file
            receipt.save()
