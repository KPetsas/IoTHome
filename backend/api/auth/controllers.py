import config

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flasgger import swag_from

from app_initialization import app, devices_cache
from auth.models import UserModel

# Set the request arguments to be expected.
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('email', help='This field cannot be blank', required=False)
parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    """ User registration controller. """

    @swag_from('swagger/sign_up_swag.yml')
    def post(self):
        # Parse the data from the POST request.
        data = parser.parse_args()

        # Find if the user already exists in DB.
        if UserModel.find_by_username(data['username']):
            return dict(message='User {} already exists'.format(data['username']))

        # Create a new user model.
        new_user = UserModel(
            username=data['username'],
            email=data['email'],
            password=UserModel.generate_hash(data['password'])
        )

        try:
            # Save model in DB.
            new_user.save_to_db()
            # Create access and refresh tokens, based on username and return them.
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return (dict(
                message='User {} was created'.format(data['username']),
                access_token=access_token,
                refresh_token=refresh_token
            ), 201)
        except Exception as e:
            app.logger.error(e)
            return (dict(message='Something went wrong'), 400)


class UserLogin(Resource):
    """ User login controller. """

    @swag_from('swagger/login_swag.yml')
    def post(self):
        # Parse the data from the POST request.
        data = parser.parse_args()
        # Find the current user model from DB.
        current_user = UserModel.find_by_username(data['username'])

        # Handle no user found.
        if not current_user:
            return dict(status=401)

        # Verify user password.
        if UserModel.verify_hash(data['password'], current_user.password):
            if config.CACHE_ENABLED:
                # Clear user cache in order to refresh it.
                devices_cache.clear_user_cache(current_user.id)
            # Return the access and refresh tokens, created based on username.
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return dict(
                status=200,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        else:
            return (dict(message='User login failed.'), 401)


class TokenRefresh(Resource):
    """
    Token refresh controller.
    When the access token expires, refresh it by using the refresh token.
    """

    @jwt_refresh_token_required
    @swag_from('swagger/refresh_token_swag.yml')
    def post(self):
        """ POST method that requires the JWT refresh token, in order to return the new access token. """
        # Get username from JWT.
        current_user = get_jwt_identity()
        # Create an access token, based on the username.
        access_token = create_access_token(identity=current_user)
        return dict(access_token=access_token)
