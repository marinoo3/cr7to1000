import requests
from bs4 import BeautifulSoup
import os


class MessiVSRonaldo():

    def __init__(self) -> None:
        
        self.base_url = 'https://www.messivsronaldo.app/'


    def __player_url(self, name='', id='') -> str:

        url = f'{self.base_url}/{name}/{id}/'
        return url


    def __parse_stats(self, html) -> dict:

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select('div[class*="RonaldoStatsBlock"]')[0]
        total = table.select('li[class*="StatsBlock-module--goals"]')[0]
        number = total.select('span[class*="statNum"]')[0]

        stats = {
            'goals': stats['goals'] + int(number.text)
        }

        return stats
    

    def get_player_stat(self, name='', id='') -> dict:

        url = self.__player_url(name, id)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        os.chdir('/Users/marinnagy/Documents/Programmation/Python/cr7 to 1000/web')
        with open('response.html', 'w') as file:
            file.write(response.text)
        stats = self.__parse_stats(response.text)

        return stats