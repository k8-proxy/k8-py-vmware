import datetime


class Utils:
    @staticmethod
    def format_expected_date(dt, dt_format):
        try:
            day, time = dt.split(",")
            d = datetime.date.today()
            while d.strftime("%A") != day.title():
                d += datetime.timedelta(1)

            d = datetime.datetime.strftime(d, "%Y-%m-%d")
            d = d + " " + time
            d = datetime.datetime.strptime(d, dt_format)
            d = datetime.datetime.strftime(d, dt_format)
        except:
            raise Exception("input date should have format eg. `Friday,10:30AM`")
        return d
