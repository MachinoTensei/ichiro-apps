from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from csvconverter.forms import UploadForm, UploadForm2
from csvconverter.functions import process_file,to_csv,update_file,to_csv2 #functions.pyで定義した関数を使うために読み込み
import csv,io
import pandas as pd

# Create your views here!
def CsvUploadView(request):
    if request.method == 'POST':
        upload = UploadForm(request.POST, request.FILES)
        if upload.is_valid():
            data = pd.read_csv(request.FILES['testfile'], encoding="shift-jis", delimiter=',', header=3)
            df = process_file(data)
            df['Metafield: SellerUserName [single_line_text_field]'] = request.user.company #最後の列に1列カラムを追加して、どのユーザーか（会社名）を記入
            response = to_csv(df)
            return response
        
        upload2 = UploadForm2(request.POST, request.FILES)
        if upload2.is_valid():
            data2_1 = pd.read_csv(request.FILES['testfile2_1'], encoding="")
            data2_2 = pd.read_csv(request.FILES['testfile2_2'], encoding="")
            df2 = update_file(data2_1, data2_2)
            response2 = to_csv2(df2)
            return response2

    else:
        upload = UploadForm()
        upload2 = UploadForm2()
        return render(request, "csvconverter/csvupload.html", {'form':upload, 'form2':upload2})


