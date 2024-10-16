from flask import Flask, request, render_template, jsonify
from flask import redirect, url_for
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import time
import requests
import sys
import os
from datetime import datetime
from textblob import TextBlob
import pymongo


#import getPdfFile

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['WebScraping']
collection = db['ArXiv2']



def akademik_arama(anahtar_kelimeler, sonuc_sayisi):
    yayinlar = []
    RESULTS_PER_PAGE = 50

    MAX_SAYFA = int(sonuc_sayisi / RESULTS_PER_PAGE)

    if not os.path.exists('D:/VsCode Projeler/YAZLAB2/1-WebScraping/Pdf/'):
        os.makedirs('D:/VsCode Projeler/YAZLAB2/1-WebScraping/Pdf/')

    for sayfa in range(0, MAX_SAYFA):
        # baslangic_indisi = sayfa * RESULTS_PER_PAGE
        # url = f'https://arxiv.org/search/?query={anahtar_kelimeler}&searchtype=all&source=header'


        baslangic_indisi = sayfa * RESULTS_PER_PAGE
        url = f'https://arxiv.org/search/?query={anahtar_kelimeler}&searchtype=all&source=header&size={RESULTS_PER_PAGE}&start={baslangic_indisi}'

        response = requests.get(url)

        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')

            for entry in soup.find_all('li', attrs={'class': 'arxiv-result'})[:RESULTS_PER_PAGE]:

                yayinId = entry.find('p', attrs={'class': 'list-title is-inline-block'}).text.strip()[6:16]


                text = entry.find('p', attrs={'class': 'title is-5 mathjax'}).text.strip()


                authors_tag = entry.find('p', attrs={'class': 'authors'})
                authors = ', '.join([author.text.strip() for author in
                                     authors_tag.find_all(['a'])]) if authors_tag else 'Authors not found'
                authors = authors.split(',')


                abstract = entry.find('p', attrs={'class': 'abstract mathjax'}).text.strip()[9:]


                pub_date_tag = entry.find('p', attrs={'class': 'is-size-7'})
                pub_date = pub_date_tag.text.strip()[9:].split(';')[0] if pub_date_tag else 'Publication date not found'
                pub_date = months(pub_date)


                urlMakale = entry.find('div', attrs={'class': 'is-marginless'}).find('a')['href']


                pdf_url_tag = entry.find('div', attrs={'class': 'is-marginless'}).find('a', string='pdf')
                pdfUrl = pdf_url_tag['href'] if pdf_url_tag else 'PDF link not found'
                #getPdfFile.downloadPdfFile(pdfUrl,yayinId+'.pdf')
                #downloadPdfFile(pdfUrl,yayinId+'.pdf')


                makale_response = requests.get(urlMakale)
                makale_soup = BeautifulSoup(makale_response.text, 'html.parser')

                subject_span = makale_soup.find('td', attrs={'class': 'tablecell subjects'})
                subjects = subject_span.text.strip() if subject_span else 'Subject not found'
                subjects = subjects.split(';')


                get_doi = makale_soup.find('td', class_='tablecell arxivdoi')
                doi_num = get_doi.find('a').get('href').strip() if get_doi and get_doi.find('a') else 'Doi not found'


                yayin = {
                    'yayinId': yayinId,
                    'baslik': text,
                    'yazarlar': authors,
                    'abstract': abstract,
                    'pub_date': pub_date,
                    'urlMakale': urlMakale,
                    'pdfUrl': pdfUrl,
                    'subjects': subjects,
                    'keyword': anahtar_kelimeler,
                    'doi': doi_num
                }


                collection.insert_one(yayin)
                yayinlar.append(yayin)


            time.sleep(2)

        else:

            print(f'Hata! {response.status_code}')
            break

    return yayinlar

def downloadFile(url, fileName):

    if not os.path.exists(fileName):
         response = requests.get(url)

         if response.status_code == 200:
             with open(fileName, 'wb') as pdf_file:
                 pdf_file.write(response.content)
         else:
             print(f'Hata! PDF indirilemedi. {response.status_code}')
    else:
         print(f'{fileName} zaten var, indirme işlemi atlandı.')

         
def downloadPdfFile(url,filename):
    scriptPath = sys.path[0]+'\\pdf'
    downloadPath = os.path.join(scriptPath, '')

    downloadFile(url, downloadPath+filename)



