import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class OpenGraphScraper:
    def __init__(self, url):
        self.url = url
        print(url)
        self.opengraph_data = {}

    def fetch_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        return None

    def extract_opengraph(self, soup):
        meta_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        for tag in meta_tags:
            property_name = tag.get('property')[3:]
            self.opengraph_data[property_name] = tag.get('content')

    def extract_favicon(self, soup):
        favicon = None
        favicon_tag = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
        if favicon_tag:
            favicon_url = favicon_tag.get('href')
            if favicon_url:
                favicon = urljoin(self.url, favicon_url)
        return favicon

    def get_page_description(self, soup):
        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description:
            return meta_description.get('content')
        return None

    def get_opengraph_data(self):
        html = self.fetch_html()
        #print(html)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            self.extract_opengraph(soup)
            
            if not self.opengraph_data.get('title'):
                self.opengraph_data['title'] = soup.title.string.strip() if soup.title else None
            
            if not self.opengraph_data.get('description'):
                self.opengraph_data['description'] = self.get_page_description(soup)
            
            self.opengraph_data['favicon'] = self.extract_favicon(soup)

            return self.opengraph_data
        return None

    def to_json(self, data):
        return json.dumps(data, indent=4)
