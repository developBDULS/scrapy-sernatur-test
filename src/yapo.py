import pandas as pd
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

site = 'https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&l=0&q=arriendo&w=1&cmn='
wd = webdriver.Chrome('chromedriver',options=options)
wd.get(site)
html = wd.page_source
yp = pd.read_html(html)

print(yp)