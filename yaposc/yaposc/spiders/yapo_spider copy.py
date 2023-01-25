import scrapy
import pandas as pd

class YapoSpider(scrapy.Spider):
    name = "yapo2"

    def start_requests(self):
        urls = [
            #'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&cg=1260&q=arriendo&o=1',
            'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=1',
            #'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=2',
            #'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=3',
            #'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&q=arriendo&cg=1260&o=4'
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
                #'camas': ad.css('span.icons__element-text::text').get(),
                #'baños':ad.css('span.icons_e')
            }            
            print('works!')
            print('fecha'+ad.css('span.date::text').get())

    def parse_ad(self, response):
        '''for res in response.css('div.details'):
            yield{
                'precio':res.css('div.price.price-final strong::text').get(),
                'tipo':res.css('tbody tr:nth-child(1).th::text').get(),
            }'''
        for res in response.css('div.details table tbody'):
            yield{
                'precio':res.css('div.price.price-final strong::text').get(),
                res.css('tr:nth-child(2) th::text').get():res.css('tr:nth-child(2) td::text').get(),
                res.css('tr:nth-child(3) th::text').get():res.css('tr:nth-child(3) td::text').get(),
                res.css('tr:nth-child(4) th::text').get():res.css('tr:nth-child(4) td::text').get(),
                res.css('tr:nth-child(5) th::text').get():res.css('tr:nth-child(5) td::text').get(),
                res.css('tr:nth-child(6) th::text').get():res.css('tr:nth-child(6) td::text').get(),
                res.css('tr:nth-child(7) th::text').get():res.css('tr:nth-child(7) td::text').get(),
            }
        '''yield{
            'descripcion':response.css('div.description h4::text').get(),
            'descripcion2':response.css('div.description p::text').get().strip(),
            #'Fecha':response.css('div.da-detail__header-date::text').get(),
            'titulo':response.css('div.da-detail__header h1::text').get(),
        }'''
        for res in response.css('div.da-detail.daview-title'):
            print('******************ENTRO!!!!!!!')
            yield{
                'titulo':res.css('div.da-detail__header div.da-detail__header-date h1.da-detail__header-title ::text').get(),
            }
        print(response.css('div.da-detail__header-date::text').get())

    def parse(self, response):
        '''page = response.url.split("=")[4]
        filename = f'yapo-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')'''
        for ad in response.css('tr.ad.listing_thumbs'):
            '''yield{
                'fecha': ad.css('span.date::text').get(),
                'hora' : ad.css('span.hour::text').get(),
                'link' : ad.css('a::attr(href)').get(),
                'anuncio': ad.css('a.title::text').get(),
                'precio': ad.css('span.price::text').get().strip(),
                'uf': ad.css('span.convertedPrice::text').get().strip(),
                'Region': ad.css('span.region::text').get(),
                'Comuna': ad.css('span.commune::text').get(),
                'tipo anuncio': ad.css('span.company_ad::text').get(),
                #'camas': ad.css('span.icons__element-text::text').get(),
                #'baños':ad.css('span.icons_e')
            }'''
            link = ad.css('a::attr(href)').get()
            yield scrapy.Request(url=link, callback=self.parse_ad)
            #print('works!')
            #print('fecha'+ad.css('span.date::text').get())
#scrapy crawl yapo --set DOWNLOAD_DELAY=3