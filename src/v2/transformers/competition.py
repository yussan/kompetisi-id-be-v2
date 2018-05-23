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
    # ref teranary condition: https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
    'announcement': json.loads(n.dataPengumuman) if n.dataPengumuman else [],
    'contacts': json.loads(n.kontak) if n.kontak else [],
    'tag': n.tag,
    'link_source': n.sumber,
    'link_join': n.ikuti,
    'views': n.views
  }