from sqlalchemy import Table, select, delete, insert, func
from datetime import datetime

from .base_table import BaseTable


class Goals(BaseTable):

    def __init__(self, engine, session) -> Table:
        # Pass table name and variables to the parent class
        super().__init__("Goals", engine, session)


    def get_data(self, limit=6, offset=0) -> None:

        with self.session() as session:

            try:

                # Subquery that groups by month_year and gets the latest date in each group
                subq = (
                    select(
                    self.table.c.month_year,
                    func.max(self.table.c.date).label("max_date")
                    )
                    .group_by(self.table.c.month_year)
                ).subquery()
                
                # Select from that subquery, ordering by "max_date"
                month_year_stmt = (
                    select(subq.c.month_year)
                    .order_by(subq.c.max_date.desc())
                    .limit(limit)
                    .offset(offset)
                )

                # Get a list of data from the 6 latest month_year (+ offset)
                month_years = session.execute(month_year_stmt).scalars().all()

                # Select all goals for the selected "month_year" values
                stmt = (
                    select(
                        self.table.c.date,
                        self.table.c.month_year,
                        self.table.c.competition,
                        self.table.c.position,
                        self.table.c.minute,
                        self.table.c.type,
                    )
                    .where(self.table.c.month_year.in_(month_years))
                    .order_by(self.table.c.date.desc())
                )

                result = session.execute(stmt).fetchall()
                
                grouped_data = {}
                for row in result:
                    if row.month_year not in grouped_data:
                        grouped_data[row.month_year] = {
                            'monthYear': row.month_year,
                            'goals': []
                        }
                    grouped_data[row.month_year]['goals'].append(
                        {
                            "date": datetime.strptime(row.date, '%Y-%m-%d %H:%M:%S').strftime('%a %d'),
                            "competition": row.competition,
                            "position": row.position,
                            "minute": row.minute,
                            "typeOfGoal": row.type
                        }
                    )

                goals_list = list(grouped_data.values())

                return goals_list

            except Exception as e:
                raise Exception(f"Database error {e}")
            

    def get_data__old(self, limimt=24, offset=0) -> list:

        with self.session() as session:

            try:

                stmt = (
                    select(
                        self.table.c.date,
                        self.table.c.month_year,
                        self.table.c.competition,
                        self.table.c.position,
                        self.table.c.minute,
                        self.table.c.type,
                    )
                    .order_by(self.table.c.date.desc())
                    .limit(limimt)
                    .offset(offset)
                )

                result = session.execute(stmt).fetchall()

                grouped_data = {}
                for row in result:
                    if row.month_year not in grouped_data:
                        grouped_data[row.month_year] = {
                            'monthYear': row.month_year,
                            'goals': []
                        }
                    grouped_data[row.month_year]['goals'].append(
                        {
                            "date": datetime.strptime(row.date, '%Y-%m-%d %H:%M:%S').strftime('%a %d'),
                            "competition": row.competition,
                            "position": row.position,
                            "minute": row.minute,
                            "typeOfGoal": row.type
                        }
                    )

                goals_list = list(grouped_data.values())

                return goals_list

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
                    {
                        "month_year": month_year,
                        "date": date,
                        "competition": competition,
                        "position": position,
                        "minute": minute,
                        "type_of_goal": type_of_goal,
                    }
                    for month_year, date, competition, position, minute, type_of_goal in zip(
                        data["month_year"],
                        data["date"],
                        data["competition"],
                        data["position"],
                        data["minute"],
                        data["type_of_goal"],
                    )
                ]

                # Insert new data
                if new_data:
                    session.execute(insert(self.table), new_data)

                # Commit transaction
                session.commit()

            except Exception as e:
                session.rollback()
                raise Exception(f'Database error {e}')
