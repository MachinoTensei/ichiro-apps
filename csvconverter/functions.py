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

    #お好きなようにデータ処理ここから-----------------------------------------------------------------------------------------------------------------------

    sort_columns = ['ReferenceNo','Handle','CommandType','title','Body HTML','Make','BodyStyle1','Options','Tags Command','Created At','Updated At','Status','Published','Published At','Published Scope','Template Suffix','Gift Card','Row #','Top Row','Custom Collections','ImageFiles','Image Command','Image Position','Image Width','Image Height','Image Alt Text','Variant ID','Variant Command','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant Generate From Options','Variant Position','Variant SKU','Variant Weight','Variant Weight Unit','Variant HS Code','Variant Country of Origin','Price','Variant Compare At Price','Variant Cost','Variant Requires Shipping','Variant Taxable','Variant Tax Code','Variant Barcode','Variant Image','Variant Inventory Tracker','Variant Inventory Policy','Variant Fulfillment Service','Variant Inventory Qty','Variant Inventory Adjust','YearMonth','Model','GradeTrim','GradeTrimDomestic','Mileage','ModelCode','VINSerialNo','Currency','BodyStyle2','Steering','Transmission','Door','Displacement','Passengers','FuelType','DriveType','ExteriorColor','InteriorColor','Condition','CheckYearMonth','MechanicalProblem','Options','Comments','CommentsDomestic','VehicleWidth','VehicleLength','VehicleHeight','ItemType','Domestic','Overseas','Title','PriceDomestic','PayTrade','MileageOption','Staff','Comment','LayingDate','LayingCost','LayingCostCurrency','LayingSupplier','IsPostedOption']
    #列の並び替え順を指定
    tcv_csv = tcv_csv.reindex(columns=sort_columns) #shopify形式になるように並び替え

    tcv_csv.columns = ['ID','Handle','Command','Title','Body HTML','Vendor','Type','Tags','Tags Command','Created At','Updated At','Status','Published','Published At','Published Scope','Template Suffix','Gift Card','Row #','Top Row','Custom Collections','Image Src','Image Command','Image Position','Image Width','Image Height','Image Alt Text','Variant ID','Variant Command','Option1 Name','Option1 Value','Option2 Name','Option2 Value','Option3 Name','Option3 Value','Variant Generate From Options','Variant Position','Variant SKU','Variant Weight','Variant Weight Unit','Variant HS Code','Variant Country of Origin','Variant Price','Variant Compare At Price','Variant Cost','Variant Requires Shipping','Variant Taxable','Variant Tax Code','Variant Barcode','Variant Image','Variant Inventory Tracker','Variant Inventory Policy','Variant Fulfillment Service','Variant Inventory Qty','Variant Inventory Adjust','Metafield: YearMonth [single_line_text_field]','Metafield: Model [single_line_text_field]','Metafield: GradeTrim [single_line_text_field]','Metafield: GradeTrimDomestic [single_line_text_field]','Metafield: Mileage [number_integer]','Metafield: ModelCode [single_line_text_field]','Metafield: VINSerialNo [single_line_text_field]','Metafield: Currency [single_line_text_field]','Metafield: BodyStyle2 [single_line_text_field]','Metafield: Steering [single_line_text_field]','Metafield: Transmission [single_line_text_field]','Metafield: Door [number_integer]','Metafield: Displacement [number_integer]','Metafield: Passengers [number_integer]','Metafield: FuelType [single_line_text_field]','Metafield: DriveType [single_line_text_field]','Metafield: ExteriorColor [single_line_text_field]','Metafield: InteriorColor [single_line_text_field]','Metafield: Condition [single_line_text_field]','Metafield: CheckYearMonth [single_line_text_field]','Metafield: MechanicalProblem [multi_line_text_field]','Metafield: Option [multi_line_text_field]','Metafield: Comments [multi_line_text_field]','Metafield: CommentsDomestic [multi_line_text_field]','Metafield: VehicleWidth [number_integer]','Metafield: VehicleLength [number_integer]','Metafield: VehicleHeight [number_integer]','Metafield: ItemType [single_line_text_field]','Metafield: Domestic [single_line_text_field]','Metafield: Overseas [single_line_text_field]','Metafield: title [single_line_text_field]','Metafield: PriceDomestic [single_line_text_field]','Metafield: PayTrade [single_line_text_field]','Metafield: MileageOption [multi_line_text_field]','Metafield: Staff [single_line_text_field]','Metafield: Comment [multi_line_text_field]','Metafield: LayingDate [single_line_text_field]','Metafield: LayingCost [single_line_text_field]','Metafield: LayingCostCurrency [single_line_text_field]','Metafield: LayingSupplier [single_line_text_field]','Metafield: IsPostedOption [single_line_text_field]']
    #ヘッダー名を変更

    tcv_csv = tcv_csv.dropna(how='all', axis=0) #全てNaNの行を削除
    tcv_csv = tcv_csv.replace({'Command':{'Add': 'MERGE', 'Delete': 'DELETE'}}) #値を置き換え
    tcv_csv = tcv_csv.fillna({'Command': 'IGNORE', 'Status': 'Active', 'Published': 'TRUE', 'Published Scope': 'global'}) #NaNを穴埋め

    indexNum = len(tcv_csv) #行数取得

    #Title列の値を変更する記述
    YearMonthColumns = tcv_csv['Metafield: YearMonth [single_line_text_field]']
    VendorColumns = tcv_csv['Vendor']
    ModelColumns = tcv_csv['Metafield: Model [single_line_text_field]']

    titleTitleList = []

    for i in range(indexNum):
        titleYearMonth = tcv_csv.at[i, 'Metafield: YearMonth [single_line_text_field]']
        titleVendor = tcv_csv.at[i, 'Vendor']
        titleModel = tcv_csv.at[i, 'Metafield: Model [single_line_text_field]']
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
        i = str(i)
        i = i.replace('<','').replace('>','; ')
        ImageSrcList.append(i)

    tcv_csv['Image Src'] = ImageSrcList

    
    #Options(metafieldsの方)の<>をHTMLタグにする記述
    OptionsColumns = tcv_csv['Metafield: Option [multi_line_text_field]']
    OptionsList = []
    for i in OptionsColumns:
        i = str(i)
        i = i.replace('<','@').replace('>','¥').replace('/','')
        i = i.replace('@','<li>').replace('¥','</li>')
        OptionsList.append(i)

    tcv_csv['Metafield: Option [multi_line_text_field]'] = OptionsList

    #ReferenceNoをHandleに設定して、IDは空欄が推奨のため空欄にする。
    tcv_csv['Handle'] = tcv_csv['ID']
    tcv_csv['ID'] = ''

    #JPY登録のものをUSDに直す
    JPY_TTB = 109 #為替相場
    for num in range(indexNum):
        if tcv_csv.at[num, 'Metafield: Currency [single_line_text_field]'] == 'JPY':
            tcv_csv.at[num, 'Variant Price'] = round(tcv_csv.at[num, 'Variant Price'] / JPY_TTB)
    

    #お好きなようにデータ処理ここまで-----------------------------------------------------------------------------------------------------------------------
    
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


