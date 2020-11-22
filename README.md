# IoT Home

This is a ready to deploy application/platform on a Raspberry Pi with [balenaOS](https://www.balena.io/os/), which enables Docker containers to run on embedded devices.

The platform consists of:

1. A frontend with a dashboard, where the user logs in and interacts with the devices in the Smart Home.
2. A backend that receives REST requests in order to
do specific actions in Home, such as turn on/off devices, or retrieve data from
devices, such as the temperature of the fridge. The user could also schedule a device to change state at a specified date and time or interval.
3. A Mosquitto MQTT message broker that connects the devices with the backend.
4. The IoT devices that receive MQTT messages published in specific topics, in order to perform actions.
5. A postgreSQL database with users and devices data, connected through a many-to-many relationship.

# Backend

The backend is implemented with **Flask** and lets the users interact with the smart home devices through the **Mosquitto MQTT** message broker.
The user can also schedule when to turn on/off a device (**APScheduler**).

# Frontend

The **React** frontend is a client from which the user can interact with the IoTHome service. Currently it is not fully synchronized with the backend to utilize all features.

# Security

- User authentication method: **JWT** (JSON Web Tokens).
- The frontend is available only through **HTTPS** and its build is served as static content through Nginx web server. The React application contains **protected routes** where only authorized users are able to access them.
- The backend runs behind a Nginx reverse proxy and connects to the devices through a secure MQTT connection. The mosquitto MQTT broker is configured to use **TLS security**. The MQTT client connects to the broker using a **SSL** connection.
- The IoT devices connect to the secure MQTT broker, only after verifying its certificate **fingerprint** (the firmware is not available in the GitHub repository).
- The database container is in a **separate network** from the container with the Nginx web server and the frontend of the application, as defined in the docker-compose.yml.

## Author

* **Konstantinos Petsas**

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details.
