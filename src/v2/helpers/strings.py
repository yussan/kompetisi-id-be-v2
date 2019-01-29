import re
import cgi

# function to generate link slug


def generateTitleUrl(title=''):
    # solved text trim from : https://stackoverflow.com/questions/1546226/simple-way-to-remove-multiple-spaces-in-a-string?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    title = re.sub(' +', ' ', title)
    title = title.replace(' ', '-'),
    return title


# function to remove all HTML tags
# ref: https://stackoverflow.com/a/19730306/2780875
def stripTags(str=''):
    tag_regx = re.compile(r'(<!--.*?-->|<[^>]*>)')
    strip_tags = tag_regx.sub('', str)
    return cgi.escape(strip_tags)
