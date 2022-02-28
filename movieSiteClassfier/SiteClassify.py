import sklearn
import joblib
import requests
import chardet
from lxml import etree
import jieba
import numpy as np


MAX_HREF_NUM = 1000

def predict_url(url):
    """
    args:
    url : The site Url to be classify: Movie Site or Not Movie Site
    Returns:
    1 : Movie Site
    0 : Not Movie Site
    False : Request Failed
    """
    model = joblib.load('movie_website.pkl')
    tfidf = joblib.load('tfi-idf.pkl')
    try:
        response = requests.get(url, timeout=5)
    except:
        return False
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.text)
    if html is None:
        return False
#     html_data = html.xpath('//*[@href]/text()')  # 只选取“带有链接”的文本
    html_data = html.xpath('//*[name(.)!="style" and name(.)!="script"]/text()')
    if len(html_data) >= MAX_HREF_NUM:  # 只选取前多少个带有链接的文本
        html_data = html_data[:MAX_HREF_NUM]
        
    one_item = ''
    for item in html_data:
        item = item.strip()
        one_item += ' '
        one_item += item
    
    item_text = []
    text = [i for i in one_item.split()]
    for i in text:
        for j in jieba.cut(i, cut_all=False):
            item_text.append(j)
    item_text = ' '.join(item_text)
    out= []
    out.append(item_text)
    out = np.array(out).reshape(-1,)
    out_tf = tfidf.transform(out).toarray()
    result = model.predict(out_tf)[0]
    return int(result)


def predict_file(file_path):
    model = joblib.load('movie_website.pkl')
    tfidf = joblib.load('tf-idf.pkl')
    with open(file_path, 'rb') as f:
        results = f.read()
        code = chardet.detect(results)
        try:
            if code['encoding'] is None:
                results = results.decode('utf8')
            else:
                results = results.decode(code['encoding'])
        except UnicodeDecodeError:
            try:
                results = results.decode('GB18030')
            except UnicodeDecodeError:
                try:
                    results = results.decode('utf8', errors='ignore')
                except:
                    return False
        html = etree.HTML(results)
        if html is None:
            return False
#         html_data = html.xpath('//*[@href]/text()')
        html_data = html.xpath('//*[name(.)!="style" and name(.)!="script"]/text()')
        if len(html_data) >= MAX_HREF_NUM:  # 只选取前多少个带有链接的文本
            html_data = html_data[:MAX_HREF_NUM]
            
    one_item = ''
        
    for item in html_data:
        item = item.strip()
        one_item += ' '
        one_item += item
    
    item_text = []
    text = [i for i in one_item.split()]
    for i in text:
        for j in jieba.cut(i, cut_all=False):
            item_text.append(j)
    item_text = ' '.join(item_text)
    out= []
    out.append(item_text)
    out = np.array(out).reshape(-1,)
    out_tf = tfidf.transform(out).toarray()
    result = model.predict(out_tf)
    return int(result)