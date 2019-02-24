# coding: utf-8
import os, time, zipfile
from decimal import Decimal
from datetime import date
from django.conf import settings
from .common import CrawlerUtils
from pathlib import Path
import requests

class CrawlerPDF(CrawlerUtils):

    def download_pdf(self):
        # self.goTo('https://www.tjpe.jus.br/dje/djeletronico?visaoId=tjdf.djeletronico.comum.internet.apresentacao.VisaoDiarioEletronicoInternetPorData')
        # time.sleep(15)

        # self.click('/html/body/div/form/div/table/tr/td/a[@href]/')
        # print('ok')
        # t = self.element_exists('/html/body/')
        # print(t)

        filename = Path('metadata.pdf')
        url = 'http://www.tjpe.jus.br/dje/DownloadServlet?dj=DJ39_2019-ASSINADO.PDF&statusDoDiario=ASSINADO'
        response = requests.get(url, verify=False)
        filename.write_bytes(response.content)
        

