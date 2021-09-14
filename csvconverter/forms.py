from django import forms
from django.core.exceptions import ValidationError
import os

def csv_check(csvfile):
    csvfile_root, csvfile_ext = os.path.splitext(csvfile)
    if csvfile_ext == '.csv':
        raise ValidationError('csvファイルをインポートしてください')


class UploadForm(forms.Form):
    testfile = forms.FileField(
        #validators=[csv_check],
    )