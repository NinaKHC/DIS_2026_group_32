@echo off
REM Start the Streamlit app with Docker Compose
echo Starting the app...
docker-compose up -d
echo.
echo Waiting for the app to start...
timeout /t 5 /nobreak
echo Opening app in browser...
start http://localhost:8501
pause
