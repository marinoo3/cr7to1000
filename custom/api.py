from .scrapper import TransferMarkt, Wikipedia



class Api():

    def __init__(self) -> None:

        self.transfermarkt = TransferMarkt()
        self.wikipedia = Wikipedia()

    def get_data(self):

        # Scrap player data from transfermarkt
        transfermarkt_data = self.transfermarkt.get_player_data()
        # Scrap goals count from wikipedia
        wiki_data = self.wikipedia.get_goals_count()

        # Merge data
        data = {
            'goals_data': transfermarkt_data,
            'wiki_count': wiki_data
        }

        return data

