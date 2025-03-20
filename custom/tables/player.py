from sqlalchemy import Table, select, delete, insert
from .base_table import BaseTable

        
        
class Player(BaseTable):


    def __init__(self, engine, session) -> Table:
        # Pass table name and variables to the parent class
        super().__init__("Player", engine, session)


    def get_data(self) -> dict:
            
        with self.session() as session:

            try:

                stmt = select(self.table.c.goals, self.table.c.progress, self.table.c.seasons, self.table.c.goals_per_season, self.table.c.prediction)
                result = session.execute(stmt).fetchall()

                print('GOALS PER SEASON', result[0].goals_per_season)
                
                return {
                    "goals": result[0].goals,
                    "progress": result[0].progress,
                    "seasons": result[0].seasons,
                    "goals_per_season": result[0].goals_per_season,
                    "prediction": result[0].prediction
                }
            
            except Exception as e:
                raise Exception(f"Database error {e}")
                    

    def save_data(self, data: dict) -> None:

        with self.session() as session:
            
            try:
                # Begin a transaction
                session.begin()

                # Delete all existing data in the table
                session.execute(delete(self.table))

                # Prepare new data to insert
                new_data = [{
                    "goals": data["goals"],
                    "progress": data["progress"],
                    "seasons": data["seasons"],
                    "goals_per_season": data["goals_per_season"],
                    "prediction": data["prediction"]
                }]

                # Insert new data
                if new_data:
                    session.execute(insert(self.table), new_data)
                
                # Commit transaction
                session.commit()

            except Exception as e:
                session.rollback()
                raise Exception(f'Database error {e}')