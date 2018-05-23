from v2.helpers.encId import encId

def transform(n):
  return {
    'id': encId(n.id_kompetisi),
    'title': n.judul_kompetisi,
    'sort': n.sort,
    'penyelenggara': n.penyelenggara,
    'deadline_at': n.deadline.strftime('%s'),
    'announcement_at': n.pengumuman.strftime('%s'),
    'created_at': n.created_at.strftime('%s'),
    'updated_at': n.updated_at.strftime('%s'),
    'is_mediapartner': n.mediapartner == 1,
    'is_garansi': n.garansi == 1,
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
    }
  }