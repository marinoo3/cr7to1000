from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from .tables import TimeChart, TypeChart, PositionChart, Player, Header, Goals

import os





class Database():

    def __init__(self) -> None:

        _engine = self.__create_engine()
        _session = sessionmaker(bind=_engine)

        # Init header table
        self.header = Header(engine=_engine, session=_session)

        # Init dashboard tables
        self.timechart = TimeChart(engine=_engine, session=_session)
        self.typechart = TypeChart(engine=_engine, session=_session)
        self.positionchart = PositionChart(engine=_engine, session=_session)
        self.player = Player(engine=_engine, session=_session)

        # Init goals table
        self.goals_list = Goals(engine=_engine, session=_session)



    def __create_engine(self):

        connection_string = URL.create(
            'postgresql',
            username = os.environ.get('CR7TO1000_DB_USERNAME'),
            password = os.environ.get('CR7TO1000_DB_PASSWORD'),
            host = 'ep-sparkling-feather-a24lwp3r.eu-central-1.pg.koyeb.app',
            database = 'cr7to1000-db'
        )

        engine = create_engine(connection_string, pool_recycle=150)

        return engine
    

    def get_last_update(self, stats='') -> datetime:

        if not stats:
            return None
        
        date = self.header.get_last_update(stats=stats)
        return datetime.strptime(date, '%Y-%m-%d')
    

    def save_stats(self, stats) -> None:

        # Save dashboard tables
        self.timechart.save_data(stats['timeChart'])
        self.typechart.save_data(stats['typeChart'])
        self.positionchart.save_data(stats['positionChart'])
        self.player.save_data(stats['player'])

        # Save goals table
        self.goals_list.save_data(stats['goals'])
        
        # Save header table
        self.header.update(stats='all_stats')
    

    def get_dashboard_stats(self) -> dict:

        stats = {
            'timeChart': self.timechart.get_data(),
            'typeChart': self.typechart.get_data(),
            'positionChart': self.positionchart.get_data(),
            'player': self.player.get_data(),
        }

        return stats
    

    def get_goals_stats(self, offset=0) -> dict:

        stats = {
            'goals': self.goals_list.get_data(offset=offset),
        }

        return stats
