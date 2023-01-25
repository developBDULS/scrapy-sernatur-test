from requests_html import HTMLSession

session = HTMLSession()
r = session.get('https://www.yapo.cl/coquimbo/arriendo_temporada?ca=5_s&l=0&q=arriendo&w=1&cmn=')

r.html.find('tr')
print(r.html.links)