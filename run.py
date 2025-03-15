from flask import Flask
from flask_migrate import Migrate
from app.config import Config
from app.core.domain.seller import db
from app.controllers.seller_controller import seller_bp
from app.controllers.auth_controller import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

# inicializar o banco de dados
db.init_app(app)

# configurar Flask-Migrate
migrate = Migrate(app, db)

# registrar os Blueprints
app.register_blueprint(seller_bp, url_prefix='/seller')
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == "__main__":
    app.run(debug=True)