# simulator.py

import streamlit as st
import random

# 🎲 Simulation Parameters
DEFAULT_BANKROLL = 1000
MAX_EXPOSURE = 500
BET_LEVELS = [1, 2, 3, 5, 7]

# 🔧 Core Functions
def get_hot_number(results):
    return max(set(results), key=results.count)

def get_trend_number(results):
    return sum(results[-5:]) // 5 if len(results) >= 5 else random.randint(0, 36)

def get_bet_numbers(result_history):
    core = []
    last = result_history[-1] if result_history else 18
    core += [(last + offset) % 37 for offset in [-2, -1, 1, 2, -18, 18]]
    hot = get_hot_number(result_history) if result_history else 18
    trend = get_trend_number(result_history) if result_history else 18
    return list(set(core + [hot, trend]))[:8]

def run_simulation(spin_data):
    bankroll = DEFAULT_BANKROLL
    history = []
    wins = 0
    units_won = 0
    units_lost = 0
    loss_streak = 0
    max_drawdown = 0

    for i, spin in enumerate(spin_data):
        bet_level = BET_LEVELS[min(loss_streak, len(BET_LEVELS) - 1)]
        numbers = get_bet_numbers(history)
        total_bet = bet_level * len(numbers)

        if bankroll - total_bet < (DEFAULT_BANKROLL - MAX_EXPOSURE):
            break  # Exposure limit hit

        if spin in numbers:
            win_amount = bet_level * 36
            bankroll += win_amount
            units_won += win_amount
            loss_streak = 0
            wins += 1
        else:
            bankroll -= total_bet
            units_lost += total_bet
            loss_streak += 1

        drawdown = DEFAULT_BANKROLL - bankroll
        if drawdown > max_drawdown:
            max_drawdown = drawdown

        history.append(spin)

    return {
        'final_bankroll': bankroll,
        'win_rate': f"{(wins/len(history))*100:.1f}%",
        'units_won': units_won,
        'units_lost': units_lost,
        'drawdown': max_drawdown,
        'hot_efficiency': f"{get_hot_number(history)}",
        'trend_efficiency': f"{get_trend_number(history)}",
        'spins_run': len(history)
    }

# 🖥️ Streamlit UI
st.set_page_config(page_title="Roulette Simulator", layout="centered")
st.title("🎰 Roulette Strategy Simulator")
st.caption("Powered by custom logic + betting progression")

spin_input = st.text_area("Enter 108 spin results separated by commas (e.g. 12,34,7,...)", height=150)

if spin_input:
    try:
        spin_data = [int(n.strip()) % 37 for n in spin_input.split(",") if n.strip().isdigit()]
        if len(spin_data) < 20:
            st.warning("Please enter at least 20 spins for meaningful simulation.")
        else:
            result = run_simulation(spin_data)

            st.subheader("📊 Simulation Results")
            st.metric("Final Bankroll", f"{result['final_bankroll']} units")
            st.metric("Win Rate", result['win_rate'])
            st.metric("Units Won", result['units_won'])
            st.metric("Units Lost", result['units_lost'])
            st.metric("Max Drawdown", f"{result['drawdown']} units")
            st.metric("Hot Number Selected", result['hot_efficiency'])
            st.metric("Trend Number Avg", result['trend_efficiency'])
            st.metric("Total Spins Simulated", result['spins_run'])

    except Exception as e:
        st.error(f"Error parsing input: {e}")
else:
    st.info("Paste 108 numbers and click run to simulate your strategy!")
