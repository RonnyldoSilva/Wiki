import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import re
import locale
import urllib3
import emoji

# Suppress the InsecureRequestWarning specifically
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_html(url = 'https://sindipetro-es.org.br/noticias-2/'):
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    html_content = response.text

    return html_content

def texto_para_datetime(texto: str) -> datetime:
    texto = texto.lower().replace("ago", "").strip()  # normaliza
    
    agora = datetime.now()
    
    if "segundo" in texto:
        qtd = int(texto.split()[0])
        return agora - timedelta(seconds=qtd)
    elif "minuto" in texto:
        qtd = int(texto.split()[0])
        return agora - timedelta(minutes=qtd)
    elif "hora" in texto:
        qtd = int(texto.split()[0])
        return agora - timedelta(hours=qtd)
    elif "dia" in texto:
        qtd = int(texto.split()[0])
        return agora - timedelta(days=qtd)
    else:
        raise ValueError(f"Formato não reconhecido: {texto}")

def get_links_and_dates(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    spans = soup.find_all('span', class_='post_meta_item post_date')

    locale.setlocale(locale.LC_TIME, "pt_BR.utf8") 

    news_links = []

    for span in spans:
        a = span.find('a')
        link = a.get('href')
        date = span.text.strip()

        today = re.match(r".*ago$", date, re.IGNORECASE)

        if today:
            date = texto_para_datetime(date)
        else:
            date = datetime.strptime(date, "%d/%m/%Y")
            
        link_date = [link, date]
        news_links.append(link_date)

    return news_links

def get_validated_links(news_links, min_date = datetime(2025,6,1)):
    validated_links = []
    for link, date in news_links:
        if date < min_date:
            break
        else:
            validated_links.append([link, date])

    return validated_links

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
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')

    title = soup.find('h1').text
    div = soup.find('div', class_='post_content post_content_single entry-content')

    paragraphs = div.find_all('p')

    paragraphs_text = [p.get_text(strip=True) for p in paragraphs]
    #paragraphs = paragraphs.text.split('\n')
    paragraphs = sanitize_paragraphs(paragraphs_text)

    return title, paragraphs

def es_extractor(min_date = datetime(2025,6,1)):
    url = 'https://sindipetro-es.org.br/noticias-2/'
    print('obtendo links |', str(url))
    html_content = get_html(url)
    news_links = get_links_and_dates(html_content)
    validated_news_links = get_validated_links(news_links, min_date)

    result = []
    total_urls = len(validated_news_links)
    num_url = 1
    for url, date in validated_news_links:
        print(str(num_url), '/', str(total_urls), '| obtendo textos de', str(url))
        title, paragraphs = get_content_news(url)
        num_url += 1
        num_paragraph = 1
        for paragraph in paragraphs:
            result.append(
                {
                    'sindicato': 'ES',
                    'url' : url,
                    'titulo' : title,
                    'data': date.strftime("%Y-%m-%d"),
                    'paragrafo' : paragraph,
                    'num_paragrafo' : num_paragraph
                }
            )
            num_paragraph += 1

    return result