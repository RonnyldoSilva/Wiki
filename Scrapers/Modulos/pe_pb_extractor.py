import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re
import locale
import urllib3
import emoji
import json

# Suppress the InsecureRequestWarning specifically
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_token():
    url = "https://sindipetropepb.org.br/wp-admin/admin-ajax.php" 
    payload = 'action=eael_get_token'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://google.com",
        "Cookie": "ci_session=dc1e4779c1d8a2e8921e1102b67c0ac1ab173dc2",
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    html_content = response.text
    
    data = json.loads(html_content)
    token = data['data']['nonce']

    return token

def get_html_news(url):
    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://google.com",
        "Cookie": "ci_session=dc1e4779c1d8a2e8921e1102b67c0ac1ab173dc2"
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    html_content = response.text

    return html_content

def get_html(url = "https://sindipetropepb.org.br/wp-admin/admin-ajax.php", page_number = 1, token = ''):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://google.com"
    }
    payload = {'action': 'load_more',
        'class': 'Essential_Addons_Elementor\\Elements\\Post_Grid',
        'args': 'orderby=date&order=desc&ignore_sticky_posts=1&post_status=publish&posts_per_page=4&offset=0&post_type=post',
        'page': page_number,
        'page_id': '5855',
        'widget_id': '702100d',
        'nonce': token,
        'template_info[dir]': 'lite',
        'template_info[file_name]': 'two.php',
        'template_info[name]': 'Post-Grid'}
    files=[

    ]

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
    html_content = response.text

    clean_html = json.loads(html_content)

    return clean_html

def get_links_and_dates(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article')

    locale.setlocale(locale.LC_TIME, "pt_BR.utf8") 

    news_links = []

    for article in articles:
        a = article.find('a')
        link = a.get('href')
        span = article.find('time')
        date = span.text.strip()
        title = article.find('h2', class_='eael-entry-title').text.strip()
        try:
            date = datetime.strptime(date, "%d de %B de %Y")
            link_date = [link, date, title]
            news_links.append(link_date)
        except ValueError as e:
            print(e)
            continue


    return news_links

def get_validated_links(news_links, min_date = datetime(2025,6,1)):
    validated_links = []
    next_page = True
    for link, date, title in news_links:
        if date < min_date:
            next_page = False
            break
        else:
            validated_links.append([link, date, title])

    return validated_links, next_page

def get_next_page(fnp_url = 'https://sindipetropepb.org.br/wp-admin/admin-ajax.php', next_page_number = 1, min_date = datetime(2025,6,1)):
    validated_news_links = []
    url = fnp_url
    print('obtendo links |', str(url))
    token = get_token()
    html_content = get_html(url, next_page_number, token)
    news_links = get_links_and_dates(html_content)
    validated_links, next_page = get_validated_links(news_links, min_date)

    for validated_link in validated_links:
        validated_news_links.append(validated_link)

    if next_page:
        validated_links = get_next_page(fnp_url, next_page_number + 1, min_date)
        
        for validated_link in validated_links:
            validated_news_links.append(validated_link)

    return validated_news_links

def sanitize_paragraphs(paragraphs:list, min_paragraph_len = 500, concat_trigger_size = 1500):
    '''
    sanitiza os parágrafos, realizando replace de partes de strings e concatenando parágrafos
    
    paragraphs: lista de parágrafos
    min_paragraph_len: define quais parágrafos devem ser concatenados
    concat_trigger_size: caso o tamanho da concatenação de textos esteja acima desse valor, 
                            escreve como parágrafo e reseta a variável que armazena as 
                            strings a serem concatenadas
    '''
    def append_paragraphs(current_new_paragraph):
        new_paragraphs.append(current_new_paragraph.strip())
    
    paragraphs = [emoji.demojize(paragraph) for paragraph in [paragraph\
                                                              .replace('\xa0',' ')\
                                                              .replace('\n',' ')\
                                                              .replace('\t',' ')\
                                                              .replace('[email-protected]', '')\
                                                              .strip() \
                                                              for paragraph in paragraphs] \
                  if len(paragraph)>0] #removendo emoji, tratanto texto e realizando strip para então construir lista de parágrafos que tenham len > 0
    paragraphs_mask = [len(paragraph) < min_paragraph_len for paragraph in paragraphs] # true são os abaixo do min_paragraph_len, precisarao ser tratados
    if any(paragraphs_mask): #caso algum elemento precise ser tratado, trigga processo
        new_paragraphs = []
        current_new_paragraph = ''
        for i in range(len(paragraphs)):
            if len(current_new_paragraph) >= concat_trigger_size:
                append_paragraphs(current_new_paragraph)
                current_new_paragraph = ''
            if paragraphs_mask[i]: #caso seja menor que o min_paragraph_len
                current_new_paragraph = current_new_paragraph + ' ' + paragraphs[i]
                if i == len(paragraphs)-1: #caso seja o ultimo elemento
                    append_paragraphs(current_new_paragraph)
            else:
                current_new_paragraph = current_new_paragraph + '' + paragraphs[i]
                append_paragraphs(current_new_paragraph)
                current_new_paragraph = ''
        paragraphs = new_paragraphs
                    
    return paragraphs

def get_content_news(url):
    html_content = get_html_news(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    div = soup.find('div', class_='cm-entry-summary')

    paragraphs = div.text.split('\n')
    paragraphs = sanitize_paragraphs(paragraphs)
    
    return paragraphs

def pe_pb_extractor(min_date = datetime(2025,6,1)):
    url_default = 'https://sindipetropepb.org.br/wp-admin/admin-ajax.php'
    next_page_number = 1
    validated_news_links = []
    token = get_token()
    print('obtendo links |', str(url_default))
    html_content = get_html(url_default, next_page_number, token)
    news_links = get_links_and_dates(html_content)
    validated_links, next_page = get_validated_links(news_links, min_date)

    for validated_link in validated_links:
        validated_news_links.append(validated_link)

    if next_page:
        validated_links = get_next_page(url_default, next_page_number + 1, min_date)
        
        for validated_link in validated_links:
            validated_news_links.append(validated_link)

    result = []
    total_urls = len(validated_news_links)
    num_url = 1
    for url, date, title in validated_news_links:
        print(str(num_url), '/', str(total_urls), '| obtendo textos de', str(url))
        paragraphs = get_content_news(url)
        num_paragraph = 1
        num_url += 1
        for paragraph in paragraphs:
            result.append(
                {
                    'sindicato': 'PE_PB',
                    'url' : url,
                    'titulo' : title,
                    'data': date.strftime("%Y-%m-%d"),
                    'paragrafo' : paragraph,
                    'num_paragrafo' : num_paragraph
                }
            )
            num_paragraph += 1

    return result