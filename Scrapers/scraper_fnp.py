import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from tqdm import tqdm

def get_html(url):
    payload = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://google.com"
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    html_content = response.text

    return html_content

def get_links_and_dates(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article')

    news_links = []

    for article in articles:
        a = article.find('a')
        link = a.get('href')
        span = article.find('span')
        date = span.text.strip()
        date = datetime.datetime.strptime(date, '%d/%m/%Y')
        link_date = [link, date]
        news_links.append(link_date)

    return news_links

def get_validated_links(news_links, min_date = datetime.datetime(2025,6,1)):
    validated_links = []
    next_page = True
    for link, date in news_links:
        if date < min_date:
            next_page = False
            break
        else:
            validated_links.append([link, date])

    return validated_links, next_page

def get_next_page(fnp_url, next_page_number = 1):
    validated_news_links = []
    url = fnp_url + 'page/' + str(next_page_number) + '/'
    html_content = get_html(url)
    news_links = get_links_and_dates(html_content)
    validated_links, next_page = get_validated_links(news_links)

    for validated_link in validated_links:
        validated_news_links.append(validated_link)

    if next_page:
        validated_links = get_next_page(fnp_url, next_page_number + 1)
        
        for validated_link in validated_links:
            validated_news_links.append(validated_link)

    return validated_news_links

def clean_paragraphs(paragraphs):
    return paragraphs

def get_content_news(url):
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    title = soup.find('h1').text
    paragraphs = soup.find_all('p')

    paragraphs = clean_paragraphs(paragraphs)

    return title, paragraphs

def main():
    fnp_urls = [
        'https://fnpetroleiros.org.br/category/diversos/',
        'https://fnpetroleiros.org.br/category/post_category/',
        'https://fnpetroleiros.org.br/category/artigos/',
        'https://fnpetroleiros.org.br/category/petrobras/',
        'https://fnpetroleiros.org.br/category/brasil/',
        'https://fnpetroleiros.org.br/category/mundo/',
        'https://fnpetroleiros.org.br/category/eleicoes/',
        'https://fnpetroleiros.org.br/category/direitos/'
    ]

    # Getting News Links

    next_page_number = 1
    validated_news_links = []
    for fnp_url in fnp_urls:
        url = fnp_url + 'page/' + str(next_page_number) + '/'
        html_content = get_html(url)
        news_links = get_links_and_dates(html_content)
        validated_links, next_page = get_validated_links(news_links)

        for validated_link in validated_links:
            validated_news_links.append(validated_link)

        if next_page:
            validated_links = get_next_page(fnp_url, next_page_number + 1)
            
            for validated_link in validated_links:
                validated_news_links.append(validated_link)

    # Getting Paragraphs

    result = []
    for url, date in tqdm(validated_news_links):
        title, paragraphs = get_content_news(url)

        num_paragraph = 1
        for paragraph in paragraphs:
            result.append(
                {
                    'sindicato': 'FNP',
                    'url' : url,
                    'titulo' : title,
                    'data': str(validated_news_links[0][1]).split(' ')[0],
                    'paragrafo' : paragraph.text,
                    'num_paragrafo' : num_paragraph
                }
            )
            num_paragraph += 1

    return result

