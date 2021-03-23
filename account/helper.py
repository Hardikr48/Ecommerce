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
    print(month)

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


def count_occmsgrences(key, value, category, dict_list):
    counter = 0
    for d in dict_list:
        if key in d and 'category' in d:
            if d[key] == value and d['category'] == category:
                counter += 1
    return counter


def encode(string1):
    return base64.b64encode(string1)


def decode(string):
    return string.decode('base64')


def getPositiveResponse(msg, data={}):
    response = {}
    response['status'] = constants.SUCCESS
    response['message'] = msg
    response['result'] = data
    return response


def getNegativeResponse(msg, status_code=400, result={}):
    response = {}
    response['status'] = constants.FAIL
    response['message'] = msg
    response['result'] = result
    response['statusCode'] = status_code
    return response


def todayDate():
    return datetime.now()


def stringToDate(string):
    try:
        date = datetime.strptime(string, '%Y-%m-%d')
        return date
    except:
        return False


def stringDateTimeToDateTime(string, format):
    try:
        date = datetime.strptime(string, format)
        return date
    except:
        return False


def DateTimeToString(date):
    return date.strftime('%d-%m-%Y')


def datetimeToStringDateTime(date, format):
    return date.strftime(format)


def randomGeneratorCode(size=25, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def incrementDateTime(datetime_obj, value):
    return datetime_obj + timedelta(minutes=value)


def decrementDateTime(datetime_obj, value):
    return datetime_obj - timedelta(minutes=value)


def incrementDate(date_obj, value):
    return date_obj + timedelta(days=value)


def decrementDate(date_obj, value):
    return date_obj - timedelta(days=value)


def getErrorMessage(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = getErrorMessage(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = getErrorMessage(response_message)
        else:
            response = field + " : " + response[0]
    return response


def getFirstErrorMessage(error_dict):
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = getFirstErrorMessage(response)
    elif isinstance(response, list):
        response = response[0]
        if isinstance(response, dict):
            response = getFirstErrorMessage(response)
    return response


def getPKErrorMessage(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = getErrorMessage(response)
    elif isinstance(response, list):
        value = response[0].split('\"')[1]
        response = "Invalid value " + value + " for " + field + "."
    return response


def randomString():
    string = datetime.now()
    return string.strftime("%Y" "%m" "%d" "%H" "%M" "%S" "%m") + str(random.randint(1000, 9999))


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def getUTCDateTime():
    return pytz.utc.localize(datetime.utcnow()).replace(microsecond=0)


def phone_formate_converter(phone):
    if phone:
        phone = ''.join(x for x in str(phone) if x.isdigit())
        if len(phone) != 10:
            return False
        first_number = phone[0:3]
        second_number = phone[3:6]
        third_number = phone[6:10]
        phone = first_number+'-'+second_number+'-'+third_number
        return phone
    else:
        return ''


def convert_time_to_user_timezone(time, date, time_zone):
    user_timezone = pytz.timezone(time_zone)
    user_timezone = pytz.utc.localize(datetime(
        date.year, date.month, date.day, time.hour, time.minute, time.second)).astimezone(user_timezone)
    print(user_timezone)
    return user_timezone
