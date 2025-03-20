from datetime import datetime




def up_to_date(date):

    # Checks if the collected stats are up to date (from the same day as today's date)

    if not date:
        return False

    stats_date = datetime.strptime(date, '%Y-%m-%d')
    today = datetime.today()

    print(stats_date.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))

    same_day = (
        stats_date.year == today.year and
        stats_date.month == today.month and
        stats_date.day == today.day
        )
    
    return same_day