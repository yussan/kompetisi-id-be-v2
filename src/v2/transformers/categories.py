def transformMainCategory(n):
  return {
    'id': n.id_main_kat,
    'name': n.main_kat,
    'color': n.color,
    'description': n.deskripsi
  }

def transformSubCategory(n):
  return {
    'id': n.id_sub_kat,
    'name': n.sub_kat
  }