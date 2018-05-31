def transform(n):
  return {
    'id': n.id_req, 
    'title': n.nama,
    'email': n.email,
    'link': n.link,
    'poster': n.poster,
    'status': n.status,
    'created_at': n.created_at.strftime('%s'),
    'updated_at': n.updated_at.strftime('%s'),
    'accepted_at': n.accepted_at.strftime('%s'),
    'note': n.note
  }