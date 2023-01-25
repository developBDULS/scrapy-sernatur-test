import scrapy
import pandas as pd
from scrapy.http import headers
import pathlib

class YapoSpider(scrapy.Spider):
    name = "tripadvisor"
    df = pd.DataFrame(columns=['anuncio','descripcion','dormitorios','baños','capacidad','link'])
    base = 'https://tripadvisor.cl'
    base_path = str(pathlib.Path().absolute())
    
    def start_requests(self):
        urls = [
            'file:///C:/Users/develop/Documents/workspace/python/sernatur/yaposc/static/tripadvisor_1.html',
            'file:///C:/Users/develop/Documents/workspace/python/sernatur/yaposc/static/tripadvisor_2.html',
            'file:///C:/Users/develop/Documents/workspace/python/sernatur/yaposc/static/tripadvisor_3.html',
            #'{}{}'.format(self.base_path, '\\static\\tripadvisor_2.html'),
            #'{}{}'.format(self.base_path, '\\static\\tripadvisor_3.html'),
            #'https://www.tripadvisor.cl/VacationRentals-g2615208-Reviews-Coquimbo_Region-Vacation_Rentals.html',
            #'https://www.tripadvisor.cl/VRACSearch-g2615208-Reviews-oa50-Coquimbo_Region-Vacation_Rentals.html?oa=50',
            #'https://www.tripadvisor.cl/VRACSearch-g2615208-Reviews-oa100-Coquimbo_Region-Vacation_Rentals.html?oa=100',            
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)        
        print('============================')
        print(self.base_path)
        print('============================')
    
    def parse_ad(self, response):
        cell = {}
        current_ad = response.meta['current_ad']        
        description = response.css('div.VGN0nqph::text').get()#correcto
        cell = {
            'anuncio':current_ad['anuncio'],
            'link':current_ad['link'],
            'descripcion':description,
            'dormitorios':current_ad['dormitorios'],
            'baños':current_ad['baños'],
            'capacidad':current_ad['capacidad']
        }
        try:
           self.df = pd.read_excel('tripadvisor-datos-region-coquimbo_st.xlsx',engine='openpyxl',index_col=0)
        except:
            self.df = pd.DataFrame(columns=['anuncio','descripcion','dormitorios','baños','capacidad','link'])
        
        self.df = self.df[self.df.columns.drop(list(self.df.filter(regex='Unnamed:')))]
        self.df = self.df.append(cell, ignore_index=True)
        self.df.to_excel('tripadvisor-datos-region-coquimbo_st.xlsx') 
        

    def parse(self, response):    
        for ad in response.css('div._1L5PA1gU'):            
            link_clipped = ad.css('a::attr(href)').get()
            link = '{}{}'.format(self.base,link_clipped)
            current_ad = {
                'anuncio': ad.css('h2._2K0y-IXo a::text').get(),
                'link': link_clipped,
                'dormitorios':ad.css('div._3PfoU1uf:nth-child(1) div.M1tanZPN::text').get(),
                'baños':ad.css('div._3PfoU1uf:nth-child(2) div.M1tanZPN::text').get(),
                'capacidad':ad.css('div._3PfoU1uf:nth-child(3) div.M1tanZPN::text').get(),                
            }
            yield scrapy.Request(url=link_clipped, callback=self.parse_ad, meta={'current_ad':current_ad})#yield
            
