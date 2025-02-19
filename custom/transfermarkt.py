import requests
from bs4 import BeautifulSoup






class TransferMarkt():


    def __init__(self) -> None:
        
        self.url = 'https://www.transfermarkt.com/cristiano-ronaldo/alletore/spieler/8198/plus/1'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            }


    def __parse_row(self, content, last_content):

        data = {
            'date': '',
            'venue': '',
            'result': '',
            'position': '',
            'type_of_goal': '',
            'goal_assist': ''
        }

        cursor = 0
        for col in content:

            match cursor:
                case 3:
                    data['date'] = col.text
                case 4:
                    data['venue'] = col.text
                case 9:
                    data['result'] = col.text
                case 10:
                    data['position'] = col.text
                case 13:
                    data['type_of_goal'] = col.text
                case 14:
                    data['goal_assist'] = col.text

            cursor += 1
            colspan = col.get('colspan')
            if colspan:
                cursor += int(colspan) - 1

        if not any(data.values()):
            # if data is empty returns None (it's a header row)
            return None
        
        for key, value in data.items():
            if not value and last_content:
                data[key] = last_content[key]

        return data


    def __parse_data(self, html):

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.select('div.row .responsive-table tbody')[0]
        rows = table.select('tr')

        stats = []

        for row in rows:

            content = row.select('td')
            last_data = stats[-1] if stats else None

            row_stats = self.__parse_row(content, last_data)
            if row_stats:
                stats.append(row_stats)

        return stats
    

    def get_player_stat(self):

        response = requests.get(self.url, headers=self.headers)
        data = self.__parse_data(response.text)

        return data
    










"""
        COLUMN FORMAT (18-02-2025)

        'league_logo': 0,
        'league_name': 1,
        'matchday': 2,
        'date': 3,
        'venue': 4,
        'team_logo': 5,
        'team_name': 6,
        'opponent_logo': 7,
        'opponent_name': 8,
        'result': 9,
        'position': 10,
        'minute': 11,
        'at_score': 12,
        'type_of_goal': 13,
        'goal_assist': 14
"""