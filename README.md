
This is a simple Flask application that interacts with a PostgreSQL database (e.g., Amazon Aurora) to perform CRUD operations. The application provides endpoints for health checks, readiness checks, and managing user data.

The application is also available as a **Helm chart** for easy deployment on Kubernetes. You can find the Helm chart in the following repository: [https://victor-ocanto.github.io/fantastic-app-demo](https://victor-ocanto.github.io/fantastic-app-demo).

## Features
- **Health Check**: Endpoint to check if the application is running.
- **Readiness Check**: Endpoint to confirm the application is ready to serve requests.
- **User Management**:
  - Add a new user via a web form.
  - Fetch and display a list of users.
- **Database Integration**: Connects to a PostgreSQL database (e.g., Amazon Aurora) using environment variables.

