from datetime import datetime




def up_to_date(date: datetime) -> bool:

    # Checks if the collected stats are up to date (from the same day as today's date)

    if not date:
        return False

    today = datetime.today()

    same_day = (
        date.year == today.year and
        date.month == today.month and
        date.day == today.day
    )
    
    return same_day