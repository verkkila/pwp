import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


#https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2019/flask-api-project-layout/#using-application-factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///../db/pwp.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.app = app
    db.init_app(app)

    from . import api
    app.register_blueprint(api.api_bp)

    from . import models
    app.cli.add_command(models.init_db_command)
    return app
