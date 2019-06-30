from v2.helpers.strings import generateTitleUrl
from v2.helpers.encId import encId
import json
import re
import os


def transform(n):
    return {
        'id': encId(n.id),
        'author': {
            'id': n.id_user,
            'username': n.username,
            'moto': n.moto
        },
        'title': n.title.replace('&', ''),
        'nospace_title':  (generateTitleUrl(n.title)[0]).replace('&', ''),
        'content': n.content,
        'image': transformImage(n.image),
        'is_draft': n.draft == '1',
        'created_at': n.created_at.strftime('%s'),
        'updated_at': n.updated_at.strftime('%s'),
        'tag': n.tag
    }


def transformImage(image):
    if not image:
        return {
            'small': 'https://kompetisi.id/assets/images/news-default-image.png',
            'original': 'https://kompetisi.id/assets/images/news-default-image.png'
        }
    else:
        image = json.loads(image)
        return {
            'small': image['small'] if image['small'].find('http') > -1 else os.environ.get('MEDIA_HOST', 'https://media.kompetisi.id') + image['small'],
            'original': image['original'] if re.match(r'^http', image['original']) else os.environ.get('MEDIA_HOST', 'https://media.kompetisi.id') + image['original']
        }
