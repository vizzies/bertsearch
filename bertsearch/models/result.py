from bertsearch.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property

class Result(db.Model):
    """Basic user model
    """

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    text = db.Column(db.String)
    abstract = db.Column(db.String)
    title = db.Column(db.String)
    authors = db.Column(db.String)
    publisher = db.Column(db.String)
    date = db.Column(db.String)

    @hybrid_property
    def text_abbrv(self):
        return self.text[:200]
    
    
    def __init__(self, **kwargs):
        super(Result, self).__init__(**kwargs)

    def __repr__(self):
        return f"<Result id: {self.id}, text: {self.text}"
