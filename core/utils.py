from datetime import datetime, timedelta

def generate_available_time_slots(open_time, close_time):
    """
    Generates time slots at 30-minute intervals
    starting 30 min after open until 30 min before close.
    """
    slots = []
    start_dt = datetime.combine(datetime.today(), open_time) + timedelta(minutes=30)
    end_dt = datetime.combine(datetime.today(), close_time) - timedelta(minutes=30)

    while start_dt <= end_dt:
        slots.append(start_dt.time())
        start_dt += timedelta(minutes=30)

    return slots