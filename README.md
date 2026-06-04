# Streamlit + PostgreSQL Docker Setup

This project uses Docker and Docker Compose to run a Streamlit application with a PostgreSQL database.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/NinaKHC/DIS_2026_group_32
cd DIS_2026_group_32
```

### 2. Create Environment File

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
```

Edit `.env` to add database credentials fx:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=streamlit_db
```

### 3. Build and Start Containers
  On linux (with apt) simply run
  ```bash
  ./start.sh
  ```  

  otherwise you can manualy install docker and docker-compose and run
  
  ```bash
  sudo docker-compose up --build
  ```
  
  on windows, open Docker Desktop, and run
  ```batch
    start.bat
  ```
  
This will:
- Build the Streamlit Docker image
- Start PostgreSQL container
- Start Streamlit container
- Set up networking between them
- Open the app (or see point 4.)

### 4. Access the Application

Open your browser and go to: **http://localhost:8501**

## 5. Stopping the containers
To stop the containers run
```bash
# docker-compose down
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