def months(pub_date):
    month_list = ["January,", "February,", "March,", "April,", "May,", "June,", "July,", "August,", "September,",
                  "October,", "November,", "December,"]
    month = pub_date.split()
    i = 0
    while i < len(month_list):
        if month[1] == month_list[i]:
            break
        i += 1

    if (i + 1) < 10:
        month[1] = "0" + str(int(i + 1))
    else:
        month[1] = str(int(i + 1))

    if int(month[0]) < 10:
        month[0] = "0" + str(month[0])

    month = str(month[0]) + "-" + str(month[1]) + "-" + str(month[2])

    return month




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        anahtar_kelimeler = request.form['anahtar_kelimeler']
        sonuc_sayisi = int(request.form['sonuc_sayisi'])
        sonuclar = akademik_arama(anahtar_kelimeler, sonuc_sayisi)
        sonuclar_db = collection.find()
        return render_template('index2.html', sonuclar=sonuclar_db, anahtar_kelimeler=anahtar_kelimeler)
    else:
        authors = set()
        for document in collection.find():
            if 'yazarlar' in document:
                authors.update(document['yazarlar'])
        keywords = []
        for document in collection.find():
            if 'keyword' in document:
                keywords.append(document['keyword'])
        keywords = list(set(keywords))
        sonuclar_db = collection.find()
        return render_template('index2.html', sonuclar=sonuclar_db, authors=sorted(authors), keywords=sorted(keywords))




@app.route('/selectAll', methods=['POST'])
def selectAll():
    selectedKeyword = request.form.get('keyword')
    selected_author = request.form.get('author')
    secilen_tarih = request.form.get('tarih_secimi')

    # Başlangıçta temiz bir filtre oluştur
    filter_dict = {}

    # Yazar filtresini ekle (seçiliyse)
    if selected_author and selected_author != 'Seçiniz':
        filter_dict["yazarlar"] = selected_author

    # Tarih filtresini ekle (seçiliyse)
    if secilen_tarih and secilen_tarih != 'gg.aa.yyyy':
        try:
            selected_date = datetime.strptime(secilen_tarih, "%Y-%m-%d")
            selected_date2 = selected_date.strftime("%d-%m-%Y")
            filter_dict["pub_date"] = selected_date2
        except ValueError as e:
            print("Tarih formatı uyumsuz:", e)

    # Anahtar kelime filtresini ekle (seçiliyse)
    if selectedKeyword and selectedKeyword != 'Seçiniz':
        filter_dict["keyword"] = selectedKeyword

    # Eğer hiçbir filtre seçilmediyse, tüm verileri getir
    if not filter_dict:
        result = collection.find({}, {"baslik": 1, "yazarlar": 1, "pub_date": 1, "yayinId":1, "_id": 0})
    else:
        # Diğer durumlarda, filtrelenmiş sonuçları getir
        result = collection.find(filter_dict, {"baslik": 1, "yazarlar": 1, "pub_date": 1, "yayinId":1, "_id": 0})

    articles = list(result)
    return render_template('results.html', sonuc=articles)




# sort_by_date fonksiyonunu tanımlayın
def sort_by_date(articles, sorting_type):
    if sorting_type == 'eskiden_yeniye':
        sorted_articles = sorted(articles, key=lambda x: datetime.strptime(x['pub_date'], '%d-%m-%Y'))
    elif sorting_type == 'yeniden_eskiye':
        sorted_articles = sorted(articles, key=lambda x: datetime.strptime(x['pub_date'], '%d-%m-%Y'), reverse=True)
    else:
        sorted_articles = articles

    return sorted_articles

# sorted_date endpoint'ini tanımlayın
@app.route('/sorted_date', methods=['POST'])
def sorted_date():
    sorting_type = request.form['sorting_type']

    # Tüm makaleleri getir
    articles = collection.find({}, {"baslik": 1, "yazarlar": 1, "pub_date": 1, "yayinId": 1, "_id": 0})

    # Tarihe göre sırala
    sorted_articles = sort_by_date(articles, sorting_type)

    return render_template('sorted_date.html', sorted_articles=sorted_articles)




@app.route('/makale/<yayinId>')
def makale_detay(yayinId):
    makale = collection.find_one({'yayinId': yayinId})

    if not makale:
        return "Makale bulunamadı."

    return render_template('makale_detay.html', makale=makale)





@app.route('/article_search', methods=['POST'])
def article_search():
    if request.method == 'POST':
        search_text = request.form['search']

        # Yazım hatalarını kontrol et ve düzeltilmiş metni al
        blob = TextBlob(search_text)
        corrected_search_text = str(blob.correct())

        
        if corrected_search_text != search_text:
            # Yazım hatası uyarısı 
            warning_message = f"Yazım hatası var. Doğrusu: {corrected_search_text}"
            return render_template('index2.html', search_text=search_text, warning_message=warning_message, has_warning=True)

        # kelimeye göre arama 
        regex_pattern = f'.*{search_text}.*'
        result = collection.find({
            '$or': [
                {"baslik": {'$regex': regex_pattern, '$options': 'i'}},
                {"keyword": {'$regex': regex_pattern, '$options': 'i'}}
            ]
        })
        # Arama sonuçlarını bir liste haline getir
        search_results = [doc for doc in result]

        return render_template('search_results.html', search_text=search_text, results=search_results, has_warning=False)



if __name__ == '__main__':
    app.run(debug=True)