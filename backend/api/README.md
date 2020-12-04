## Application Conventions
1. In order to add new routes, such as devices.routes that has the endpoint /devices, which is associated with the devices.controllers.Devices, which handles the requests for this endpoint, you should add to your new package a routes.py module and follow the same logic as the other routes.py files -> Inherit the Route abstract base class from the router.py and implement the register_routes abstract method.

2. In order to add new models, such as devices.models, you should add to your new package a models.py module and follow the same logic as the other models.py files -> Inherit the BaseModel abstract class from the base_model.py.

## How to start the app (development server):
```
1. Install requirements.
2. $ source .env_dev
3. (Optional) If there are any changes in the models, make the migrations with the following command:
     $ python manage.py db migrate -m "Your message."
4. Create the DB tables with the following command:
     $ python manage.py db upgrade
5. $ python manage.py runserver --host=0.0.0.0 --port=9191

```
*Note: create a migration repository with the command: ```$ python manage.py db init```*

## Swagger
Swagger is available at the */apidocs* endpoint. E.g. http://localhost:9191/apidocs/
