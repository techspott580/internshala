from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        invoice_details = validated_data.pop('invoice_details', [])
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in invoice_details:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice

    def update(self, instance, validated_data):
        invoice_details = validated_data.pop('invoice_details', [])
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.save()

        # Delete existing details before creating/updating new ones
        InvoiceDetail.objects.filter(invoice=instance).delete()
        for detail_data in invoice_details:
            InvoiceDetail.objects.create(invoice=instance, **detail_data)
        return instance
