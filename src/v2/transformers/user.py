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
    # ref: https://stackoverflow.com/a/50763403/2780875
    'register_date': n.tgl_gabung.strftime("%Y-%m-%d %H:%M:%S"),
    'user_key': n.user_key
  }