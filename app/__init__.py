from  flask import Flask

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    @app.route('/')
    def home():
        return "<h1>Hello, World!</h1>"
    
    from app.routes.auth import auth
    from app.routes.views import view
    app.register_blueprint(auth)
    app.register_blueprint(view)
    
    
    return app