from sqlalchemy import Table, select, delete, insert
from .base_table import BaseTable

        
        
class TypeChart(BaseTable):


    def __init__(self, engine, session) -> Table:
        # Pass table name and variables to the parent class
        super().__init__("TypeChart", engine, session)


    def get_data(self) -> dict:
            
        with self.session() as session:

            try:

                stmt = select(self.table.c.label, self.table.c.data)
                result = session.execute(stmt).fetchall()

                labels = [row.label for row in result]
                data_values = [row.data for row in result]
                
                return {
                    "labels": labels,
                    "data": data_values
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
                new_data = [
                    {"label": label, "data": data}
                    for label, data in zip(data["labels"], data["data"])
                ]

                # Insert new data
                if new_data:
                    session.execute(insert(self.table), new_data)
                
                # Commit transaction
                session.commit()

            except Exception as e:
                session.rollback()
                raise Exception(f'Database error {e}')