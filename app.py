from flask import Flask, render_template
from flask_migrate import Migrate



from config import Config

from extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    
    # LOGIN MANAGER
    login_manager.init_app(app)
    
    login_manager.login_view = "auth.login"
    
    
    
# ALL OUR MODELS
    from models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    from models.assignment import Assignment
    
    
    
    
    
# ALL OUR ROUTES
    from routes.main import main
    from routes.auth import auth
    from routes.admin import admin
    

    
    
    
    


#   ALL OUR BLUEPRINTS  
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    
    
    
    
    
    
    
    
    with app.app_context():
        db.create_all()
        
    return app 

app = create_app()

Migrate = Migrate(app, db)



@app.errorhandler(404)

def page_not_found(error):
     return render_template(
         "404.html"
     ), 404
     
     
@app.errorhandler(500)

def page_not_found(error):
     return render_template(
         "500.html"
     ), 500
     
     

   


if __name__ == "__main__":
    app.run(debug=True)