# Makefile for Python project with Docker Compose

# Variables
DOCKER_COMPOSE = docker-compose

# Start services
.PHONY: api
api:
	$(DOCKER_COMPOSE) up -d --build
