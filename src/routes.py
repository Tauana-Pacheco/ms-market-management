from flask import Flask
from Application.Controller.user_controller import UserController
from config import Config, db
from Application.Controller.product_controller import ProductController
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

SQLALCHEMY_ECHO = True

app.route('/register', methods=['POST'])(UserController.register)
app.route('/activate', methods=['POST'])(UserController.activate)
app.route('/login', methods=['POST'])(UserController.login)
app.route('/register_produto', methods=['POST'])(ProductController.register_product)
app.route('/produtos', methods=['GET'])(ProductController.listar_produtos)
app.route('/assets/<path:filename>', methods=['GET'])(ProductController.serve_assets)
app.route('/produtos/<int:produto_id>/imagem', methods=['POST'])(ProductController.atualizar_imagem)
app.route('/produtos/<int:id>', methods=['GET'])(ProductController.get_produto)
app.route('/produtos/<int:id>', methods=['PUT'])(ProductController.atualizar_produto)

if __name__ == "__main__":
    app.run(debug=True)
