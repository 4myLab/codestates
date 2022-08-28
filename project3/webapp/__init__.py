from flask import Flask

def create_app(config=None):
    app = Flask(__name__) #static , static_folder='./css'
    
    # Page import
    from webapp.controller.mainController import main_bp
    # from webapp.controller.resultController import result_bp
    
    # Blueprint setting
    app.register_blueprint(main_bp)
    # app.register_blueprint(result_bp)
    return app