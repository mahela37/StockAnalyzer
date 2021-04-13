import calendar
import datetime

'''Some helper functions to convert time'''

''' Given a UTC datetime object, return a UNIX timestamp equivalent '''
def timestamp_from_utc(datetime_object):
    return calendar.timegm(datetime_object.timetuple()) 

''' Given the opening time in UTC, return the UNIX timestamp for the current day opening time'''
def today_opening_timestamp(opening_time_utc):
    now=datetime.datetime.utcnow()
    today_opening=now.replace(hour=opening_time_utc['hour'],minute=opening_time_utc['minute'])
    return timestamp_from_utc(today_opening)
