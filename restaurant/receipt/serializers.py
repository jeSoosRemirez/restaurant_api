from rest_framework import serializers
from .models import Printer, Receipt


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


class GenerateReceiptSerializer(serializers.Serializer):
    printer_api_key = serializers.CharField()
    receipt_type = serializers.ChoiceField(choices=Receipt.RECEIPT_TYPES)
    order = serializers.JSONField()

    def create(self, validated_data):
        printer_api_key = validated_data['printer_api_key']
        receipt_type = validated_data['receipt_type']
        order = validated_data['order']

        try:
            printer = Printer.objects.get(api_key=printer_api_key, receipt_type=receipt_type)
        except Printer.DoesNotExist:
            raise serializers.ValidationError("Printer not found.")

        receipt = Receipt.objects.create(
            printer=printer,
            type=receipt_type,
            order=order,
            status='new'
        )

        return receipt
