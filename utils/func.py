from datetime import datetime
import time


def wait(n=1):
    print(f"waiting {n} seconds")
    time.sleep(n)


def get_timestamp():
    return datetime.now().strftime("%Y, %B %d, %H:%M")

