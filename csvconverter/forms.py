from django import forms
from django.core.exceptions import ValidationError
import os

def csv_check(csvfile):
    csvfile_root, csvfile_ext = os.path.splitext(csvfile)
    if csvfile_ext == '.csv':
        raise ValidationError('csvファイルをインポートしてください')


#csv変換用フォーム
class UploadForm(forms.Form):
    testfile = forms.FileField(
        #validators=[csv_check],
    )


#更新作業用フォーム
class UploadForm2(forms.Form):
    testfile2_1 = forms.FileField(
    )
    testfile2_2 = forms.FileField(
    )