from datetime import datetime, time, timedelta

def generate_available_time_slots(open_time: time, close_time: time):
    """
    Generate 30-minute interval slots between open_time and close_time.
    Example: 10:00 → 10:30 → 11:00 ...
    """
    slots = []
    current_time = datetime.combine(datetime.today(), open_time)
    end_time = datetime.combine(datetime.today(), close_time)

    while current_time < end_time:
        slots.append(current_time.time())
        current_time += timedelta(minutes=30)

    return slots