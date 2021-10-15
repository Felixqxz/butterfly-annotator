from .models import User

def setup_user_loader(login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user(user_id)
