import requests
from bs4 import BeautifulSoup


class FlashScore():

    def __init__(self) -> None:
        
        self.base_url = 'https://www.flashscore.fr/joueur'
        self.friendly_goals = 44


    def __player_url(self, name='', id=''):

        url = f'{self.base_url}/{name}/{id}/'
        return url


    def __parse_stats(self, html):

        stats = {
            'plays': 0,
            'goals': self.friendly_goals,
            'assists': 0,
            'yellow_cards': 0,
            'red_cards': 0
        }

        for category in ['league', 'nacional-cup', 'international-cups', 'national-team']:

            soup = BeautifulSoup(html, 'html.parser')
            table = soup.select(f'div.careerTab#{category}')[0]
            total = table.select('div.careerTab__row--total')[0]

            stats = {
                'plays': stats['plays'] + int(total.select('div.careerTab__stat--2')[0].text),
                'goals': stats['goals'] + int(total.select('div.careerTab__stat--3')[0].text),
                'assists': stats['assists'] + int(total.select('div.careerTab__stat--4')[0].text),
                'yellow_cards': stats['yellow_cards'] + int(total.select('div.careerTab__stat--5')[0].text),
                'red_cards': stats['red_cards'] + int(total.select('div.careerTab__stat--6')[0].text),
            }

        stats['progress'] = round(stats['goals'] / 1000 * 100)
        stats['average_goals'] = round(stats['goals'] / stats['plays'], 2)

        return stats
    

    def get_player_stat(self, name='', id=''):

        url = self.__player_url(name, id)
        response = requests.get(url)
        stats = self.__parse_stats(response.text)

        return stats