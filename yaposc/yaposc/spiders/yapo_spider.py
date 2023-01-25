from os import sep
import scrapy
import pandas as pd
import numpy as np
from scrapy.http import headers

class YapoSpider(scrapy.Spider):
    name = "yapo"
    df = pd.DataFrame(columns=['precio','Tipo de inmueble','Comuna','Dormitorios','Baños','Servicios'])

    def start_requests(self):
        urls = [
            #'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&cg=1260&q=arriendo&o=1',
            'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=1',
            'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=2',
            'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=3',
            'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=4'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)        

    def extract_data(self, res):
        for ad in res.css('tr.ad.listing_thumbs'):
            yield{
                'fecha': ad.css('span.date::text').get(),
                'hora' : ad.css('span.hour::text').get(),
                'link' : ad.css('a::attr(href)').get(),
                'anuncio': ad.css('a.title::text').get(),
                'precio': ad.css('span.price::text').get().strip(),
                'uf': ad.css('span.convertedPrice::text').get().strip(),
                'Region': ad.css('span.region::text').get(),
                'Comuna': ad.css('span.commune::text').get(),
                'tipo anuncio': ad.css('span.company_ad::text').get(),
            }

            

    def parse_ad(self, response):
        cell = {}
        precio=''
        current_ad = response.meta['current_ad']
        print(current_ad)
        try:
            precio = response.css('div.price.price-final strong::text').get().strip()
        except:
            precio = 'Sin informacion'

        for res in response.css('div.details table tbody'):           
            cell = {
                'precio':precio,
                'anuncio':current_ad['anuncio'],
                'fecha':current_ad['fecha'],
                'hora':current_ad['hora'],
                'Region':current_ad['Region'],
                res.css('tr:nth-child(2) th::text').get():res.css('tr:nth-child(2) td::text').get(),
                res.css('tr:nth-child(3) th::text').get():res.css('tr:nth-child(3) td::text').get(),
                res.css('tr:nth-child(4) th::text').get():res.css('tr:nth-child(4) td::text').get(),
                res.css('tr:nth-child(5) th::text').get():res.css('tr:nth-child(5) td::text').get(),
                res.css('tr:nth-child(6) th::text').get():res.css('tr:nth-child(6) td::text').get(),
                res.css('tr:nth-child(7) th::text').get():res.css('tr:nth-child(7) td::text').get(),
                'Descripcion':response.css('div.description p::text').get().strip(),
                'link':response.request.url
            }            
           
            try:
                self.df = pd.read_excel('yapo-testing.xlsx',engine='openpyxl',index_col=0)
            except:
                self.df = pd.DataFrame(columns=['precio','Tipo de inmueble','Comuna','Dormitorios','Baños','Servicios'])

            #sr = pd.Series(data=cell)
            #df_tmp = pd.DataFrame([list(data)], columns=columns)
            self.df = self.df[self.df.columns.drop(list(self.df.filter(regex='Unnamed:')))]

            self.df = self.df.append(cell,ignore_index=True)

            self.df.to_excel('yapo-testing.xlsx') 

    def parse(self, response):        
        for ad in response.css('tr.ad.listing_thumbs'):            
            link = ad.css('a::attr(href)').get()
            current_ad = {
                'fecha': ad.css('span.date::text').get(),
                'hora' : ad.css('span.hour::text').get(),
                'Region': ad.css('span.region::text').get(),
                'anuncio': ad.css('a.title::text').get(),
            }
            yield scrapy.Request(url=link, callback=self.parse_ad, meta={'current_ad':current_ad})#yield
            

#scrapy crawl yapo --set DOWNLOAD_DELAY=3