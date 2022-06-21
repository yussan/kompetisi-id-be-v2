# ref: https://docs.python.org/2/library/base64.html
import base64
import binascii

# function to encrypt number id to base64
# ref: https://stackoverflow.com/a/45482834/2780875
def encId(id):
  id = str(id).encode("utf-8")
  encoded = base64.b64encode(id)
  encoded = base64.b64encode(encoded)
  encoded = encoded.decode('utf-8').replace('=', '')

  return encoded

# function to decrypt base64 id to number id
def decId(encid):
  # ref: https://stackoverflow.com/a/9807138/2780875
  try:
    if(len(encid) >= 6):
      encid = encid.encode("utf-8")
      missing_padding = len(encid) % 4
      if missing_padding != 0:
        encid += b'=' * (4 - missing_padding)
      decoded = base64.decodestring(encid)
      decoded = base64.decodestring(decoded)
      # ref parse int: https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int-in-python
      return int(decoded)
    else: 
      return 0
  except binascii.Error:
    return 0