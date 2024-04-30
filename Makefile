.PHONY: help lint test makemigrations migrate

# Display callable targets to the user
help:
	@echo "Usage:"
	@echo "  make lint        Run flake8 to check the code for style issues."
	@echo "  make unit-tests        Run unit tests to check code components."

# Run the linting tool
lint:
	@echo "Running flake8 linting inside the Docker container..."
	docker-compose run --rm app sh -c "flake8 /app --verbose"

# Run unit tests
test:
	@echo "Running unit tests..."
	docker-compose run --rm app sh -c "python manage.py test && flake8"

# Create new migrations based on changes to Django models.
makemigrations:
	@echo "Creating new migrations based on model changes..."
	docker-compose run --rm app sh -c "python manage.py makemigrations"
	@echo "Migrations created successfully."

# Ensures that the database is ready and then applies Django migrations to update the database schema according to the latest models.
migrate:
	@echo "Checking database availability..."
	docker-compose run --rm app sh -c "python manage.py wait_for_db"
	@echo "Applying database migrations..."
	docker-compose run --rm app sh -c "python manage.py migrate"
	@echo "Database migration completed successfully."
