from sqlalchemy import MetaData, Table, engine
from sqlalchemy.orm import session

class BaseTable():

    def __init__(self, table_name, engine: engine.base.Engine, session: session.sessionmaker) -> None:
        
        self.engine = engine
        self.session = session
        self.metadata = MetaData()
        self.table = self.__get_table(table_name)
        

    def __get_table(self, table_name) -> Table:

        table = Table(table_name, self.metadata, autoload_with=self.engine)
        return table