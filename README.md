EN
------------
Academic Web Scraping Application
This project is a web application that scrapes academic publications from academic search engines like ArXiv, stores the data in a MongoDB database, and processes HTML content using BeautifulSoup. The application also allows users to search, view, and dynamically filter the scraped data.

Features
1. Web Scraping:
At least 10 academic publications are scraped from the selected academic search engine based on user-provided keywords.
For each publication, the following data is scraped:
Title
Author names
Publication type (article, conference paper, book, etc.)
Publication date
Publisher information
Keywords
Abstract
References
Citation count
DOI (if available)
URL
PDF files related to the publications are downloaded, and additional information may be extracted from their content.
2. Database:
The scraped data is stored in a MongoDB database.
The database is structured to store all the necessary information related to the publications.
3. Web Interface:
Users can search for publications using keywords and view the results through the web interface.
The search results can be dynamically filtered from the database.
Spelling errors in search queries are automatically corrected, and suggestions are provided.
Publications can be sorted by publication date or citation count.
Clicking on a publication will display more detailed information on a separate page.
Technologies Used
Backend: Python (web scraping using Selenium and BeautifulSoup)
Database: MongoDB
HTML Processing: BeautifulSoup
Frontend: HTML, CSS, JavaScript (or any preferred framework)
Other: PDF processing with PyPDF2 or a similar library
Setup and Execution
Requirements:
Python 3.x
MongoDB
To install the required Python packages, run the following command:
pip install -r requirements.txt
------------
TR
------------
Akademik Web Kazıma (Scraping) Uygulaması
Bu proje, ArXiv gibi akademik arama motorlarından web kazıma yöntemiyle akademik yayınların bilgilerini elde eden, bu verileri MongoDB veritabanında saklayan ve BeautifulSoup kullanarak HTML içeriklerini işleyen bir web uygulamasıdır. Ayrıca, uygulama üzerinden arama yapma, verileri görüntüleme ve dinamik filtreleme gibi işlemler yapılabilmektedir.

Özellikler
1. Web Kazıma:
Kullanıcı tarafından girilen anahtar kelimelere göre en az 10 akademik yayın, seçilen akademik arama motoru üzerinden kazınarak elde edilir.
Her yayının:
Yayın adı
Yazar isimleri
Yayın türü (makale, konferans bildirisi, kitap vb.)
Yayın tarihi
Yayıncı bilgisi
Anahtar kelimeler
Özet
Referanslar
Alıntı sayısı
DOI numarası (varsa)
URL adresi bilgileri kazınır.
Yayınlara ait PDF dosyaları indirilir ve içeriklerinden de ek bilgiler alınabilir.
2. Veritabanı:
Kazılan veriler MongoDB veritabanına kaydedilir.
Veritabanı, yayınlarla ilgili tüm gerekli bilgileri tutacak şekilde yapılandırılmıştır.
3. Web Arayüzü:
Kullanıcılar anahtar kelimelerle arama yapabilir ve sonuçları web arayüzü üzerinden görüntüleyebilir.
Arama sonuçları veritabanından dinamik olarak filtrelenebilir.
Arama esnasında yazım hataları otomatik düzeltilir ve öneriler sunulur.
Yayınlar, yayımlanma tarihi ya da alıntı sayısına göre sıralanabilir.
Her bir yayının detaylarına tıklayarak ayrı bir sayfada daha fazla bilgi görüntülenebilir.
Kullanılan Teknolojiler
Backend: Python (Selenium, BeautifulSoup ile web kazıma)
Veritabanı: MongoDB
HTML İşleme: BeautifulSoup
Frontend: HTML, CSS, JavaScript (veya tercih edilen bir framework)
Diğer: PDF işlemleri için PyPDF2 veya benzeri bir kütüphane
Kurulum ve Çalıştırma
Gereksinimler:
Python 3.x
MongoDB
Gerekli Python paketlerini yüklemek için:
pip install -r requirements.txt
