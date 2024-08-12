import json
import streamlit as st

class SettingsManager:
    @staticmethod
    def save_settings(data, filename = 'user_data.json') -> None:
        with open(f"data/{filename}", 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_settings(filename = 'user_data.json') -> dict | None:
        try:
            with open(f"data/{filename}", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            st.warning('No saved data found.')
            return None