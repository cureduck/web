import sched, time
from get_img import pixiv_download
s = sched.scheduler(time.time, time.sleep)

time.sleep(500*60)
while True:
    print(time.time())
    s.enter(24*60*60,1,pixiv_download)
    s.run()


