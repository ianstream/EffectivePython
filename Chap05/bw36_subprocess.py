# subprocess 로 자식 프로세스 실행

import subprocess

proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout=subprocess.PIPE)

out, err = proc.communicate()
print(out.decode('utf-8'))


# 자식 프로세스의 상태는 주기적으로 폴링

from time import sleep, time

proc = subprocess.Popen(['echo', 'sleep', '0.3'])
while proc.poll() is None:
    print('Working...')
    # Some time consuming work here
    sleep(0.2)

print('Exit status', proc.poll())




def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc

print('\nfor loop with subprocess time check')
start = time()
procs = []
for _ in range(10):
    proc = run_sleep(0.2)
    procs.append(proc)

for index, proc in enumerate(procs, start=1):
    out, err = proc.communicate()
    print(index, out, err)
end = time()
print('Finished in %.3f seconds' % (end - start))

# 부모 프로세스가 자식 프로세스를 병렬로 실행한다. 그 결과 전체 수행시간은 0.2 * 10 보다 짧다
# 파이프를 이용해 데이터를 서브 프로세스로 보내고 그 결과를 받아오는 것도 가능하다
import os

def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    proc.stdin.write(data)
    proc.stdin.flush() # 자식 프로세스가 입력을 반드시 받게 함
    return proc


print('\ntest subprocess pipe')

procs = []
for _ in range(3):
    data = os.urandom(10)
    print('data: ', data)
    proc = run_openssl(data)
    procs.append(proc)


for proc in procs:
    out, err = proc.communicate()
    print(out[:])



print('\ntest subprocess timeout')

proc = run_sleep(10)
try:
    proc.communicate(timeout=0.5)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()

print('Exit status', proc.poll())




