import requests

class API():

    def __init__(self) -> None:
        
        self.api_key = 'a0f379213911f1205006ab1515f5d9fd'
        self.url = 'https://v3.football.api-sports.io/players'

    def get_player_stat(self, name='ronaldo'):

        response = requests.get(self.url, params={'action': 'get_players', 'player_name': name, 'APIkey': self.api_key})
        stats = response.json()

        print(stats)

        return stats[0]