import requests
import sys
import os

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


