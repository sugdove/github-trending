import subprocess
import time
from datetime import datetime
while True:
    # Run every hour
    now = datetime.now()
    if now.minute == 0:
        # Commit every 3h
        # if now.hour % 3 == 0:
        if True:
            try:
                subprocess.run('git pull')
            except:
                pass
        time.sleep(60 * 50)
    else:
        time.sleep(1)
  