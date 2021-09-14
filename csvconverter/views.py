from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from csvconverter.forms import UploadForm
from csvconverter.functions import process_file,to_csv
import csv,io
import pandas as pd

# Create your views here!
def CsvUploadView(request):
    if request.method == 'POST':
        upload = UploadForm(request.POST, request.FILES)
        if upload.is_valid():
            data = pd.read_csv(request.FILES['testfile'], encoding="shift-jis", delimiter=',', header=2)
            df = process_file(data)
            response = to_csv(df)
            return response
    else:
        upload = UploadForm()
        return render(request, "csvconverter/csvupload.html", {'form':upload})