#新旧ファイルを見比べて更新するプログラム
def update_file(data2_1, data2_2):
    old_csv = data2_1#エクスポートした旧CSV
    new_csv = data2_2#新しく持ってきた新CSV

    #お好きなようにデータ処理ここから-----------------------------------------------------------------------------------------------------------------------

    OldIndexNum = len(old_csv) #旧csvの行数取得
    NewIndexNum = len(new_csv) #新csvの行数取得

    #旧csvのHandleを1つずつ取り出していき、新csvのHandleと照合
    delete_list = [] #deleteコマンドにするHandleを溜めていく配列を宣言
    for i in range(OldIndexNum):
        delete_count = 0 #照合してイコールではなかった回数をカウント
        for j in range(NewIndexNum):
            if old_csv.at[i, 'Handle'] == new_csv.at[j, 'Handle']: #もし旧Handleが新csvにもあったら
                new_csv.at[j, 'Handle'] = 1234567890 #1234567890(重複を示す)とする→後でその行は削除
                delete_count = 0 #揃った時点でカウントをゼロにしないとそのHandleまでdelete_listに追加されてしまう
                break
            elif old_csv.at[i, 'Handle'] != new_csv.at[j, 'Handle']: #もし旧Handleが新csvになかったら
                delete_count += 1
        if delete_count >= 1:
            delete_list += [old_csv.at[i, 'Handle']] #deleteコマンドにするHandleを溜めていく
    
    #delete_listに溜めたHandleをdeleteコマンドで新csvに追加していく
    for delete_handle in delete_list:
        new_csv=new_csv.append({'Handle' : delete_handle, 'Command' : 'DELETE'} , ignore_index=True)
    
    #1234567890を持つ行を削除
    new_csv = new_csv.drop(new_csv.index[(new_csv['Handle'] == 1234567890)])

    #お好きなようにデータ処理ここまで-----------------------------------------------------------------------------------------------------------------------

    df_result = new_csv #最後にcsvに変換したいデータフレームとして返す

    return df_result


def to_csv2(df2):
    #ここからオリジナルで追加
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y-%m-%d--%H-%M-%S')
    #ここまでオリジナルで追加
    response = HttpResponse(content_type='text/csv; charset=UTF-8')
    response['Content-Disposition'] = 'attachment; filename="update.csv"'

    df2.to_csv(path_or_buf = response, encoding = 'utf-8-sig', index=False)

    return response