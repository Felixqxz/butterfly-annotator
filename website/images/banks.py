from ..database.access import db
from ..database.models import ImageAnnotation

def delete_bank(bank):
  db.session.delete(bank)
  db.session.commit()
  for image in bank.images:
    db.session.query(ImageAnnotation).filter(ImageAnnotation.image_id == image.id).delete()
    db.session.commit()
    db.session.delete(image)
  for access in bank.accesses:
    db.session.delete(access)
  db.session.commit()
