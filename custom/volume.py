import json

class Volume():

    def __init__(self) -> None:
        self.stats_path = 'stats.json'

    def get_stats(self) -> dict:

        try:
            with open(self.stats_path, 'r') as file:
                stats = json.load(file)
        except FileNotFoundError:
            return None

        return stats
    
    def save_stats(self, stats) -> None:

        with open(self.stats_path, 'w') as file:
            json.dump(stats, file)