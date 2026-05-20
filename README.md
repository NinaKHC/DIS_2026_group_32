# Streamlit + PostgreSQL Docker Setup

This project uses Docker and Docker Compose to run a Streamlit application with a PostgreSQL database.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Project Structure

```
.
├── Dockerfile              # Container image for Streamlit app
├── docker-compose.yml      # Orchestrates Streamlit + PostgreSQL
├── .env.example            # Example environment variables
├── .dockerignore           # Files to exclude from Docker build
├── requirements.txt        # Python dependencies
├── app.py                  # Main Streamlit application
└── README.md              # This file
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd DIS_2026_group_32
```

### 2. Create Environment File

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
```

Edit `.env` to change database credentials if desired:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=streamlit_db
```

### 3. Build and Start Containers

```bash
docker-compose up --build
```

This will:
- Build the Streamlit Docker image
- Start PostgreSQL container
- Start Streamlit container
- Set up networking between them

### 4. Access the Application

Open your browser and go to: **http://localhost:8501**

## Common Commands

### Start containers (if already built)
```bash
docker-compose up
```

### Stop containers
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs streamlit  # Streamlit logs
docker-compose logs postgres   # PostgreSQL logs
```

### Access PostgreSQL from command line
```bash
docker-compose exec postgres psql -U postgres -d streamlit_db
```

### Rebuild after changes to requirements.txt
```bash
docker-compose up --build
```

### Remove everything (including data)
```bash
docker-compose down -v
```

## Connecting to PostgreSQL in Your Streamlit App

Use the `DATABASE_URL` environment variable:

```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
```

Or for psycopg2:

```python
import psycopg2
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
```

## Troubleshooting

### Port Already in Use
If ports 8501 or 5432 are in use, modify the `docker-compose.yml`:

```yaml
ports:
  - "8502:8501"    # Use 8502 instead
```

### Database Connection Refused
Ensure PostgreSQL is fully started before Streamlit connects. The `docker-compose.yml` has health checks to manage this.

### Permission Denied
On Linux, you might need to run Docker commands with `sudo`:

```bash
sudo docker-compose up
```

Or add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

## Next Steps

1. Modify `requirements.txt` to add more Python packages as needed
2. Update `app.py` with your Streamlit application code
3. Create database migration scripts if needed
4. Consider adding volumes for persistent data storage
5. Set up CI/CD workflows for automated deployment

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
