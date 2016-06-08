from time import localtime, strftime

# localtime 은 유닉스 타임스탬프를 호스트 컴퓨터의 시간대로 변경한다
now = 1407694710
local_tuple = localtime(now)
time_format = '%Y-%m-%d %H:%M:%S'
time_str = strftime(time_format, local_tuple)
print(time_str)

# 반대로 하는 경우엔..
from time import mktime, strptime

time_tuple = strptime(time_str, time_format)
utc_now = mktime(time_tuple)
print(utc_now)


# time 모듈은 여러 지역 시간에 대해 일관된 동작을 보장하지 못한다. datetime 을 사용하자
from datetime import datetime, timezone

now = datetime(2014, 8, 10, 18, 18, 30)
now_utc = now.replace(tzinfo=timezone.utc)
now_local = now_utc.astimezone()
print(now_local)


time_str = '2014-08-10 11:18:30'
now = datetime.strptime(time_str, time_format)
time_tuple = now.timetuple()
utc_now = mktime(time_tuple)
print(utc_now)

# 단점은 tzinfo 클래스와 관련 메스드를 이용한 시간대 변환 기능만 제공한다는 것이다.
# 파이썬 패키지의 pytz 모듈을 사용해보자
# pytz 의 효과적인 사용을 위해서는 지역시간을 utc 로 먼저 변경해야 한다. 그 뒤에 utc 값에 필요한 datetime 연산을 수행하고 필요한 지역시간으로 변환한다

import pytz

print('using pytz...')
arrival_nyc = '2014-05-01 23:33:24'
nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
eastern = pytz.timezone('US/Eastern')
nyc_dt = eastern.localize(nyc_dt_naive)
utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
print(utc_dt) # utc time 을 얻는다


pacific = pytz.timezone('US/Pacific')
sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
print(sf_dt) # 필요한 시간대로 변경


nepal = pytz.timezone('Asia/Katmandu')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(nepal_dt)


nepal = pytz.timezone('Asia/Seoul')
nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
print(nepal_dt)


