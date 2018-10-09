import time

# function to convert epoch time to custom format
def epochToFormat(epochtime = 0, format = "%Y-%m-%d %H:%M:%S"):
  epochtime = int(epochtime)
  return time.strftime(format, time.localtime(epochtime))