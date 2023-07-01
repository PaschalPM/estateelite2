from core import app
from auth import auth_api_bp
import core.manage.api_http_error

''' API '''
app.register_blueprint(auth_api_bp)


@app.route('/')
def index():
    return {'msg': 'HOME'}

if __name__ == '__main__':
    host = app.config.get('HOST')
    port = app.config.get('PORT')
    app.run(host=host, port=port)