import requests
from bs4 import BeautifulSoup






class Wikipedia():


    def __init__(self) -> None:
        
        self.url = 'https://en.wikipedia.org/wiki/List_of_footballers_with_500_or_more_goals'


    def __parse_goals(self, html) -> int:

        soup = BeautifulSoup(html, 'html.parser')

        # Find table
        table = soup.select('table.wikitable')[0]
        table_content = table.select('tbody')[0]

        # Parse table content
        ronaldo_row = table_content.select('tr')[2]
        score_element = ronaldo_row.select('td')[6]
        
        # Get score as string
        score = score_element.select('b')[0].text

        return int(score)
    

    def get_goals_count(self) -> int:

        goals = None

        try:
            response = requests.get(self.url)
            goals = self.__parse_goals(response.text)
        except Exception as e:
            print(f'Error scrapping Wikipedia: {e}')

        return goals