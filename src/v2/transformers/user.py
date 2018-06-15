def transform(n):
  return {
    'id': n.id_user,
    'fullname': n.fullname,
    'username': n.username,
    'email': n.email,
    'moto': n.moto,
    'status': n.status,
    'level': n.level,
    'is_verified': n.is_verified == 1,
  }