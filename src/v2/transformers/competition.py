def transform(n):
  return {
    'id': n.id_kompetisi,
    'user': {
      'id': 1,
      'username': n.username,
      'name': n.fullname
    }
  }