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

def get_html(url = 'https://sindipetrosp.org.br/wp-admin/admin-ajax.php', page_number = 3):
    payload = {}
    headers = {}

    payload = {
        'query_params[post_types]': 'post',
        'query_params[i_attachment]': '',
        'query_params[taxonomies]': '',
        'category': '',
        'query_params[multi_post_types]': '',
        'query_params[multi_taxonomies]': '',
        'query_params[query_types]': '1',
        'query_params[i_taxonomies]': '',
        'query_params[e_taxonomies]': '1322, 1323, 1324, 2684',
        'query_params[i_ids]': '',
        'query_params[cq_operator]': '0',
        'query_params[e_ids]': '',
        'query_params[query_author]': '',
        'query_params[query_offset]': '',
        'query_params[query_include_children]': '1',
        'query_params[today_post]': '0',
        'query_params[datetime_meta]': '',
        'query_params[woo_query]': '0',
        'query_params[post_count]': '-1',
        'query_params[posts_per_page]': '30',
        'query_params[d_i_filter]': '',
        'filter': '',
        'order': 'DESC',
        'orderby': 'date',
        'sub_opt_query[meta_key_query]': '',
        'sub_opt_query[paged]': page_number,
        'sub_opt_query[first_query]': 'off',
        'sub_opt_query[total_pages]': '69',
        'sub_opt_query[items_last_page]': '18',
        'sub_opt_query[query_operator]': '0',
        'sub_opt_query[query_relation]': '1',
        'options[layout_style]': '0',
        'options[button_gallery_name]': 'Gallery',
        'options[grid_style]': '7',
        'options[list_style]': '0',
        'options[carousel_t_style]': '0',
        'options[carousel_f_style]': '0',
        'options[creative_style]': '0',
        'options[timeline_style]': '0',
        'options[block_content_style]': '0',
        'options[sync_slider_style]': '0',
        'options[grid_masonry]': '0',
        'options[show_arrows]': '1',
        'options[arrows_outside]': '0',
        'options[show_dots]': '1',
        'options[infinite]': '1',
        'options[autoplay]': '1',
        'options[autoplayspeed]': '5000',
        'options[scrollperpage]': '1',
        'options[speed]': '500',
        'options[centermode]': '0',
        'options[sync_slider_height_d]': '',
        'options[sync_slider_height_t]': '',
        'options[sync_slider_height_m]': '',
        'options[sync_slider_width_d]': '',
        'options[sync_slider_width_t]': '',
        'options[sync_slider_width_m]': '',
        'options[show_elements]': '0',
        'options[av_content]': '0',
        'options[cc_mobile]': '1',
        'options[cc_portrait_tablet]': '2',
        'options[cc_landscape_tablet]': '3',
        'options[cc_small_desktop]': '3',
        'options[cc_medium_desktop]': '3',
        'options[cc_large_desktop]': '3',
        'options[cc_extra_large_desktop]': '3',
        'options[image_size]': 'penci-thumb-760-570',
        'options[image_size_s]': 'thumbnail',
        'options[s_image]': '1',
        'options[s_image_link]': '1',
        'options[s_image_link_target]': '0',
        'options[s_icon_lightbox_video]': '0',
        'options[video_url_meta]': '0',
        'options[video_url_meta_key]': '',
        'options[s_icon_lightbox_image]': '0',
        'options[s_icon_link]': '0',
        'options[s_icon_link_target]': '0',
        'options[s_image_hover_effect]': '0',
        'options[s_overlay_hover_effect]': '',
        'options[s_overlay_settings]': '0',
        'options[s_overlay_color]': '',
        'options[s_image_post_format]': '0',
        'options[s_image_post_format_pos]': 'ul-bottom-right',
        'options[s_image_avatar]': '0',
        'options[s_title]': '1',
        'options[s_title_limit]': '0',
        'options[s_title_link]': '1',
        'options[s_title_link_target]': '0',
        'options[s_excerpt]': '1',
        'options[s_excerpt_rbtn]': '0',
        'options[s_excerpt_f]': 'get_the_excerpt',
        'options[s_excerpt_sc]': '0',
        'options[s_excerpt_sh]': '0',
        'options[s_excerpt_length]': '0',
        'options[s_categories]': '0',
        'options[s_s_categories]': '0',
        'options[s_s_categories_parent]': '0',
        'options[ex_items_taxonomies]': '',
        'options[s_c_categories]': '0',
        'options[s_ct_categories]': '',
        'options[s_cb_categories]': '',
        'options[s_categories_target]': '0',
        'options[s_metas_o]': '1',
        'options[s_metas_o_author]': '0',
        'options[s_metas_o_author_avatar]': '0',
        'options[s_metas_o_time]': '1',
        'options[time_format]': 'F j, Y',
        'options[s_metas_o_comment]': '0',
        'options[s_metas_o_like]': '0',
        'options[s_metas_o_share]': '0',
        'options[custom_meta_o]': '',
        'options[s_metas_t]': '1',
        'options[s_metas_t_author]': '0',
        'options[s_metas_t_author_avatar]': '0',
        'options[s_metas_t_time]': '0',
        'options[time_format_t]': 'F j, Y',
        'options[s_metas_t_comment]': '0',
        'options[s_metas_t_like]': '0',
        'options[s_metas_t_share]': '1',
        'options[custom_meta_t]': '',
        'options[s_metas_t_readmore]': '1',
        'options[s_metas_t_readmore_link_target]': '0',
        'options[share_text]': 'Compartilhe',
        'options[read_more_text]': 'Leia Mais',
        'options[before_author_text]': '',
        'options[pagination]': '3',
        'options[loadmore_text]': '',
        'options[prev_text]': '',
        'options[next_text]': '',
        'options[animate]': 'default',
        'options[lazyload]': '0',
        'options[lazyload_p]': '',
        'options[geodirectory_rating]': '0',
        'options[quick_view]': '0',
        'options[quick_view_mode]': '0',
        'options[extra_class]': '',
        'options[rnd_id]': 'ul44219',
        'options[s_title_small]': '1',
        'options[s_title_limit_small]': '0',
        'options[s_title_link_small]': '1',
        'options[s_title_link_target_small]': '0',
        'options[s_categories_small]': '1',
        'options[s_s_categories_small]': '0',
        'options[s_s_categories_parent_small]': '0',
        'options[ex_items_taxonomies_small]': '',
        'options[s_c_categories_small]': '0',
        'options[s_ct_categories_small]': '',
        'options[s_cb_categories_small]': '',
        'options[s_categories_target_small]': '0',
        'options[s_metas_o_small]': '1',
        'options[s_metas_o_author_small]': '1',
        'options[s_metas_o_author_avatar_small]': '0',
        'options[s_metas_o_time_small]': '1',
        'options[time_format_small]': 'F j, Y',
        'options[s_metas_o_comment_small]': '1',
        'options[s_metas_o_like_small]': '0',
        'options[s_metas_o_share_small]': '0',
        'options[custom_meta_o_small]': '',
        'options[woo_show_price]': '0',
        'options[woo_show_rating]': '0',
        'options[woo_show_cart]': '0',
        'options[qv_s_title]': '1',
        'options[qv_s_categories]': '1',
        'options[qv_s_s_categories]': '0',
        'options[qv_s_s_categories_parent]': '0',
        'options[qv_ex_items_taxonomies]': '',
        'options[qv_s_c_categories]': '0',
        'options[qv_s_ct_categories]': '',
        'options[qv_s_cb_categories]': '',
        'options[qv_s_categories_target]': '0',
        'options[qv_s_metas_o]': '1',
        'options[qv_s_metas_o_author]': '1',
        'options[qv_s_metas_o_author_avatar]': '0',
        'options[qv_s_metas_o_time]': '1',
        'options[qv_time_format]': 'F j, Y',
        'options[qv_s_metas_o_comment]': '1',
        'options[qv_s_metas_o_like]': '1',
        'options[qv_custom_meta_o]': '',
        'options[qv_show_content]': '1',
        'options[qv_content_stripsc]': '0',
        'options[qv_show_share]': '1',
        'options[qv_woo_show_rating]': '1',
        'options[qv_s_featured_image]': '1',
        'options[goo_ads_client]': '',
        'options[goo_ads_id]': '',
        'options[goo_ads_offset]': '1',
        'options[css_class]': '',
        'random_id': 'ul44219',
        'action': 'ultimatelayoutsajaxaction'
    }

    files=[

    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        "Referer": "https://google.com"
    }

    # sub_opt_query[paged]

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
    html_content = response.text

    return html_content

