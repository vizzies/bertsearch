from flask import current_app as app_ref, request
from bertsearch.extensions import celery, db
from bertsearch.tasks.examples import example1
from bertsearch.api.schemas import ResultSchema

import pickle

current_app = app_ref._get_current_object()

@current_app.route("/", methods=["GET"])
def index():
    host = request.host
    return f"QueryAPI located at {host}/api/v1/results", 200

@current_app.route("/clear", methods=["GET"])
def clear_tables():
    
    db.drop_all()
    db.create_all()

    return 'All tables dropped and re-added', 200

@current_app.route("/addall", methods=["GET"])
def add_all():
    with open('/Users/etyates/Desktop/arc-code-ti-publications.pkl', 'rb') as f:
        corpus_dataframe = pickle.load(f)

    for indx, (ind, row) in enumerate(corpus_dataframe.iterrows()):
    
        doc_id = ind

        result_obj = {
            "id": indx,
            "link": row[0] if type(row[0])==str else "",
            "text": row[1] if type(row[1])==str else "",
            "abstract": row[3] if type(row[3])==str else "",
            "title": row[5] if type(row[5])==str else "",
            "authors": row[6] if type(row[6])==str else "",
            "publisher": row[7] if type(row[7])==str else "",
            "date": row[8] if type(row[8])==str else ""            
        }
        print(ind)
        schema = ResultSchema()
        result = schema.load(result_obj)

        db.session.add(result)
        
    db.session.commit()
        

    return "Done", 200


