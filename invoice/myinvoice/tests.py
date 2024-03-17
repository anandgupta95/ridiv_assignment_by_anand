from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail

class InvoiceAPITests(APITestCase):
    def setUp(self):
        self.invoice_data = {
            'date': '2024-03-16',
            'customer_name': 'Anand'
        }
        self.invoice = Invoice.objects.create(**self.invoice_data)

        self.detail_data = {
            'invoice': self.invoice,
            'description': 'invoice description',
            'quantity': 1,
            'unit_price': '1.50',
            'price': '1.50'
        }
        self.invoice_detail = InvoiceDetail.objects.create(**self.detail_data)

    def test_invoice(self):
        url = reverse('invoice')
        data = {'date': '2023-04-24', 'customer_name': 'Anand'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(Invoice.objects.get(pk=response.data['id']).customer_name, 'Anand')

    def test_fetch_invoice_list(self):
        url = reverse('invoice')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customer_name'], 'Anand')

    def test_fetch_invoice(self):
        url = reverse('detail', args=[self.invoice.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_name'], 'Anand')

    def test_update_invoice(self):
        url = reverse('detail',args=[self.invoice.id])
        data = {'date':'2024-03-18','customer_name':'Himanshu'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(pk=self.invoice.id).customer_name, 'Himanshu')

    def test_delete_invoice(self):
        url = reverse('detail', args=[self.invoice.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
