import datetime


def sprint_dates(workspace):
    if workspace == '<someid>':
        return {
            1: {"start": datetime.date(2016, 10, 3), "end": datetime.date(2016, 10, 6)},
            2: {"start": datetime.date(2016, 10, 7), "end": datetime.date(2016, 10, 13)},
            3: {"start": datetime.date(2016, 10, 14), "end": datetime.date(2016, 10, 20)},
            4: {"start": datetime.date(2016, 10, 21), "end": datetime.date(2016, 10, 26)},
            5: {"start": datetime.date(2016, 10, 27), "end": datetime.date(2016, 11, 3)},
            6: {"start": datetime.date(2016, 11, 4), "end": datetime.date(2016, 11, 10)},
            7: {"start": datetime.date(2016, 11, 11), "end": datetime.date(2016, 11, 17)},
            8: {"start": datetime.date(2016, 11, 18), "end": datetime.date(2016, 11, 24)},
            9: {"start": datetime.date(2016, 11, 25), "end": datetime.date(2016, 12, 1)},
            10: {"start": datetime.date(2016, 12, 2), "end": datetime.date(2016, 12, 9)}
        }
    elif workspace == '<some other id>':
        return {
            1 : {"start": datetime.date(2015, 10, 3), "end": datetime.date(2015, 10, 6)},
            2 : {"start": datetime.date(2015, 10, 7), "end": datetime.date(2015, 10, 13)},
            3 : {"start": datetime.date(2015, 10, 14), "end": datetime.date(2015, 10, 20)},
            4 : {"start": datetime.date(2015, 10, 21), "end": datetime.date(2015, 10, 26)},
            5 : {"start": datetime.date(2015, 10, 27), "end": datetime.date(2015, 11, 3)},
            6 : {"start": datetime.date(2015, 11, 4), "end": datetime.date(2015, 11, 10)},
        }
    else:
        return {0: {"start": datetime.date(2000, 1, 1), "end": datetime.date(2019, 12, 31)}}
