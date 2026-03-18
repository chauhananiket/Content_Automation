from datetime import datetime, timedelta
from utils.datetime_utils import ist_to_utc

def generate_schedule(videos, per_day, upload_time, start_date, end_date=None):

    schedule = []

    current_date = datetime.combine(start_date, datetime.min.time())

    i = 0

    while i < len(videos):

        for _ in range(per_day):

            if i >= len(videos):
                break

            publish_ist = datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                upload_time.hour,
                upload_time.minute
            )

            # stop if beyond end date
            if end_date and publish_ist.date() > end_date:
                return schedule

            publish_utc = ist_to_utc(publish_ist)

            schedule.append((videos[i], publish_utc))

            i += 1

        current_date += timedelta(days=1)

    return schedule