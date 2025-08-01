from app import db
from app.models.base_model import BaseModel

class Review(BaseModel):
    #name of the table in the db
    __tablename__ = 'reviews'

    #attributs related to the db'scolumn
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    def __repr__(self):
        return f"<Review {self.id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
