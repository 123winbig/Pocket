import streamlit as st
import pandas as pd

# Initialize session state
if "spins" not in st.session_state:
    st.session_state.spins = []
if "balance" not in st.session_state:
    st.session_state.balance = 0

# Title and Introduction
st.title("🎰 Roulette Tracker")
st.markdown("Log your spins, track your balance, and see what might be next!")

# Input Section
spin = st.number_input("🎯 Enter spin result (0–36):", min_value=0, max_value=36, step=1)
bet = st.number_input("💰 Bet amount:", min_value=0)
outcome = st.radio("🔁 Result:", ["Win", "Lose"])

# Log spin on button click
if st.button("Log Spin"):
    st.session_state.spins.append(spin)
    if outcome == "Win":
        st.session_state.balance += bet
    else:
        st.session_state.balance -= bet
    st.success(f"Spin {spin} logged! Current balance: €{st.session_state.balance}")

# Display logged spins
if st.session_state.spins:
    st.subheader("🧾 Spin History")
    df = pd.DataFrame({
        "Spin #": list(range(1, len(st.session_state.spins)+1)),
        "Number": st.session_state.spins
    })
    st.dataframe(df)

    # Basic prediction logic — show most frequent recent numbers
    st.subheader("🔮 Prediction Insights")
    counts = pd.Series(st.session_state.spins).value_counts().head(5)
    st.write("Most frequent spins:")
    st.bar_chart(counts)

# Reset option
if st.button("Reset App"):
    st.session_state.spins = []
    st.session_state.balance = 0
    st.info("Session reset.")

# 🔁 European wheel in physical layout
wheel_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# 🧠 Session state setup
if "spins" not in st.session_state:
    st.session_state.spins = []
if "predictions" not in st.session_state:
    st.session_state.predictions = []
if "balance" not in st.session_state:
    st.session_state.balance = None
if "outcomes" not in st.session_state:
    st.session_state.outcomes = []

# 🔧 Logic helpers
def get_neighbors(num):
    idx = wheel_order.index(num)
    return [
        wheel_order[(idx - 2) % len(wheel_order)],
        wheel_order[(idx - 1) % len(wheel_order)],
        wheel_order[(idx + 1) % len(wheel_order)],
        wheel_order[(idx + 2) % len(wheel_order)],
        wheel_order[(idx - 18) % len(wheel_order)],
        wheel_order[(idx + 18) % len(wheel_order)]
    ]

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
    base = get_neighbors(last)
    hot = get_hot(spins)
    trend = get_trend(spins)
    result = list(dict.fromkeys(base + [hot] + ([trend] if trend else [])))
    return result[:8]

# 🖼️ UI Section
st.markdown("<h4 style='text-align:center;'>108Spin Predictor</h4>", unsafe_allow_html=True)
st.caption("⚙️ European Wheel | Strategy Mode | Predictive Tracker")

# 🎯 Balance Input
if st.session_state.balance is None:
    starting = st.number_input("Enter starting balance (units)", min_value=1, step=1)
    if st.button("Set Balance"):
        st.session_state.balance = starting
        st.success(f"🔢 Starting balance set to {starting} units.")

# 🔄 Spin Logging
if st.session_state.balance is not None and len(st.session_state.spins) < 108:
    new_spin = st.number_input("Enter new spin (0–36)", min_value=0, max_value=36, step=1)
    if st.button("Log Spin"):
        st.session_state.spins.append(new_spin)
        spin_num = len(st.session_state.spins)
        st.success(f"🎯 Spin {spin_num}: {new_spin} logged.")

        if spin_num >= 12:
            prediction = predict_next(st.session_state.spins)
            st.session_state.predictions.append(prediction)
            st.info(f"🔮 Suggested bet for Spin {spin_num + 1}: {prediction}")

# 💰 Outcome Tracker
if len(st.session_state.predictions) > 0:
    st.subheader("💸 Outcome Logging")
    last_prediction = st.session_state.predictions[-1]
    result_spin = st.number_input("Enter result of predicted spin", min_value=0, max_value=36, step=1)
    if st.button("Check Outcome"):
        if result_spin in last_prediction:
            win_amount = 36  # payout for 1 unit straight bet
            st.session_state.balance += win_amount
            st.session_state.outcomes.append(("Win", result_spin, st.session_state.balance))
            st.success(f"✅ WIN! Balance now: {st.session_state.balance} units")
        else:
            loss_amount = len(last_prediction)  # assume 1 unit per number
            st.session_state.balance -= loss_amount
            st.session_state.outcomes.append(("Loss", result_spin, st.session_state.balance))
            st.error(f"❌ Loss. Balance now: {st.session_state.balance} units")

# 📦 Session Summary
if st.session_state.balance is not None:
    st.markdown("---")
    st.subheader("📈 Current Session")
    st.metric("Spins Logged", len(st.session_state.spins))
    st.metric("Predictions Made", len(st.session_state.predictions))
    st.metric("Balance", f"{st.session_state.balance} units")

# 🧼 Reset Button
if st.button("🔄 Reset Entire Session"):
    st.session_state.spins = []
    st.session_state.predictions = []
    st.session_state.balance = None
    st.session_state.outcomes = []
    st.warning("Session reset. Ready to start fresh!")

# 🛑 Session Cap
if len(st.session_state.spins) >= 108:
    st.success("✅ 108 spins completed! Session full.")
