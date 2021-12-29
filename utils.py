from datetime import datetime

def posix2DateTime(timeTicks):
    return datetime.utcfromtimestamp(timeTicks).strftime('%Y-%m-%dT%H:%M:%SZ')