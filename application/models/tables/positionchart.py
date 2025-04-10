from sqlalchemy import Table, select, delete, insert
from .base_table import BaseTable

        
        
class PositionChart(BaseTable):


    def __init__(self, engine, session) -> Table:
        # Pass table name and variables to the parent class
        super().__init__("PositionChart", engine, session)


    def get_data(self) -> dict:
            
        with self.session() as session:

            try:

                stmt = select(self.table.c.position, self.table.c.count, self.table.c.percent)
                result = session.execute(stmt).fetchall()

                data = {}
                for row in result:
                    data[row.position] = {
                        "count": row.count,
                        "percent": row.percent
                    }
                
                return data
            
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
                new_data = [
                    {"position": key, "count": value["count"], "percent": value["percent"]} 
                    for key, value in data.items()
                ]

                # Insert new data
                if new_data:
                    session.execute(insert(self.table), new_data)
                
                # Commit transaction
                session.commit()

            except Exception as e:
                session.rollback()
                raise Exception(f'Database error {e}')