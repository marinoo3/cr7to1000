from sqlalchemy import Table, select, delete, insert
from .base_table import BaseTable
from datetime import datetime

        
        
class Header(BaseTable):

    #TODO: Create a row for dashboard stats (table already created)
    # Also write a methode to update the last_update column in the table for a specific stats


    def __init__(self, engine, session) -> Table:
        # Pass table name and variables to the parent class
        super().__init__("Header", engine, session)


    def get_last_update(self, stats='') -> str:

        if not stats:
            return None

        with self.session() as session:

            try:

                stmt = select(self.table.c.last_update).where(self.table.c.stats == stats)
                result = session.execute(stmt).fetchall()

                last_update = result[0].last_update
                
                return last_update
            
            except Exception as e:
                raise Exception(f"Database error {e}")
            

    def update(self, stats='') -> None:

        if not stats:
            return
        
        with self.session() as session:
            
            try:
                # Begin a transaction
                session.begin()

                # Delete all existing data in the table
                session.execute(delete(self.table))

                # Prepare new data to insert
                today = datetime.today()
                new_data = [
                    {'stats': 'dashboard', 'last_update': today.strftime('%Y-%m-%d')}
                ]

                # Insert new data
                if new_data:
                    session.execute(insert(self.table), new_data)
                
                # Commit transaction
                session.commit()

            except Exception as e:
                session.rollback()
                raise Exception(f'Database error {e}')