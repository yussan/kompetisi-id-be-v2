from v2.helpers.encId import encId
# ref: http://docs.python-guide.org/en/latest/scenarios/json/
import json

def transform(n):
  return {
    # 'id': n.id_kompetisi,
    'id': encId(n.id_kompetisi),
    'title': n.judul_kompetisi,
    'sort': n.sort,
    'organizer': n.penyelenggara,
    'deadline_at': n.deadline.strftime('%s'),
    'announcement_at': n.pengumuman.strftime('%s'),
    'created_at': n.created_at.strftime('%s'),
    'updated_at': n.updated_at.strftime('%s'),
    'is_mediapartner': n.mediapartner == 1,
    'is_garansi': n.garansi == 1,
    'content': n.konten,
    'prize': {
      'total': n.total_hadiah,
      'description': n.hadiah
    },
    'poster': '',
    'main_category': {
      'id': n.id_main_kat,
      'name': n.main_kat,
    },
    'sub_category': {
      'id': n.id_sub_kat,
      'name': n.sub_kat
    },
    'user': {
      'id': 1,
      'username': n.username,
      'name': n.fullname
    },
    # 'announcement': json.loads(n.dataPengumuman),
    'contacts': json.loads(n.kontak),
    'tag': n.tag,
    'link_source': n.sumber,
    'link_join': n.ikuti
  }