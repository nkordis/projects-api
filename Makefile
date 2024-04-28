.PHONY: help lint test

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
	docker-compose run --rm app sh -c "python manage.py test"
