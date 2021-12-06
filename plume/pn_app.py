import panel as pn
from .rp import Dashboard

def app(doc):
    db = Dashboard()
    row = pn.Row(db.param, db.plot)
    row.server_doc(doc)
