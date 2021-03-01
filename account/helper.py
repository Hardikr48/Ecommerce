import base64
import calendar
import datetime as dt
import random
import string
from datetime import datetime, timedelta

import pytz
from django.contrib.messages import constants



def increment_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def get_time_difference(clientDate):
    date = getTodayDate()
    return time_count((date - clientDate.date()).days)


def time_count(days):
    y = 365
    y2 = 31
    remainder = days % y
    day = remainder % y2
    year = (days - remainder) / y
    month = int((remainder - day) / y2)

    if(year != 0 and month != 0):
        return str(year) + " years & " + str(month) + " months"

    elif(year == 0 and month == 0 and day != 0):
        return str(day) + " days"

    elif(year == 0 and month != 0 and day != 0):
        return str(month) + " months & " + str(day) + " days"

    elif(year != 0 and month == 0 and day != 0):
        return str(year) + " years & " + str(day) + " days"

    elif(year != 0 and month != 0 and day != 0):
        return str(year) + " years & " + str(month) + " months & " + str(day) + " days"

    elif(year == 0 and month == 0 and day == 0):
        return str(day) + " days"

    elif(year == 0 and month != 0 and day == 0):
        return str(month) + " month"
    return ''


def getTodayDate():
    return dt.date.today()


def get_now():
    return datetime.now().time()
