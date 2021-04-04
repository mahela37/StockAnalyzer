import calendar
import datetime

def timestamp_from_utc(datetime_object):
    return calendar.timegm(datetime_object.timetuple()) 

def today_opening_timestamp(opening_time_utc):
    now=datetime.datetime.utcnow()  
    today_opening=now.replace(hour=opening_time_utc['hour'],minute=opening_time_utc['minute'])
    return timestamp_from_utc(today_opening)    