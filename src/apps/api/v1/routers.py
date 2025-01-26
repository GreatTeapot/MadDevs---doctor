from api.v1.controllers.auth import auth
from api.v1.controllers.user import user
from api.v1.controllers.patient import patient

routers = [
    auth,
    user,
    patient,
]