from majcalc import loginManager
from majcalc.models import User

@loginManager.user_loader
def loadUser(id):
    user = User.query.get(int(id))
    return user