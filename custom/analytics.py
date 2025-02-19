import pandas as pd
from datetime import datetime, timedelta
import calendar


class Analytics():

    def __init__(self) -> None:
        self.friendly_goals = 141

    def __predict_data(self, df, goals_count):

        prediction_df = df
        prediction_df['date'] = pd.to_datetime(prediction_df['date'])
        # Create a Year column
        prediction_df['year'] = prediction_df['date'].dt.year
        # Create a Month column
        prediction_df['month'] = prediction_df['date'].dt.month

        # Only keep last 6 years of data
        _years_limit = int(datetime.now().strftime('%Y')) - 6
        prediction_df = prediction_df[prediction_df['year'] >= _years_limit]
        # Exclude 2022 because covid-19 and current year
        prediction_df = prediction_df[prediction_df['year'] != 2022]
        prediction_df = prediction_df[prediction_df['year'] != datetime.now().year]

        # Compute the average goals scored for each month
        _years_count = prediction_df['year'].nunique() # the number of years keeped in the dataframe
        grouped_df = prediction_df.groupby('month').size().reset_index(name='goals')
        grouped_df['avg'] = grouped_df['goals'] / _years_count

        # Predict the amount of goals that will be scored tomorrow, 
        # add it to the count and continue for the next day until the count reachs 1000
        count = goals_count
        date = datetime.now()
        while count < 1000:

            date = date + timedelta(days=1)

            days_count = calendar.monthrange(date.year, date.month)[1]
            month_avg = grouped_df['avg'][grouped_df['month'] == date.month].values[0]
            goals_per_day = month_avg / days_count

            count += goals_per_day

        return date.strftime('%d %b %Y')


    

    def format_stats(self, data):

        stats = {}
        df = pd.DataFrame(data)

        # Create Time Chart data dict
        time_chart = df
        time_chart['date'] = pd.to_datetime(time_chart['date'])
        time_chart['year'] = time_chart['date'].dt.year
        time_chart = time_chart.groupby('year').size().reset_index(name='count')
        # Add data dict to general stats dict
        stats['timeChart'] = {
            'labels': time_chart['year'].tolist(),
            'data': time_chart['count'].tolist()
        }

        # Create Goals Type Chart data dict
        goals_type_chart = df
        goals_type_chart = goals_type_chart.groupby('type_of_goal').size().reset_index(name='count')
        goals_type_chart = goals_type_chart[goals_type_chart['type_of_goal'] != 'Not reported']
        goals_type_chart = goals_type_chart.sort_values(by='count', ascending=False)
        # Add data dict to general stats dict
        stats['goalsTypeChart'] = {
            'labels': goals_type_chart['type_of_goal'].to_list(),
            'data': goals_type_chart['count'].to_list()
        }

        # Create Position Chart data dict
        position_chart = df
        position_chart['position'] = position_chart['position'].str.strip()
        position_chart = position_chart.groupby('position').size().reset_index(name='count')
        _total = position_chart['count'].sum()
        position_chart['percent'] = position_chart['count'] / _total
        # Add data dict to general stats dict
        stats['positionChart'] = position_chart.set_index('position').T.to_dict(orient='dict')
        print(stats['positionChart'])
        #stats['positionChart'] = position_chart.set_index('position')['percent'].to_dict()

        # Create general player stats
        _total_goals = len(df) + self.friendly_goals # add 141 non-reported friendly goals
        player_stats = {
            'goals': _total_goals, 
            'progress': round(_total_goals / 1000 * 100),
            'seasons': len(time_chart['year']),
            'goals_per_saison': round(_total_goals / len(time_chart['year']), 2),
            'prediction': self.__predict_data(df, _total_goals)
        }
        # Add player stats to general data stats dict
        stats['player'] = player_stats

        # Create Header for stats
        stats['header'] = {
            'date': datetime.strftime(datetime.today(), '%d-%m-%y')
        }

        return stats