from flask import Flask
from Application.Controller.user_controller import UserController
from Application.Service.user_service import UserService
from config import Config, db
from Application.Controller.product_controller import ProductController
from Infrastructure.Http.whatsapp import WhatsAppService
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

SQLALCHEMY_ECHO = True

user_service = UserService(WhatsAppService())
user_controller = UserController(user_service)

app.route('/register', methods=['POST'])(user_controller.register)
app.route('/activate', methods=['POST'])(user_controller.activate)
app.route('/login', methods=['POST'])(user_controller.login)
app.route('/register_produto', methods=['POST'])(ProductController.register_product)
app.route('/produtos', methods=['GET'])(ProductController.listar_produtos)
app.route('/assets/<path:filename>', methods=['GET'])(ProductController.serve_assets)
app.route('/produtos/<int:produto_id>/imagem', methods=['POST'])(ProductController.atualizar_imagem)
app.route('/produtos/<int:id>', methods=['GET'])(ProductController.get_produto)
app.route('/produtos/<int:id>', methods=['PUT'])(ProductController.atualizar_produto)

if __name__ == "__main__":
    app.run(debug=True)
