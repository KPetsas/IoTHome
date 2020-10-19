## Application Conventions
1. In order to add new routes, such as devices.routes that has the endpoint /devices, which is associated with the devices.controllers.Devices, which handles the requests for this endpoint, you should add to your new package a routes.py module and follow the same logic as the other routes.py files -> Inherit the Route abstract base class from the router.py and implement the register_routes abstract method.

## How to start the app:
```
1. Install requirements.
2. $ source .env_dev
3. $ flask run --host=0.0.0.0 --port=9191
```

## Swagger
Swagger is available at the */apidocs* endpoint. E.g. http://localhost:9191/apidocs/
