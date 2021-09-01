from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor@localhost/cms'
    app.config['SECRET_KEY'] = 'donthack'
    from .views import views

    db.init_app(app)

    from .models import Seats

    db.create_all(app=app)

    

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import Users

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))  

    app.register_blueprint(views, url_prefix='/')

    return app