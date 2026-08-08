from shared.db import db, utc_now


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_pinned = db.Column(db.Boolean, default=False)
    color = db.Column(db.String(20), default="default")
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
    user_id = db.Column(db.Integer, nullable=False, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "is_pinned": self.is_pinned,
            "color": self.color,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user_id": self.user_id,
        }
