from datetime import datetime




def up_to_date(stats):

    # Checks if the collected stats are up to date (from the same day as today's date)

    if not stats:
        return False

    stats_date = datetime.strptime(stats['header']['date'], '%d-%m-%y')
    today = datetime.today()

    same_day = (
        stats_date.year == today.year and
        stats_date.month == today.month and
        stats_date.day == today.day
        )
    
    return same_day