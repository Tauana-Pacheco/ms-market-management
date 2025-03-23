from flask import Flask
from Application.Controller.user_controller import UserController
from config import Config, db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.route('/register', methods=['POST'])(UserController.register)
app.route('/activate', methods=['POST'])(UserController.activate)
app.route('/login', methods=['POST'])(UserController.login)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == "__main__":
    app.run(debug=True)
