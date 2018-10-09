import time

# function to convert epoch time to custom format
# "%Y-%m-%d %H:%M:%S"
def epochToFormat(epochtime = 0, formattime = "%Y-%m-%d %H:%M:%S"):
  epochtime = int(epochtime)
  return time.strftime(formattime, time.localtime(epochtime))