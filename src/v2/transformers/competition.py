from v2.helpers.encId import encId
from v2.helpers.strings import generateTitleUrl
# ref: http://docs.python-guide.org/en/latest/scenarios/json/
import json
import re
import os


def transform(n):
    return {
        # 'id': n.id_kompetisi,
        'id': encId(n.id_kompetisi),
        'title': n.judul_kompetisi.replace('&', ''),
        'nospace_title':  (generateTitleUrl(n.judul_kompetisi)[0]).replace('&', ''),
        'sort': n.sort,
        'organizer': n.penyelenggara,
        'deadline_at': n.deadline.strftime('%s') if n.deadline != '0000-00-00' else 0,
        'announcement_at': n.pengumuman.strftime('%s') if n.pengumuman != '0000-00-00' else 0,
        'created_at': n.created_at.strftime('%s'),
        'updated_at': n.updated_at.strftime('%s'),
        'is_mediapartner': n.mediapartner == 1,
        'is_garansi': n.garansi == "1",
        'content': n.konten,
        'prize': {
            'total': n.total_hadiah,
            'description': n.hadiah
        },
        'poster': transformImage(n.poster),
        'main_category': {
            'id': n.id_main_kat,
            'name': n.main_kat,
        },
        'sub_category': {
            'id': n.id_sub_kat,
            'name': n.sub_kat
        },
        'author': {
            'id': n.id_user,
            'username': n.username,
            'name': n.fullname,
            'moto': n.moto,
            'level': n.level
        },
        # ref teranary condition: https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
        'announcement': json.loads(n.dataPengumuman) if n.dataPengumuman else [],
        'contacts': json.loads(n.kontak) if n.kontak else [],
        'tag': n.tag,
        'link_source': n.sumber,
        'link_join': n.ikuti,
        'views': n.views,
        "status": n.status
    }


def transformImage(image):
    if not image:
        return {
            'small': 'https://kompetisi.id/assets/images/news-default-image.png',
            'original': 'https://kompetisi.id/assets/images/news-default-image.png'
        }
    else:
        try:
            image = json.loads(image)
            return {
                'small': image['small'] if image['small'].find('http') > -1 else os.environ.get('MEDIA_HOST', 'https://media.kompetisi.id') + image['small'],
                'original': image['original'] if re.match(r'^http', image['original']) else os.environ.get('MEDIA_HOST', 'https://media.kompetisi.id') + image['original']
            }
        except ValueError:
            return {
                'small': 'https://kompetisi.id/assets/images/news-default-image.png',
                'original': 'https://kompetisi.id/assets/images/news-default-image.png'
            }
