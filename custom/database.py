from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from .tables import TimeChart, TypeChart, PositionChart, Player, Header

import os





class Database():

    def __init__(self) -> None:

        _engine = self.__create_engine()
        _session = sessionmaker(bind=_engine)

        self.header = Header(engine=_engine, session=_session)

        self.timechart = TimeChart(engine=_engine, session=_session)
        self.typechart = TypeChart(engine=_engine, session=_session)
        self.positionchart = PositionChart(engine=_engine, session=_session)
        self.player = Player(engine=_engine, session=_session)


    def __create_engine(self):

        connection_string = URL.create(
            'postgresql',
            username = 'koyeb-adm', #os.environ.get('CR7TO1000_DB_USERNAME'),
            password = 'npg_wWPy2l0azDoT', #os.environ.get('CR7TO1000_DB_PASSWORD'),
            host = 'ep-sparkling-feather-a24lwp3r.eu-central-1.pg.koyeb.app',
            database = 'cr7to1000-db'
        )

        engine = create_engine(connection_string, pool_recycle=150)

        return engine
    

    def get_dashboard_stats(self) -> dict:

        stats = {
            'timeChart': self.timechart.get_data(),
            'typeChart': self.typechart.get_data(),
            'positionChart': self.positionchart.get_data(),
            'player': self.player.get_data(),
            'last_update': self.header.get_last_update(stats='dashboard')
        }

        return stats
    

    def save_dashboard_stats(self, stats) -> None:

        self.timechart.save_data(stats['timeChart'])
        self.typechart.save_data(stats['typeChart'])
        self.positionchart.save_data(stats['positionChart'])
        self.player.save_data(stats['player'])
        self.header.update(stats='dashboard')