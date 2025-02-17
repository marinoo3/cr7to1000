import requests
from bs4 import BeautifulSoup
import json
import os


class TransferMarkt():

    def __init__(self) -> None:
        
        self.url = 'https://www.transfermarkt.com/cristiano-ronaldo/alletore/spieler/8198/plus/1?saison=&verein=&liga=&wettbewerb=&pos=&minute=&pos=&torart=&stand='


    def __string_to_dict(string):

        # Convert string to JSON-compatible format
        json_string = '{"' + string.replace(": ", '": ').replace(", ", ', "') + '}'

        # Parse the JSON string to a dictionary
        result = json.loads(json_string)

        print(result)  # Output: {'match': 1, 'player': 3}
        return result


    def __parse_stats(self, html):

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select('div.row .responsive-table table')[0]
        total = table.select('tr > td')[0]

        string = total.text.lower().replace(';', ',')
        stats = self.__string_to_dict(string)

        return stats
    

    def get_player_stat(self, name='', id=''):

        response = requests.get(self.url)
        os.chdir('/Users/marinnagy/Documents/Programmation/Python/cr7 to 1000/web')
        with open('response.html', 'w') as file:
            file.write(response.text)
        stats = self.__parse_stats(response.text)

        return stats