def get_links_and_dates(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('article')

    locale.setlocale(locale.LC_TIME, "pt_BR.utf8") 

    news_links = []

    for article in articles:
        a = article.find('a')
        link = a.get('href')
        span = article.find('span')
        date = span.text.strip()
        try:
            date = datetime.strptime(date, "%B %d, %Y")
                
            link_date = [link, date]
            news_links.append(link_date)
        except ValueError as e:
            continue


    return news_links

def get_validated_links(news_links, min_date = datetime(2025,6,1)):
    validated_links = []
    next_page = True
    for link, date in news_links:
        if date < min_date:
            next_page = False
            break
        else:
            validated_links.append([link, date])

    return validated_links, next_page

def get_next_page(fnp_url = 'https://sindipetrosp.org.br/wp-admin/admin-ajax.php', next_page_number = 1, min_date = datetime(2025,6,1)):
    validated_news_links = []
    url = fnp_url
    print('obtendo links |', str(url))
    html_content = get_html(url, next_page_number)
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

    title = soup.find('h1').text
    div = soup.find('div', class_='penci-entry-content entry-content')

    paragraphs = div.text.split('\n')
    paragraphs = sanitize_paragraphs(paragraphs)
    
    return title, paragraphs

def sp_extractor(min_date = datetime(2025,6,1)):
    url_default = 'https://sindipetrosp.org.br/wp-admin/admin-ajax.php'
    next_page_number = 1
    validated_news_links = []
    print('obtendo links |', str(url_default))
    html_content = get_html(url_default, next_page_number)
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
    for url, date in validated_news_links:
        print(str(num_url), '/', str(total_urls), '| obtendo textos de', str(url))
        title, paragraphs = get_content_news(url)
        num_paragraph = 1
        num_url += 1
        for paragraph in paragraphs:
            result.append(
                {
                    'sindicato': 'SP',
                    'url' : url,
                    'titulo' : title,
                    'data': date.strftime("%Y-%m-%d"),
                    'paragrafo' : paragraph,
                    'num_paragrafo' : num_paragraph
                }
            )
            num_paragraph += 1

    return result