from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Invoice

#以下はxhtml2pdf関係
#import os
#from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
#from django.contrib.staticfiles import finders
import datetime

# Create your views here.
import calendar

#xhtml2pdfの関数
class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice/list.html'


#xhtml2pdfの関数
def invoice_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    invoice = get_object_or_404(Invoice, pk=pk)
    #DateFieldの「DATE」と「Payment Due」の値を取得
    m_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    w_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    #DATE
    invoice_Date_month = invoice.date.month
    invoice_Date_month = m_list[invoice_Date_month - 1]
    invoice_Date_weekday = invoice.date.weekday()
    invoice_Date_weekday = w_list[invoice_Date_weekday]
    #Payment Due
    invoice_PaymentDate_month = invoice.payment_due.month
    invoice_PaymentDate_month = m_list[invoice_PaymentDate_month - 1]
    invoice_PaymentDate_weekday = invoice.payment_due.weekday()
    invoice_PaymentDate_weekday = w_list[invoice_PaymentDate_weekday]
    
    template_path = 'invoice/invoice.html'
    context = {
       'invoice': invoice,
       'invoice_Date_month': invoice_Date_month,
       'invoice_Date_weekday': invoice_Date_weekday,
       'invoice_PaymentDate_month': invoice_PaymentDate_month,
       'invoice_PaymentDate_weekday': invoice_PaymentDate_weekday,
       }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #もしその画面に行った時にPDFを自動でダウンロードさせたいのであれば下記の1行を記述
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #もしダウンロードさせるのではなく表示させたいのであれば下記の1行を記述
    response['Content-Disposition'] = 'filename="invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


