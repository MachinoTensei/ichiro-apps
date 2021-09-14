import pandas as pd
import numpy as np
import sklearn,csv,re,os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from django.http import HttpResponse
from mysite.settings import BASE_DIR
import datetime

def process_file(data):
    #train_x = pd.read_csv("app/static/files/train_x.csv")
    #train_y = pd.read_csv("app/static/files/train_y.csv")
    #train_x = pd.read_csv(os.path.join(BASE_DIR, 'csvconverter/static/files/train_x_modified.csv'))
    #train_y = pd.read_csv(os.path.join(BASE_DIR, 'csvconverter/static/files/train_y_modified.csv'))
    tcv_csv = data

    #お好きなようにデータ処理ここから
    sort_columns = ['ReferenceNo','Handle','CommandType','title','Body HTML','Make','BodyStyle1','Options','Tags Command','Created At','Updated At','Status','Published','Published At','Published Scope','Template Suffix','Gift Card','Row #','Top Row','Custom Collections','ImageFiles','Image Command','Image Position','Image Width','Image Height','Image Alt Text','Variant ID','Variant Command','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant Generate From Options','Variant Position','Variant SKU','Variant Weight','Variant Weight Unit','Variant HS Code','Variant Country of Origin','Price','Variant Compare At Price','Variant Cost','Variant Requires Shipping','Variant Taxable','Variant Tax Code','Variant Barcode','Variant Image','Variant Inventory Tracker','Variant Inventory Policy','Variant Fulfillment Service','Variant Inventory Qty','Variant Inventory Adjust','YearMonth','Model','GradeTrim','GradeTrimDomestic','Mileage','ModelCode','VINSerialNo','Currency','BodyStyle2','Steering','Transmission','Door','Displacement','Passengers','FuelType','DriveType','ExteriorColor','InteriorColor','Condition','CheckYearMonth','MechanicalProblem','Options','Comments','CommentsDomestic','VehicleWidth','VehicleLength','VehicleHeight','ItemType','Domestic','Overseas','Title','PriceDomestic','PayTrade','MileageOption','Staff','Comment','LayingDate','LayingCost','LayingCostCurrency','LayingSupplier','IsPostedOption']
    #列の並び替え順を指定
    tcv_csv = tcv_csv.reindex(columns=sort_columns) #shopify形式になるように並び替え

    tcv_csv.columns = ['ID','Handle','Command','Title','Body HTML','Vendor','Type','Tags','Tags Command','Created At','Updated At','Status','Published','Published At','Published Scope','Template Suffix','Gift Card','Row #','Top Row','Custom Collections','Image Src','Image Command','Image Position','Image Width','Image Height','Image Alt Text','Variant ID','Variant Command','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant Generate From Options','Variant Position','Variant SKU','Variant Weight','Variant Weight Unit','Variant HS Code','Variant Country of Origin','Variant Price','Variant Compare At Price','Variant Cost','Variant Requires Shipping','Variant Taxable','Variant Tax Code','Variant Barcode','Variant Image','Variant Inventory Tracker','Variant Inventory Policy','Variant Fulfillment Service','Variant Inventory Qty','Variant Inventory Adjust','Metafield: YearMonth [string]','Metafield: Model [string]','Metafield: GradeTrim [string]','Metafield: GradeTrimDomestic [string]','Metafield: Mileage [integer]','Metafield: ModelCode [string]','Metafield: VINSerialNo [string]','Metafield: Currency [string]','Metafield: BodyStyle2 [string]','Metafield: Steering [string]','Metafield: Transmission [string]','Metafield: Door [integer]','Metafield: Displacement [integer]','Metafield: Passengers [integer]','Metafield: FuelType [string]','Metafield: DriveType [string]','Metafield: ExteriorColor [string]','Metafield: InteriorColor [string]','Metafield: Condition [string]','Metafield: CheckYearMonth [string]','Metafield: MechanicalProblem [string]','Metafield: Option [string]','Metafield: Comments [string]','Metafield: CommentsDomestic [string]','Metafield: VehicleWidth [integer]','Metafield: VehicleLength [integer]','Metafield: VehicleHeight [integer]','Metafield: ItemType [string]','Metafield: Domestic [string]','Metafield: Overseas [string]','Metafield: title [string]','Metafield: PriceDomestic [string]','Metafield: PayTrade [string]','Metafield: MileageOption [string]','Metafield: Staff [string]','Metafield: Comment [string]','Metafield: LayingDate [string]','Metafield: LayingCost [string]','Metafield: LayingCostCurrency [string]','Metafield: LayingSupplier [string]','Metafield: IsPostedOption [string]']
    #ヘッダー名を変更

    tcv_csv = tcv_csv.dropna(how='all', axis=0) #全てNaNの行を削除
    tcv_csv = tcv_csv.replace({'Command':{'Add': 'MERGE', 'Delete': 'DELETE'}}) #値を置き換え
    tcv_csv = tcv_csv.fillna({'Command': 'IGNORE', 'Status': 'Active', 'Published': 'TRUE', 'Published Scope': 'global'}) #NaNを穴埋め

    indexNum = len(tcv_csv) #行数取得

    #Title列の値を変更する記述
    YearMonthColumns = tcv_csv['Metafield: YearMonth [string]']
    VendorColumns = tcv_csv['Vendor']
    ModelColumns = tcv_csv['Metafield: Model [string]']

    titleTitleList = []

    for i in range(indexNum):
        titleYearMonth = tcv_csv.at[i, 'Metafield: YearMonth [string]']
        titleVendor = tcv_csv.at[i, 'Vendor']
        titleModel = tcv_csv.at[i, 'Metafield: Model [string]']
        titleTitle = str(titleYearMonth) + ' ' + str(titleVendor) + ' ' + str(titleModel)
        titleTitleList.append(titleTitle)
        
    tcv_csv['Title'] = titleTitleList

    
    #Options(Tagsの方)の<>をコンマ区切りに変換する記述
    TagsColumns = tcv_csv['Tags']
    tagList = []
    for i in TagsColumns:
        i = str(i)
        i = i.replace('<','').replace('>',', ').replace('/','')
        tagList.append(i)

    tcv_csv['Tags'] = tagList
    
    #ImageSrcを所定の形式に変更する記述
    ImageSrcColumns = tcv_csv['Image Src']
    ImageSrcList = []
    for i in ImageSrcColumns:
        i = i.replace('<','').replace('>','; ')
        ImageSrcList.append(i)

    tcv_csv['Image Src'] = ImageSrcList

    
    #Options(metafieldsの方)の<>をHTMLタグにする記述
    OptionsColumns = tcv_csv['Metafield: Option [string]']
    OptionsList = []
    for i in OptionsColumns:
        i = str(i)
        i = i.replace('<','@').replace('>','¥').replace('/','')
        i = i.replace('@','<li>').replace('¥','</li>')
        OptionsList.append(i)

    tcv_csv['Metafield: Option [string]'] = OptionsList

    #ReferenceNoをHandleに設定して、IDは空欄が推奨のため空欄にする。
    tcv_csv['Handle'] = tcv_csv['ID']
    tcv_csv['ID'] = ''
    
    #お好きなようにデータ処理ここまで

    df_result = tcv_csv #最後にcsvに変換したいデータフレームとして返す

    return df_result

def to_csv(df):
    #ここからオリジナルで追加
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y-%m-%d--%H-%M-%S')
    #ここまでオリジナルで追加
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="result.csv"'

    df.to_csv(path_or_buf = response, encoding = 'utf-8-sig', index=False)

    return response