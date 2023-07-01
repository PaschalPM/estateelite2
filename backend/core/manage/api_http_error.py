from core import app
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_error(error):
    return{
        'status': error.code,
        'message': error.description
    }, error.code
    