import json
import os
from v2.config.hosts import hosts
import re

def transform(n):
    return {
        'id': n.id_req,
        'title': n.nama,
        'email': n.email,
        'link': n.link,
        'poster': transformImage(n.poster),
        'status': n.status,
        'created_at': n.created_at.strftime('%s'),
        'updated_at': n.updated_at.strftime('%s'),
        'accepted_at': n.accepted_at.strftime('%s') if n.accepted_at else 0,
        'note': n.note
    }


def transformImage(image):

    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

    if not image:
        return {
            'small': 'https://kompetisi.id/assets/images/news-default-image.png',
            'original': 'https://kompetisi.id/assets/images/news-default-image.png'
        }
    else:
        try:
            image = json.loads(image)
            return {
                'small': image['small'] if image['small'].find('http') > -1 else hosts[FLASK_ENV]['media'] + image['small'],
                'original': image['original'] if re.match(r'^http', image['original']) else hosts[FLASK_ENV]['media'] + image['original']
            }
        except ValueError:
            return {
                'small': 'https://kompetisi.id/assets/images/news-default-image.png',
                'original': 'https://kompetisi.id/assets/images/news-default-image.png'
            }
