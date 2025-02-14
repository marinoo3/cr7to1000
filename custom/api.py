import requests

class API():

    def __init__(self) -> None:
        
        self.api_key = '1e4be630a224bb69075791002584bb8fc58ce2d1af389db19e30b2e3fb206f1e'
        self.url = 'https://apiv3.apifootball.com'

    def get_player_stat(self, name='ronaldo'):

        response = requests.get(self.url, params={'action': 'get_players', 'player_name': name, 'APIkey': self.api_key})
        stats = response.json()

        print(stats)

        return stats[0]