from bertsearch.models import Result
from bertsearch.extensions import ma, db
from marshmallow import EXCLUDE
from marshmallow import pre_dump

class ResultSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(primary_key=True)
    link = ma.String()
    text = ma.String(load_only=True)
    text_abbrv = ma.String()
    abstract = ma.String()
    title = ma.String()
    authors = ma.String()
    publisher = ma.String()
    date = ma.String()

    @pre_dump(pass_many=True)
    def abbrv_text(self, data, many, **kwargs):
        if many: pass
            # try:
            #     data.update({"text": data.get("text")[:200]})
            # except Exception as e: 
            #     print(e)
        return data

    class Meta:
        model = Result
        sqla_session = db.session
        load_instance = True
        unknown = EXCLUDE

