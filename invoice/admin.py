from django.contrib import admin
from .models import Invoice

# Register your models here.

#Django 管理サイト名変更
admin.site.site_header = 'ICHIRO EC'
admin.site.index_title = 'ichiro 管理画面'

#管理画面に追加したいモデルを記載していく。（モデルとは、models.pyで作ったclassのこと）
admin.site.register(Invoice)