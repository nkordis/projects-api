# Projects API

[![CI Status](https://github.com/nkordis/projects-api/actions/workflows/main.yml/badge.svg)](https://github.com/nkordis/projects-api/actions)

An API designed to dynamically manage and display a portfolio of software projects.

<p align="center">
  <img src="docs/images/projects-api-1.PNG" alt="projects-api-1" width="300"/>
  <img src="docs/images/projects-api-2.PNG" alt="projects-api-2" width="300"/>
  <img src="docs/images/projects-api-3.PNG" alt="projects-api-3" width="300"/>
</p>

## Description

This project is a RESTful API built with Django and Django REST Framework, providing endpoints to manage user profiles, projects, tags, and related functionalities.

## Installation

To install the project, clone the repository and build the Docker containers. Use `docker-compose up` to start the application.

## Usage

After installation, the API documentation can be accessed at `http://localhost:8000/api/docs`. Use endpoints to manage projects, tags, links, and user profiles.

## Features

-   User profile management
-   Project CRUD operations
-   Tagging system
-   Filtering and searching

### User Authentication

To create a new user and authenticate with the API, follow these steps:

1.  **Create a New User**:

   -   Send a `POST` request to `/api/user/create/` with the required user details.
   -   Example payload:
    ``
    {
  "email": "user@example.com",
  "password": "password123"
	}
  ``

2. **Obtain an Authentication Token**:

-   Send a `POST` request to `/api/user/token/` with the user's credentials.
-   The response will include a token:
 ``
 {
  "token": "your_generated_token"
}
``

3. **Authorize Requests**:

-   Use the obtained token to authorize requests to the API.
-   Include the token in the `Authorization` header of your requests:
``
Authorization: Token your_generated_token
``

## Project Details

The `project` item in the REST API includes URL mappings for project-related endpoints. These mappings make it easy to manage projects, tags, and links through the API.

##   Database

The project uses PostgreSQL as its database. The Docker setup includes a service for PostgreSQL, which will be automatically set up when you run `docker-compose up`.

## Deployment

For deployment, Docker and Docker Compose are used. The project includes configurations for building and deploying containers, ensuring the application runs smoothly in different environments.

## Testing and Linting

Comprehensive tests are included to ensure the functionality and reliability of the API, along with linting to maintain code quality.

### Running Tests and Linting

To run the tests and linting, use the following command:
``
docker-compose run --rm app sh -c "python manage.py test && flake8"
``

This command will execute the unit tests and perform linting with Flake8 inside the Docker container.

## GitHub Actions

The project uses GitHub Actions for continuous integration. The workflow includes steps for testing, linting, and building Docker images.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Resources

-   [Django Documentation](https://docs.djangoproject.com/)
-   [Django REST Framework Documentation](https://www.django-rest-framework.org/)
-   [Docker Documentation](https://docs.docker.com/)
-   [GitHub Actions Documentation](https://docs.github.com/en/actions)

Test
