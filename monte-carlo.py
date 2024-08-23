import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dotenv import load_dotenv

warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

load_dotenv(".env")
PLOT = os.getenv("PLOT", False)

# Simulation Parameters
mean_r = 11.4  # Mean weekly return in R
stddev_r = 7.657675888  # Standard deviation of weekly returns in R
starting_balance = os.getenv(
    "STARTING_BALANCE", 10000
)  # Starting balance in dollars
fee_adjustment = 0.8  # Adjusting for 20% for trading fees and slippage
num_simulations = 1000  # Number of Monte Carlo simulations
num_weeks = os.getenv("NUM_WEEKS", 52)  # Number of weeks to simulate

# Initialize a DataFrame to hold the results
simulations = pd.DataFrame()

# Run the simulations, assuming R = 1% of account balance
RISK_PER_TRADE = 0.01
for i in range(num_simulations):
    weekly_returns = np.random.normal(mean_r, stddev_r, int(num_weeks))
    balance = float(starting_balance)
    balance_history = []
    for weekly_return in weekly_returns:
        r_dollars = (
            weekly_return * (balance * RISK_PER_TRADE)
        ) * fee_adjustment
        balance += r_dollars
        balance_history.append(balance)
    simulations[i] = balance_history

# Calculate summary statistics
final_balances = simulations.iloc[-1, :]
mean_final_balance = final_balances.mean()
median_final_balance = final_balances.median()
percentile_1st = final_balances.quantile(0.01)
percentile_5th = final_balances.quantile(0.05)
percentile_95th = final_balances.quantile(0.95)
percentile_99th = final_balances.quantile(0.99)

if PLOT:
    # Visualization: Histogram of final balances
    plt.figure(figsize=(10, 6))
    plt.hist(final_balances, bins=50, color="blue", edgecolor="black")
    plt.axvline(
        mean_final_balance,
        color="red",
        linestyle="dashed",
        linewidth=1,
        label=f"Mean: ${mean_final_balance:.2f}",
    )
    plt.axvline(
        median_final_balance,
        color="green",
        linestyle="dashed",
        linewidth=1,
        label=f"Median: ${median_final_balance:.2f}",
    )
    plt.axvline(
        percentile_1st,
        color="blue",
        linestyle="dashed",
        linewidth=1,
        label=f"1st Percentile: ${percentile_1st:.2f}",
    )
    plt.axvline(
        percentile_5th,
        color="orange",
        linestyle="dashed",
        linewidth=1,
        label=f"5th Percentile: ${percentile_5th:.2f}",
    )
    plt.axvline(
        percentile_95th,
        color="purple",
        linestyle="dashed",
        linewidth=1,
        label=f"95th Percentile: ${percentile_95th:.2f}",
    )
    plt.axvline(
        percentile_99th,
        color="brown",
        linestyle="dashed",
        linewidth=1,
        label=f"99th Percentile: ${percentile_99th:.2f}",
    )

    plt.title(
        f"Monte Carlo Simulation of Final Balances After {num_weeks} Weeks"
    )
    plt.xlabel("Final Balance ($)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()

    # Visualization: Simulation paths
    plt.figure(figsize=(12, 7))
    plt.plot(simulations, color="blue", alpha=0.1)
    plt.title(
        f"Monte Carlo Simulation of Account Balance Over {num_weeks} Weeks"
    )
    plt.xlabel("Week")
    plt.ylabel("Account Balance ($)")
    plt.show()

# Display summary statistics
print(f"Monte Carlo Simulation Results After {num_weeks} Weeks")
print(f"Starting Balance: ${starting_balance}")
print(f"Mean Final Balance: ${mean_final_balance:.2f}")
print(f"Median Final Balance: ${median_final_balance:.2f}")
print(f"1st Percentile (Extreme-Case): ${percentile_1st:.2f}")
print(f"5th Percentile (Worst-Case): ${percentile_5th:.2f}")
print(f"95th Percentile (Best-Case): ${percentile_95th:.2f}")
print(f"99th Percentile (Dream-Case): ${percentile_99th:.2f}")
