def transform(n):
    return {
      'id': n.id,
      'author': {
          'id': n.id_user,
          'username': n.username
      },
      'content': n.content,
      'image': transformImage(n.image),
      'is_draft': n.status == 'draft',
      'created_at': n.created_at.strftime('%s'),
      'updated_at': n.updated_at.strftime('%s'),
      'tag': n.tag 
    }

def transformImage(n):
    return {

    }