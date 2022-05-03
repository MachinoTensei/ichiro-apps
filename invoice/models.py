from django.db import models
from django.utils import timezone
from django.conf import Settings, settings



#model(モデル)とは...
#どんなものをDBに保存していくか決めるのがmodels.py


#PDF記入モデル
class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True)
    invoice_number = models.CharField('INVOICE No.', max_length=150)
    date = models.DateField(default=timezone.now)
    consignee_name = models.CharField('名前（Consignee）', max_length=150, blank=True)
    consignee_address = models.CharField('住所（Consignee）', max_length=500, blank=True)
    consignee_tel = models.CharField('電話番号（Consignee）', max_length=150, blank=True)
    consignee_fax = models.CharField('FAX（Consignee）', max_length=150, blank=True)
    Notify_Party = models.CharField('Notify_Party', max_length=150, blank=True)
    shipped_per = models.CharField('Shipped_per', max_length=150, blank=True)
    on_or_about = models.CharField('On or About', max_length=150, blank=True)
    to = models.CharField('To', max_length=150, blank=True)
    final_destination = models.CharField('Final Destination', max_length=150, blank=True)
    payment_terms = models.CharField('Payment Terms', max_length=150, default='100% before due date by Bank Transfer', blank=True)
    payment_due = models.DateField('Payment Due')
    bank_account = models.TextField('Bank Account', blank=True)
    beneficiary_info_name = models.CharField('Name（Beneficiarys Information）', max_length=150, blank=True)
    beneficiary_info_address = models.CharField('Address（Beneficiarys Information）', max_length=150, blank=True)
    beneficiary_info_tel = models.CharField('Tel（Beneficiarys Information）', max_length=150, blank=True)
    item_description = models.TextField('Item Description', blank=True)
    insurance = models.CharField('Insurance', max_length=150, blank=True)
    total_price = models.CharField('Total Price', max_length=150, blank=True)
    updated = models.DateTimeField('更新日', auto_now=True)
    created = models.DateTimeField('作成日', auto_now=True)

    def __str__(self):
        return str(self.invoice_number)
