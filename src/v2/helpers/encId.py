# ref: https://docs.python.org/2/library/base64.html
import base64

# function to encrypt number id to base64
def encId(id):
  id = str(id)
  encoded = base64.b64encode(id)
  encoded = base64.b64encode(encoded)
  encoded = encoded.replace('=', '')

  return encoded

# function to decrypt base64 id to number id
def decId(id):
  return 1