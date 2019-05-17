import os
from shutil import copyfile
from werkzeug.utils import secure_filename

# file controller from cloudinary
def handleUpload(directory, file, directory_db):
  ReturnFile = {}

  if(os.environ.get('FLASK_ENV') != 'production'):
    print('Upload file into', directory)
  # check is directory available
  if not os.path.exists(directory):
    # create new directory
    os.makedirs(directory)

  # rename file upload

  # upload original size file
  filename = secure_filename(file.filename)
  filetarget = directory + '/' + filename
  file.save(filetarget)

  ReturnFile['original'] = directory_db + '/' + filename
  ReturnFile['small'] = directory_db + '/' + filename
  ReturnFile["filename"] = filename

  # TODO: compress image
  # # ref: https://stackoverflow.com/a/15782516/2780875
  # if os.stat(filetarget).st_size  > 100000:
  #   # upload small size file 
  #   filename_arr = filename.split('.')
  #   smallfilename = filename.replace('.' + filename_arr[len(filename_arr) - 1], '_small.' + filename_arr[len(filename_arr) - 1])
  #   smallfiletarget = directory + '/' + smallfilename
  #   smallfile.save(smallfiletarget)
  #   ReturnFile['small'] = directory_db + '/' + smallfilename
  # else:
  #   ReturnFile['small'] = directory_db + '/' + filename

  # store to server
  print("uploading image...", ReturnFile)
  return ReturnFile