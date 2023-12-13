# Mac configuaration 
# Makefile for Docker project with docker-compose

IMAGE_NAME := your_image_name
CONTAINER_NAME := $(IMAGE_NAME)_web
MONGO_CONTAINER_NAME := $(IMAGE_NAME)_mongodb
API_URL = http://localhost:5000

insert_data:
	curl -X POST $(API_URL)/add_memes_from_api
	curl -X POST $(API_URL)/update_pokemon_data

delete_data:
	curl -X DELETE $(API_URL)/delete_all_data

web: # https://stackoverflow.com/questions/63279765/docker-how-to-update-your-container-when-your-code-changes
	- docker compose down web
	- docker compose up -d web

build:
	docker compose build -q

up:
	docker compose up -d

down:
	docker compose down

clean: down
	- docker rmi $(IMAGE_NAME)_web
	- rm -r ./data


# # Makefile for Docker project with docker-compose

# IMAGE_NAME := your_image_name
# CONTAINER_NAME := $(IMAGE_NAME)_web
# MONGO_CONTAINER_NAME := $(IMAGE_NAME)_mongodb

# build:
# 	docker-compose build -q

# up:
# 	docker-compose up -d

# down:
# 	docker-compose down

# clean: down
# 	docker rmi $(IMAGE_NAME)_web

