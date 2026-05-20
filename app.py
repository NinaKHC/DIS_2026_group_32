import streamlit as st
import os
from sqlalchemy import create_engine, inspect

st.set_page_config(page_title="PostgreSQL + Streamlit", layout="wide")

st.title("PostgreSQL + Streamlit Docker Setup")

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/streamlit_db")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as conn:
        st.success("✅ Connected to PostgreSQL database!")
        
        # Display database info
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        st.subheader("Database Tables")
        if tables:
            st.write(f"Found {len(tables)} table(s): {', '.join(tables)}")
        else:
            st.info("No tables found in the database yet.")
            
except Exception as e:
    st.error(f"❌ Failed to connect to database: {str(e)}")

st.markdown("""
---
## Getting Started

1. Make sure Docker and Docker Compose are installed
2. Customize your environment variables in `.env`
3. Run `docker-compose up` to start both PostgreSQL and Streamlit
4. Open http://localhost:8501 in your browser
""")
