import streamlit as st
import pandas as pd
import datetime

# 🎡 European wheel physical layout
wheel_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# 🧠 Session state setup
for key in ["spins", "predictions", "balance", "history", "wins", "losses", "streak", "max_streak"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key in ["spins", "predictions", "history"] else 0

# 🔧 Logic functions
def get_neighbors(num):
    i = wheel_order.index(num)
    return [
        wheel_order[(i - 2) % len(wheel_order)],
        wheel_order[(i - 1) % len(wheel_order)],
        wheel_order[(i + 1) % len(wheel_order)],
        wheel_order[(i + 2) % len(wheel_order)],
        wheel_order[(i - 18) % len(wheel_order)],
        wheel_order[(i + 18) % len(wheel_order)]
    ]

def get_hot(spins):
    freq = pd.Series(spins).value_counts()
    return freq.idxmax() if not freq.empty else None

def get_trend(spins):
    if len(spins) < 3:
        return None
    indices = [wheel_order.index(s) for s in spins[-3:]]
    return wheel_order[int(sum(indices) / len(indices))]

def predict(spins):
    base = get_neighbors(spins[-1])
    hot = get_hot(spins)
    trend = get_trend(spins)
    return list(dict.fromkeys(base + [hot] + ([trend] if trend else [])))[:8]

# 🎯 UI
st.markdown("<h4 style='text-align:center;'>108Spin Predictor</h4>", unsafe_allow_html=True)
st.caption("🧠 European Strategy • Unit-Based • Prediction Tracker")

# 💰 Balance setup
if st.session_state["balance"] == 0:
    starting = st.number_input("Set starting balance (units)", min_value=1, step=1)
    if st.button("💳 Set Balance"):
        st.session_state["balance"] = starting
        st.success(f"🔢 Starting balance: {starting} units")

# 🎰 Spin input
if st.session_state["balance"] > 0 and len(st.session_state["spins"]) < 108:
    new_spin = st.number_input("Enter spin result (0–36)", min_value=0, max_value=36, step=1)
    if st.button("🎯 Log Spin", key="log_spin"):
        st.session_state["spins"].append(new_spin)
        st.success(f"Spin {len(st.session_state.spins)} logged: {new_spin}")

        if len(st.session_state["spins"]) >= 12:
            prediction = predict(st.session_state["spins"])
            st.session_state["predictions"].append(prediction)
            st.info(f"🔮 Suggested numbers for next spin: {prediction}")
        else:
            st.warning(f"Waiting for {12 - len(st.session_state.spins)} more spins...")

# 🎲 Outcome checker
if st.session_state["predictions"]:
    result_spin = st.number_input("Check outcome: Enter spin after prediction", min_value=0, max_value=36, step=1)
    if st.button("✅ Evaluate Spin", key="evaluate"):
        latest_prediction = st.session_state["predictions"][-1]
        is_win = result_spin in latest_prediction

        if is_win:
            st.session_state["balance"] += 36
            st.session_state["wins"] += 1
            st.session_state["streak"] += 1
            st.session_state["max_streak"] = max(st.session_state["streak"], st.session_state["max_streak"])
            st.success(f"🎉 WIN! +36 units → Balance: {st.session_state['balance']} units")
        else:
            cost = len(latest_prediction)
            st.session_state["balance"] -= cost
            st.session_state["losses"] += 1
            st.session_state["streak"] = 0
            st.error(f"❌ Missed. -{cost} units → Balance: {st.session_state['balance']} units")

        st.session_state["history"].append({
            "spin": result_spin,
            "predicted": latest_prediction,
            "outcome": "Win" if is_win else "Loss",
            "balance": st.session_state["balance"],
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        })

# 📈 Stats
st.markdown("---")
st.subheader("📊 Session Stats")
total_spins = len(st.session_state["spins"])
total_preds = len(st.session_state["predictions"])
hit_rate = (st.session_state["wins"] / total_preds) * 100 if total_preds else 0

st.metric("Total Spins", total_spins)
st.metric("Predictions Made", total_preds)
st.metric("Hit Rate)
