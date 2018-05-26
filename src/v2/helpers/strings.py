import re

def generateTitleUrl(str = ''):
  # solved text trim from : https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
  str = re.sub(' +',' ',str)
  str = str.replace(' ', '-'),
  return str