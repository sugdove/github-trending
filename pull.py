import subprocess
import time

while True:
    # Run every hour
    now = datetime.now()
    if now.minute == 0:
        try:
            subprocess.run('git pull')
        except:
            pass
    time.sleep(60 * 50)
    else:
        time.sleep(1)
  