# Variables
APP_NAME = uvic-course-bot
VERSION = latest
# ECR_REPO = your-aws-account-id.dkr.ecr.your-region.amazonaws.com/$(APP_NAME)
LOCAL_PORT = 8000
CONTAINER_PORT = 8000
PYTHON_VERSION = 3.12

# Build the Docker image
.PHONY: build
build:
	docker build -t $(APP_NAME):$(VERSION) .

# Run the container locally
.PHONY: run
run: build
# Stop and remove existing container if it exists
	docker stop uvic-course-bot 2>/dev/null || true
	docker rm uvic-course-bot 2>/dev/null || true
# Run new container
	docker run -d --name $(APP_NAME) \
		-p $(LOCAL_PORT):$(CONTAINER_PORT) \
		-v $(PWD):/app \
		$(APP_NAME):$(VERSION)
	@echo "Container running at http://localhost:$(LOCAL_PORT)"

# Run for development with hot reload
.PHONY: dev
dev: build
	docker run -d --name $(APP_NAME)-dev \
		-p $(LOCAL_PORT):$(CONTAINER_PORT) \
		-v $(PWD):/app \
		$(APP_NAME):$(VERSION) \
		python -m uvicorn app:app --host 0.0.0.0 --port $(CONTAINER_PORT) --reload

# # Stop the running container
# .PHONY: stop
# stop:
# 	docker stop $(APP_NAME) || true
# 	docker rm $(APP_NAME) || true
# 	docker stop $(APP_NAME)-dev || true
# 	docker rm $(APP_NAME)-dev || true

# # Remove the container and image
# .PHONY: clean
# clean: stop
# 	docker rmi $(APP_NAME):$(VERSION) || true

# # View container logs
# .PHONY: logs
# logs:
# 	docker logs -f $(APP_NAME)

# # Open a shell in the running container
# .PHONY: shell
# shell:
# 	docker exec -it $(APP_NAME) /bin/bash

# # Run tests in the container
# .PHONY: test
# test:
# 	docker run --rm -v $(PWD):/app $(APP_NAME):$(VERSION) python -m pytest

# # Run linting checks
# .PHONY: lint
# lint:
# 	docker run --rm -v $(PWD):/app $(APP_NAME):$(VERSION) ruff check .

# # Format code
# .PHONY: format
# format:
# 	docker run --rm -v $(PWD):/app $(APP_NAME):$(VERSION) black .
# 	docker run --rm -v $(PWD):/app $(APP_NAME):$(VERSION) isort .

# # Login to ECR
# .PHONY: ecr-login
# ecr-login:
# 	aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin $(ECR_REPO)

# # Tag and push image to ECR
# .PHONY: push
# push: build ecr-login
# 	docker tag $(APP_NAME):$(VERSION) $(ECR_REPO):$(VERSION)
# 	docker push $(ECR_REPO):$(VERSION)

# # Pull image from ECR
# .PHONY: pull
# pull: ecr-login
# 	docker pull $(ECR_REPO):$(VERSION)