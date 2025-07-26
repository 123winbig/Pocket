import streamlit as st
import pandas as pd
import random

# European wheel in physical layout
wheel_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# Session state for spins and predictions
if "spins" not in st.session_state:
    st.session_state.spins = []
if "predictions" not in st.session_state:
    st.session_state.predictions = []

# Logic helpers
def get_neighbors(num):
    idx = wheel_order.index(num)
    neighbors = [
        wheel_order[(idx - 2) % len(wheel_order)],
        wheel_order[(idx - 1) % len(wheel_order)],
        wheel_order[(idx + 1) % len(wheel_order)],
        wheel_order[(idx + 2) % len(wheel_order)],
        wheel_order[(idx - 18) % len(wheel_order)],
        wheel_order[(idx + 18) % len(wheel_order)]
    ]
    return neighbors

def get_hot(spins):
    freq = {num: spins.count(num) for num in set(spins)}
    return max(freq, key=freq.get)

def get_trend(spins):
    if len(spins) < 3:
        return None
    last_idxs = [wheel_order.index(s) for s in spins[-3:]]
    avg_idx = int(sum(last_idxs) / 3)
    return wheel_order[avg_idx]

def predict_next(spins):
    last = spins[-1]
    base_numbers = get_neighbors(last)
    hot = get_hot(spins)
    trend = get_trend(spins)
    suggested = base_numbers + [hot]
    if trend:
        suggested.append(trend)
    return list(dict.fromkeys(suggested))[:8]

# UI
st.title("🎰 European Roulette Spin Tracker")
st.markdown("Log each spin (0–36) and get predictions after 12 spins.")

spin = st.number_input("Enter spin result (0–36)", min_value=0, max_value=36, step=1)
if st.button("Log Spin"):
    if spin in wheel_order:
        st.session_state.spins.append(spin)
        st.success(f"Spin {spin} logged.")

        # Predict when ready
        if len(st.session_state.spins) >= 12:
            prediction = predict_next(st.session_state.spins)
            st.session_state.predictions.append(prediction)
            st.info(f"🔮 Suggested bet for next spin: {prediction}")
        else:
            st.warning(f"🕒 Waiting for {12 - len(st.session_state.spins)} more spins to begin predictions.")
    else:
        st.error("Invalid spin number.")

# Spin history
if st.session_state.spins:
    st.subheader("📜 Spin History")
    st.write(st.session_state.spins)

# Prediction history
if st.session_state.predictions:
    st.subheader("🔮 Prediction History")
    for i, p in enumerate(st.session_state.predictions, start=1):
        st.write(f"Prediction {i}: {p}")

# Reset
if st.button("Reset Session"):
    st.session_state.spins = []
    st.session_state.predictions = []
    st.success("Session reset.")
