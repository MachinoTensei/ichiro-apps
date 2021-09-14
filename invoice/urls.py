from django.urls import path
from invoice import views
from .views import InvoiceListView, invoice_render_pdf_view

app_name = 'invoice'

urlpatterns = [
    path('list/', InvoiceListView.as_view(), name='list'),
    path('pdf/<pk>/', invoice_render_pdf_view, name='invoice-pdf-view'),
]