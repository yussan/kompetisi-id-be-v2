from v2.helpers.encId import encId

def transform(n):
  return {
    'id': n.id_kompetisi,
    'enc_id': encId(n.id_kompetisi),
    'user': {
      'id': 1,
      'username': n.username,
      'name': n.fullname
    }
  }