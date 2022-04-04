from datetime import tzinfo, timedelta, datetime

ZERO = timedelta(0)
HOUR = timedelta(hours=1)
SECOND = timedelta(seconds=1)

# A class capturing the platform's idea of local time.
# (May result in wrong values on historical times in
#  timezones where UTC offset and/or the DST rules had
#  changed in the past.)
import time as _time

STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):

    def fromutc(self, dt):
        assert dt.tzinfo is self
        stamp = (dt - datetime(1970, 1, 1, tzinfo=self)) // SECOND
        args = _time.localtime(stamp)[:6]
        dst_diff = DSTDIFF // SECOND
        # Detect fold
        fold = (args == _time.localtime(stamp - dst_diff))
        return datetime(*args, microsecond=dt.microsecond,
                        tzinfo=self, fold=fold)

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0

Local = LocalTimezone()


# A complete implementation of current DST rules for major US time zones.

def first_sunday_on_or_after(dt):
    days_to_go = 6 - dt.weekday()
    if days_to_go:
        dt += timedelta(days_to_go)
    return dt


# US DST Rules
#
# This is a simplified (i.e., wrong for a few cases) set of rules for US
# DST start and end times. For a complete and up-to-date set of DST rules
# and timezone definitions, visit the Olson Database (or try pytz):
# http://www.twinsun.com/tz/tz-link.htm
# http://sourceforge.net/projects/pytz/ (might not be up-to-date)
#
# In the US, since 2007, DST starts at 2am (standard time) on the second
# Sunday in March, which is the first Sunday on or after Mar 8.
DSTSTART_2007 = datetime(1, 3, 8, 2)
# and ends at 2am (DST time) on the first Sunday of Nov.
DSTEND_2007 = datetime(1, 11, 1, 2)
# From 1987 to 2006, DST used to start at 2am (standard time) on the first
# Sunday in April and to end at 2am (DST time) on the last
# Sunday of October, which is the first Sunday on or after Oct 25.
DSTSTART_1987_2006 = datetime(1, 4, 1, 2)
DSTEND_1987_2006 = datetime(1, 10, 25, 2)
# From 1967 to 1986, DST used to start at 2am (standard time) on the last
# Sunday in April (the one on or after April 24) and to end at 2am (DST time)
# on the last Sunday of October, which is the first Sunday
# on or after Oct 25.
DSTSTART_1967_1986 = datetime(1, 4, 24, 2)
DSTEND_1967_1986 = DSTEND_1987_2006

def us_dst_range(year):
    # Find start and end times for US DST. For years before 1967, return
    # start = end for no DST.
    if 2006 < year:
        dststart, dstend = DSTSTART_2007, DSTEND_2007
    elif 1986 < year < 2007:
        dststart, dstend = DSTSTART_1987_2006, DSTEND_1987_2006
    elif 1966 < year < 1987:
        dststart, dstend = DSTSTART_1967_1986, DSTEND_1967_1986
    else:
        return (datetime(year, 1, 1), ) * 2

    start = first_sunday_on_or_after(dststart.replace(year=year))
    end = first_sunday_on_or_after(dstend.replace(year=year))
    return start, end


class USTimeZone(tzinfo):

    def __init__(self, hours, reprname, stdname, dstname):
        self.stdoffset = timedelta(hours=hours)
        self.reprname = reprname
        self.stdname = stdname
        self.dstname = dstname

    def __repr__(self):
        return self.reprname

    def tzname(self, dt):
        if self.dst(dt):
            return self.dstname
        else:
            return self.stdname

    def utcoffset(self, dt):
        return self.stdoffset + self.dst(dt)

    def dst(self, dt):
        if dt is None or dt.tzinfo is None:
            # An exception may be sensible here, in one or both cases.
            # It depends on how you want to treat them.  The default
            # fromutc() implementation (called by the default astimezone()
            # implementation) passes a datetime with dt.tzinfo is self.
            return ZERO
        assert dt.tzinfo is self
        start, end = us_dst_range(dt.year)
        # Can't compare naive to aware objects, so strip the timezone from
        # dt first.
        dt = dt.replace(tzinfo=None)
        if start + HOUR <= dt < end - HOUR:
            # DST is in effect.
            return HOUR
        if end - HOUR <= dt < end:
            # Fold (an ambiguous hour): use dt.fold to disambiguate.
            return ZERO if dt.fold else HOUR
        if start <= dt < start + HOUR:
            # Gap (a non-existent hour): reverse the fold rule.
            return HOUR if dt.fold else ZERO
        # DST is off.
        return ZERO

    def fromutc(self, dt):
        assert dt.tzinfo is self
        start, end = us_dst_range(dt.year)
        start = start.replace(tzinfo=self)
        end = end.replace(tzinfo=self)
        std_time = dt + self.stdoffset
        dst_time = std_time + HOUR
        if end <= dst_time < end + HOUR:
            # Repeated hour
            return std_time.replace(fold=1)
        if std_time < start or dst_time >= end:
            # Standard time
            return std_time
        if start <= std_time < end - HOUR:
            # Daylight saving time
            return dst_time


Eastern  = USTimeZone(-5, "Eastern",  "EST", "EDT")
Central  = USTimeZone(-6, "Central",  "CST", "CDT")
Mountain = USTimeZone(-7, "Mountain", "MST", "MDT")
Pacific  = USTimeZone(-8, "Pacific",  "PST", "PDT")


