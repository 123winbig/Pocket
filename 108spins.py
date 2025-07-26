import random

# European roulette wheel in physical wheel order
wheel_order = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]

# Store spins and predictions
spins = []
predictions = []

# Helper to get geometric neighbors
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

# Hot number logic
def get_hot(spins):
    freq = {num: spins.count(num) for num in set(spins)}
    return max(freq, key=freq.get)

# Trend logic (based on average movement)
def get_trend(spins):
    if len(spins) < 3:
        return None
    last_idxs = [wheel_order.index(s) for s in spins[-3:]]
    avg_idx = int(sum(last_idxs) / 3)
    return wheel_order[avg_idx]

# Main prediction engine
def predict_next(spins):
    last = spins[-1]
    base_numbers = get_neighbors(last)
    hot = get_hot(spins)
    trend = get_trend(spins)
    suggested = base_numbers + [hot]
    if trend:
        suggested.append(trend)
    return list(dict.fromkeys(suggested))[:8]

# User-driven spin logging
def log_spin(num):
    if num not in wheel_order:
        print(f"Invalid number: {num}")
        return
    spins.append(num)
    print(f"Logged Spin {len(spins)} → {num}")
    if len(spins) >= 12:
        bet = predict_next(spins)
        predictions.append(bet)
        print(f"🔮 Suggested Bet for Spin {len(spins)+1}: {bet}")
    else:
        print(f"🕒 Waiting for 12 spins... ({12 - len(spins)} to go)")

# Optional simulator
def simulate_session():
    for _ in range(108):
        next_spin = random.choice(wheel_order)
        log_spin(next_spin)

# Run interactively (example)
if __name__ == "__main__":
    while len(spins) < 108:
        try:
            entry = input(f"Enter Spin {len(spins)+1} (0–36): ")
            log_spin(int(entry))
        except ValueError:
            print("⚠️ Please enter a valid number.")
