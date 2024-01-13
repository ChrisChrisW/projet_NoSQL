# Flask Multi-Service Application

## Overview

This project is a Flask-based multi-service application that integrates various databases and services, including MongoDB, Redis, PostgreSQL, Neo4j, and Elasticsearch. It serves as a modular and extensible platform for handling different types of data, from Spotify playlists to memes, Pokemon data, and real-time chat messages.

## Key Features

- **Modular Architecture:** The application is designed with a modular architecture, allowing easy integration of new services and databases.

- **Database Integration:**
  - MongoDB for managing Spotify playlist data.
  - Redis for storing and retrieving memes.
  - PostgreSQL for maintaining Pokedex information.
  - Neo4j for handling graph-based data related to chat interactions.
  - Elasticsearch for real-time chatbox functionality.

- **RESTful API:** The project provides a set of RESTful APIs for each service, allowing seamless interaction with the different data sources.

- **Dockerized Deployment:** The application can be deployed using Docker and Docker Compose, simplifying the setup and ensuring consistent environments across different platforms.

## How to Use

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ChrisChrisW/projet_NoSQL.git
    cd projet_NoSQL
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables:**

    Create a `.env` file in the root directory and add necessary environment variables.

    ```env
    # Example .env file

    # MongoDB configuration
    MONGO_PORT=27017
    MONGO_DB_URI=mongodb://mongodb:${MONGO_PORT}/
    DATABASE_NAME=your_database_name
    COLLECTION_NAME=your_collection_name
    
    # Redis configuration
    REDIS_HOST=redis
    REDIS_PORT=6379
    
    # PostgreSQL configuration
    POSTGRES_DB=mydatabase
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_PORT=5432
    POSTGRES_DB_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:${POSTGRES_PORT}/${POSTGRES_DB}
    
    # Neo4j configuration
    NEO4J_PORT=7687
    NEO4J_URI=bolt://neo4j:${NEO4J_PORT}
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=your_password
    
    # Elasticsearch configuration
    ELASTICSEARCH_PORT=9200
    ELASTICSEARCH_HOST=http://elasticsearch:${ELASTICSEARCH_PORT}
    ELASTICSEARCH_INDEX=my_index
    
    # Web service configuration
    WEB_PORT=5000
    
    # ------ front ----
    
    # Spotify
    spotify_clientId=
    spotify_clientSecret=
    ```

### Usage

#### Running with Docker

Make sure Docker and Docker Compose are installed. Use the following Makefile commands:

- **Build and Start Containers:**

  ```bash
  make up
  ```

- **Stop Containers:**

  ```bash
  make down
  ```

- **Rebuild and Start Containers:**

  ```bash
  make web
  ```

#### Inserting and Deleting Data

- **Insert Sample Data:**

  ```bash
  make insert_data
  ```

- **Delete All Data:**

  ```bash
  make delete_data
  ```

## Routes and Endpoints

- **Main Routes:**
  - `/insert_default_values` (POST)
  - `/delete_all_data` (DELETE)
  - `/` (GET)

- **MongoDB Routes - Spotify Playlist:**
  - `/get_all_mongo_data` (GET)
  - `/submit_mongo` (POST)
  - `/delete_mongo` (DELETE)

- **Redis Routes - Meme:**
  - `/add_memes_from_api` (POST)
  - `/get_memes` (GET)
  - `/add_meme` (POST)
  - `/edit_meme/<meme_id>` (PUT)
  - `/delete_meme/<meme_id>` (DELETE)

- **Postgres Routes - Pokedex:**
  - `/update_pokemon_data` (POST)
  - `/get_all_pokemon` (GET)
  - `/add_pokemon` (POST)
  - `/update_pokemon/<pokemon_id>` (PUT)
  - `/delete_pokemon/<pokemon_id>` (DELETE)

- **Neo4j Route:**
  - `/chat` (POST)

- **Elasticsearch Routes - Chatbox:**
  - `/get_messages` (GET)
  - `/send_message` (POST)
  - `/delete_message` (DELETE)

## Dependencies

List the main dependencies your project relies on, including Flask, MongoDB, Redis, PostgreSQL, Neo4j, Elasticsearch, etc.
