# 호출하는 쪽의 변경 없이 기존 클래스를 사용한 곳에 새로운 동작을 하게 해주는 property 의 사용법을 알아보자

# 양동이에 남은 할당량과 이용할 수 있는 시간을 표현
from datetime import datetime, timedelta


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

bucket = Bucket(60)
print(bucket)


# 양동이를 채울 때 할당량이 다음 기간으로 넘어가지 않게 하는 식으로 동작
def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

# 양동이에서 할당량을 소비할 땐 가용량부터 체크한다
def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


# test
print('test')
bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

# 사용
if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)


# 이제 1이 사용 가능한 용량인데 3을 빼려고 하면..
if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)


# 양동이의 할당량을 알기위해 몇가지 추가해주자

class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0 # 기간동안 발생한 양
        self.quota_consumed = 0 # 소비된 양

    def __repr__(self):
        return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                (self.max_quota, self.quota_consumed))

    # 현재 할당량을 계산
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    # quota 속성이 할당을 받는 순간에 fill, deduct 에서 사용하는 이 클래스의 현재 인터페이스와 일치하는 특별한 동작을 하게 만든다
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

# 같은 코드를 다시 실행
print('같은 코드를 다시 실행')
bucket = Bucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')

print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')

print('Still', bucket)


