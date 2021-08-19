import subprocess
import time
import schedule

def main():
    subprocess.run('git pull')

schedule.every().hour.do(main)
  