from api.auth import controllers
from api.router import Router


class AuthRouter(Router):
    """ JWT Authentication router class. """

    def register_routes(self, api):
        """ Register and relate authentication endpoints with controllers. """
        api.add_resource(controllers.UserRegistration, '/registration')
        api.add_resource(controllers.UserLogin, '/login')
        api.add_resource(controllers.TokenRefresh, '/token/refresh')