from math import cos,sin,acos,asin,tan  
from math import degrees as deg, radians as rad  
from datetime import date,datetime,time  
  
class sun:  
 """  
 Calculate sunrise and sunset based on equations from NOAA 
 http://www.srrb.noaa.gov/highlights/sunrise/calcdetails.html 
 
 typical use, calculating the sunrise at the present day: 
  
 import datetime 
 import sunrise 
 s = sun(lat=49,long=3) 
 print('sunrise at ',s.sunrise(when=datetime.datetime.now()) 
 """  
 def __init__(self,lat=52.37,long=4.90): # default Amsterdam  
  self.lat=lat  
  self.long=long  
    
 def sunrise(self,when=None):  
  """ 
  return the time of sunrise as a datetime.time object 
  when is a datetime.datetime object. If none is given 
  a local time zone is assumed (including daylight saving 
  if present) 
  """  
  if when is None : when = datetime.now(tz=LocalTimezone())  
  self.__preptime(when)  
  self.__calc()  
  return sun.__timefromdecimalday(self.sunrise_t)  
    
 def sunset(self,when=None):  
  if when is None : when = datetime.now(tz=LocalTimezone())  
  self.__preptime(when)  
  self.__calc()  
  return sun.__timefromdecimalday(self.sunset_t)  
    
 def solarnoon(self,when=None):  
  if when is None : when = datetime.now(tz=LocalTimezone())  
  self.__preptime(when)  
  self.__calc()  
  return sun.__timefromdecimalday(self.solarnoon_t)  
   
 @staticmethod  
 def __timefromdecimalday(day):  
  """ 
  returns a datetime.time object. 
   
  day is a decimal day between 0.0 and 1.0, e.g. noon = 0.5 
  """  
  hours  = 24.0*day  
  h      = int(hours)  
  minutes= (hours-h)*60  
  m      = int(minutes)  
  seconds= (minutes-m)*60  
  s      = int(seconds)  
  return time(hour=h,minute=m,second=s)  
  
 def __preptime(self,when):  
  """ 
  Extract information in a suitable format from when,  
  a datetime.datetime object. 
  """  
  # datetime days are numbered in the Gregorian calendar  
  # while the calculations from NOAA are distibuted as  
  # OpenOffice spreadsheets with days numbered from  
  # 1/1/1900. The difference are those numbers taken for   
  # 18/12/2010  
  self.day = when.toordinal()-(734124-40529)  
  t=when.time()  
  self.time= (t.hour + t.minute/60.0 + t.second/3600.0)/24.0  
    
  self.timezone=0  
  offset=when.utcoffset()  
  if not offset is None:  
   self.timezone=offset.seconds/3600.0  
    
 def __calc(self):  
  """ 
  Perform the actual calculations for sunrise, sunset and 
  a number of related quantities. 
   
  The results are stored in the instance variables 
  sunrise_t, sunset_t and solarnoon_t 
  """  
  timezone = self.timezone # in hours, east is positive  
  longitude= self.long     # in decimal degrees, east is positive  
  latitude = self.lat      # in decimal degrees, north is positive  
  
  time  = self.time # percentage past midnight, i.e. noon  is 0.5  
  day      = self.day     # daynumber 1=1/1/1900  
   
  Jday     =day+2415018.5+time-timezone/24 # Julian day  
  Jcent    =(Jday-2451545)/36525    # Julian century  
  
  Manom    = 357.52911+Jcent*(35999.05029-0.0001537*Jcent)  
  Mlong    = 280.46646+Jcent*(36000.76983+Jcent*0.0003032)%360  
  Eccent   = 0.016708634-Jcent*(0.000042037+0.0001537*Jcent)  
  Mobliq   = 23+(26+((21.448-Jcent*(46.815+Jcent*(0.00059-Jcent*0.001813))))/60)/60  
  obliq    = Mobliq+0.00256*cos(rad(125.04-1934.136*Jcent))  
  vary     = tan(rad(obliq/2))*tan(rad(obliq/2))  
  Seqcent  = sin(rad(Manom))*(1.914602-Jcent*(0.004817+0.000014*Jcent))+sin(rad(2*Manom))*(0.019993-0.000101*Jcent)+sin(rad(3*Manom))*0.000289  
  Struelong= Mlong+Seqcent  
  Sapplong = Struelong-0.00569-0.00478*sin(rad(125.04-1934.136*Jcent))  
  declination = deg(asin(sin(rad(obliq))*sin(rad(Sapplong))))  
    
  eqtime   = 4*deg(vary*sin(2*rad(Mlong))-2*Eccent*sin(rad(Manom))+4*Eccent*vary*sin(rad(Manom))*cos(2*rad(Mlong))-0.5*vary*vary*sin(4*rad(Mlong))-1.25*Eccent*Eccent*sin(2*rad(Manom)))  
  
  hourangle= deg(acos(cos(rad(90.833))/(cos(rad(latitude))*cos(rad(declination)))-tan(rad(latitude))*tan(rad(declination))))  
  
  self.solarnoon_t=(720-4*longitude-eqtime+timezone*60)/1440  
  self.sunrise_t  =self.solarnoon_t-hourangle*4/1440  
  self.sunset_t   =self.solarnoon_t+hourangle*4/1440  
  
if __name__ == "__main__":  
 s=sun(lat=52.37,long=4.90)  
 print(datetime.today())  
 print(s.sunrise(),s.solarnoon(),s.sunset())