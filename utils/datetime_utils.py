from datetime import datetime, timedelta, timezone

def utc_to_ist(utc_time_str):

    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")

    ist_time = utc_time.replace(tzinfo=timezone.utc) + timedelta(hours=5, minutes=30)

    return ist_time.strftime("%Y-%m-%d %I:%M %p IST")


def ist_to_utc(ist_datetime):

    utc_time = ist_datetime - timedelta(hours=5, minutes=30)

    return utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")