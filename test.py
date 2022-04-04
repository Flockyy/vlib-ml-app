import pandas as pd
import datetime

time = datetime.datetime.now().time()

time_range = pd.date_range("18:00", "06:30", freq="30min")

def time_in_range(now):
    sunrise = datetime.time(18,0,0)
    sunset = datetime.time(6,0,0)
    return sunset <= now <= sunrise

time_in_range(time)
# sunrise = datetime.time(8,0,0)
# print(time)