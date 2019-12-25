import connexion
from injector import Module, singleton, provider, Injector
from flask import render_template
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from services.storage import TodoFeed
from lib.mongo import ConnectionFactory

import settings


class DatabaseModule(Module):

    @singleton
    @provider
    def db_provider(self) -> TodoFeed:
        return TodoFeed(
            ConnectionFactory(
                settings.DB_HOST,
                settings.DB_PORT),
            'todo',
            'todos')


injector = Injector([DatabaseModule()])
app = connexion.App(__name__, specification_dir='templates')
CORS(app.app, methods=['POST', 'PUT', 'DELETE'], allow_headers=['Content-Type'])


swagger_ui = get_swaggerui_blueprint(
    settings.SWAGGER_URL,
    settings.API_SCHEMA_URL
)
app.app.register_blueprint(swagger_ui, url_prefix=settings.SWAGGER_URL)


@app.route(settings.API_SCHEMA_URL)
def api_schema():
    return render_template('todo.yaml')


@app.route('/')
def home():
    return "TODO service is worked", 200


if __name__ == '__main__':
    app.add_api('todo.yaml')
    app.run(port=8000)
