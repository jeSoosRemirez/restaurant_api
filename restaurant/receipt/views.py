from rest_framework import viewsets, generics, status
from .models import Printer, Receipt
from .serializers import PrinterSerializer, ReceiptSerializer, GenerateReceiptSerializer
from .tasks import generate_pdf
from rest_framework.response import Response


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class GenerateReceiptView(generics.CreateAPIView):
    serializer_class = GenerateReceiptSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the printer exists
        printer = Printer.objects.filter(
            # point_id=serializer.validated_data['point_id'],
            api_key=serializer.validated_data['printer_api_key'],
            receipt_type=serializer.validated_data['receipt_type']
        ).first()
        if not printer:
            return Response({'error': 'Printer not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the receipt already exists for this order
        existing_receipts = Receipt.objects.filter(order=serializer.validated_data['order'])
        if existing_receipts.exists():
            return Response({'error': 'Receipt for this order already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the receipt
        receipt = Receipt.objects.create(
            printer=printer,
            type=serializer.validated_data['receipt_type'],
            order=serializer.validated_data['order']
        )

        # Set asynchronous tasks for generating PDF files
        generate_pdf.delay(receipt.id, receipt.type)

        return Response({'success': f'Receipt generated with id {receipt.id}'}, status=status.HTTP_201_CREATED)
