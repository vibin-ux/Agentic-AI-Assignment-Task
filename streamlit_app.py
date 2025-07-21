import streamlit as st
from run_agent import run_analysis_task
import random
import time

st.set_page_config(page_title="🏀 Agentic AI Coach", layout="centered")
st.title("🏀 Agentic AI Coach")
st.markdown("Analyze the last 20 night games of the Golden State Warriors to improve performance.")

# --- Reaction Timer Game (for fun) ---
def reaction_game():
    st.subheader("🎮 Mini Reaction Game")
    st.markdown("Click the button **as fast as you can** after it turns green!")

    if "game_started" not in st.session_state:
        st.session_state.game_started = False
        st.session_state.reaction_start = 0.0
        st.session_state.reaction_time = 0.0

    if not st.session_state.game_started:
        if st.button("Start Game"):
            st.session_state.game_started = True
            st.session_state.reaction_start = time.time() + random.uniform(2, 5)
            st.session_state.reaction_time = 0.0
    else:
        now = time.time()
        if now >= st.session_state.reaction_start:
            if st.button("Click Now!"):
                reaction = time.time() - st.session_state.reaction_start
                st.session_state.reaction_time = reaction
                st.session_state.game_started = False
                st.success(f"⚡ Your reaction time: {reaction:.3f} seconds!")
        else:
            st.info("⏳ Wait for green...")

# --- Main Agent Button ---
if st.button("🎯 Generate Coaching Advice"):
    with st.spinner("Analyzing past 20 night games... this might take 1-2 minutes. Play a mini game below!"):
        response = run_analysis_task()
    st.success("✅ Analysis complete!")
    st.markdown("### 💡 Agent Insight")
    st.write(response)
else:
    reaction_game()
