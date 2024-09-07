from wp.pages import menu
from wp.utils import Utils
import streamlit as st


def center_text_in_container(container_id):
    css=f"[data-testid='{container_id}'] {{width: fit-content; margin: auto;}}\n" +\
        f"[data-testid='{container_id}'] > div {{width: fit-content; margin: auto;}}\n" +\
        f"[data-testid='{container_id}'] label {{width: fit-content; margin: auto;}}\n"

    return css

def boot():
    pass 

def startup():
    st.set_page_config(
        page_title="PFWatchPoint",
        layout='wide')
    
    Utils.hide_anchor_link()
    st.markdown(f"<style>{center_text_in_container('stMetric')}</style>",unsafe_allow_html=True)
    st.markdown("<style>[id='account-balances'] {width: fit-content; margin: auto;}</style>", unsafe_allow_html=True)
    st.markdown("<style>[id='networth-metrics'] {width: fit-content; margin: auto;}</style>", unsafe_allow_html=True)
    menu()
    Utils.init_db()