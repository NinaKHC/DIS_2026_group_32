import os
import threading
import time

import streamlit as st


def stop_app_after_delay(delay_seconds: float = 1.5) -> None:
    """
    Stops the Streamlit process after a short delay.

    In Docker this will usually stop the container, because the Streamlit
    process is the main process inside the container.
    """

    def stop_process():
        time.sleep(delay_seconds)
        os._exit(0)

    thread = threading.Thread(target=stop_process, daemon=True)
    thread.start()


def show_exit_screen() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #101522, #1c2433);
            color: white;
        }

        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        .exit-container {
            text-align: center;
            margin-top: 22vh;
            font-family: Arial, Helvetica, sans-serif;
        }

        .exit-title {
            font-size: 64px;
            font-weight: 900;
            color: #f5d28a;
            text-shadow: 3px 3px 8px black;
            margin-bottom: 20px;
        }

        .exit-text {
            font-size: 28px;
            color: #f2f2f2;
            margin-bottom: 40px;
        }

        .exit-small-text {
            font-size: 18px;
            color: #b8b8b8;
            margin-top: 30px;
        }
        </style>

        <div class="exit-container">
            <div class="exit-title">EXITING GAME</div>
            <div class="exit-text">The game is closing...</div>
            <div class="exit-small-text">
                You can close this browser tab after the server stops.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    stop_app_after_delay()