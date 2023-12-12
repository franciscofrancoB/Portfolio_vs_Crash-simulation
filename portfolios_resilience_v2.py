# -*- coding: utf-8 -*-
"""SCS_V4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GzkDYkzfQou3YkObm8ncVKIbDHZ5vtLB
"""

# REAL ESTATE
def realestate(T, t_crash1, t_crash2, crash_length1, crash_length2):
    # Parameters for the initial simulation
    sigma = 0.01     # volatility
    dt = 1                           # time step representing 1 trading day
    S0 = 100                         # initial price

    # Parameters for the crash simulation
    sigma_crash = 0.02                         # increased volatility during the crash

    # Mean-reversion parameters
    mean_reversion = 0.01                        # strength of mean reversion
    mean_level = S0*1.07                      # mean level for mean reversion
    mean_level_crash = mean_level*0.9         # mean level for mean reversion in crash

    # Initialize empty vectors
    S = np.zeros(T)
    S[0] = S0
    i = 0; j = 0;
    # -----Simulate initial stock price using Geometric Brownian Motion with mean reversion----
    for t in range(T-1):
        if t>=t_crash1[0] and t<t_crash1[1]: # During market crash nr.1
            z = np.random.normal(0,1)  # random numbers
            mean_reversion_component = mean_reversion * (mean_level_crash - S[t])
            S[t+1] = S[t]+ mean_reversion_component * dt + sigma_crash *S[t]* np.sqrt(dt) * z

        elif t>=t_crash2[0] and t<t_crash2[1]: # During market crash nr.2
            z = np.random.normal(0,1)  # random numbers
            mean_reversion_component = mean_reversion * (mean_level_crash - S[t])
            S[t+1] = S[t]+ mean_reversion_component * dt + sigma_crash *S[t]* np.sqrt(dt) * z

        else: # recovery period
            z = np.random.normal(0, 1)  # random numbers
            mean_reversion_component = mean_reversion * (mean_level - S[t])
            S[t+1] = S[t] + mean_reversion_component * dt + sigma * S[t] * np.sqrt(dt) * z

    # ---plotting---
    #plt.plot(range(T), S, 'k-', linewidth=1, label='Housing market Price')

    # Highlight the crash period with a red vertical line
    #plt.axvline(x=int(t_crash1[0]), color='r', linestyle='-.', label='Start of Crash')
    #plt.axvline(x=int(t_crash1[1]), color='r', linestyle='--', label='End of Crash')

    #plt.axvline(x=int(t_crash2[0]), color='r', linestyle='-.')
    #plt.axvline(x=int(t_crash2[1]), color='r', linestyle='--')

    #plt.title('Simulated GBM & EMM with Mean Reversion for Real estate market with Market Crash')
    #plt.xlabel('Time (Days)')
    #plt.ylabel('Market Price')
    #plt.legend()
    #plt.show();
    return (S);

#### Stocks #####
def simulate_gbm(S0, mu, sigma, T, dt):
    """
    Simulate Geometric Brownian Motion trajectories.

    :param S0: Initial stock price
    :param mu: Annualized expected return
    :param sigma: Annualized volatility
    :param T: Duration time horizon in years
    :param dt: Time step in years
    :return: Simulated GBM path
    """
    N = int(T / dt)  # Number of time steps
    t = np.linspace(0, T, N)  # Time vector
    W = np.random.standard_normal(size = N)  # Wiener process (Brownian motion)
    W = np.cumsum(W) * np.sqrt(dt)  # Cumulative sum of Wiener increments
    S = S0 * np.exp((mu - 0.5 * sigma ** 2) * t + sigma * W)  # GBM formula
    return S, t


def stock_crash_sim(T, start_crash1, start_crash2, crash_length1, crash_length2):
  # T: Total time in days
  # start_crash1 : start of crash 1
  # start_crash2 : start of crash 2
  # crash type :
  #   P1 : 2 shorts crashes (40 days each)
  #   P2 : 2 long crashes (252 days each)
  #   P3 : 1 short 1 long
  #   P4 : 1 long 1 short


  # Parameters for the initial simulation
  #T = 1.0                      # time horizon (1 year)
  mu = 0.08/252                  # expected return
  sigma = 0.0136                # volatility
  num_trading_days = 252
  #dt = T / num_trading_days    # time step representing 1 trading day
  S0 = 100                     # initial stock price

  # Parameters for the crash simulation
  num_crash_days = crash_length1                   # number of days the crash lasts
  T_crash = num_crash_days / 252              # crash duration in terms of year fraction
  mu_crash = -0.10/num_crash_days             # negative drift during the crash, value-loosing-[%/year]
  sigma_crash = 0.0283                        # increased volatility during the crash
  t_start_crash1 = start_crash1/252
  t_start_crash2 = start_crash2/252
  t_end_crash1 = (start_crash1+crash_length1)/252
  t_end_crash2 = (start_crash2+crash_length2)/252
  # Combined time steps
  total_days = num_trading_days + crash_length1 + crash_length2
  t = np.linspace(0, T/252, T)

  S0 = 100    # initial stock price
  num_stocks = 20

  stocks_sim = []
  for s in range(num_stocks):
    # pre crash

    pre_crash_duration = start_crash1
    prices_pre_crash, _ = simulate_gbm(S0, mu, sigma, pre_crash_duration, 1)

    # crash1
    mu_crash1 = -0.3 / crash_length1
    crash1_duration = crash_length1
    S0_crash1 = prices_pre_crash[-1]  # Starting price for crash phase
    prices_crash_1, _ = simulate_gbm(S0_crash1, mu_crash1, sigma_crash, crash1_duration, 1)

    # between crash 1 and crash 2

    between_crash_duration = start_crash2 - (start_crash1 + crash_length1)
    mu_recovery1 = 0.10/252
    S0_between_crash = prices_crash_1[-1]
    prices_between_crash, _ = simulate_gbm(S0_between_crash, mu_recovery1, sigma, between_crash_duration, 1)

    # crash2
    mu_crash2 = -0.3/crash_length2
    crash2_duration = crash_length2
    S0_crash2 = prices_between_crash[-1]
    prices_crash_2, _ = simulate_gbm(S0_crash2, mu_crash2, sigma_crash, crash2_duration, 1)

    # after crash 2
    after_crash_duration = T - (start_crash2 + crash_length2)
    mu_recovery2 = 0.10/252
    S0_after_crash = prices_crash_2[-1]
    prices_after_crash, _ = simulate_gbm(S0_after_crash, mu_recovery2, sigma, after_crash_duration, 1)

    # Combine the results for the full trajectory
    full_trajectory = np.concatenate((prices_pre_crash, prices_crash_1, prices_between_crash, prices_crash_2, prices_after_crash ))
    stocks_sim.append(full_trajectory)

  stocks_sim_array = np.array(stocks_sim)


  # Plot
  #plt.figure(figsize=(12, 6))
  # Add the average line
  #average_stock_price = np.mean(stocks_sim_array.T, axis=1)
  #plt.plot(t, average_stock_price, 'k-', linewidth=4, label='Average Stock Price')
  # Highlight the crash period with a red vertical line
  #plt.axvline(x=t_start_crash1, color='r', label='Start of Crash1')
  #plt.axvline(x=t_end_crash1, color='r', linestyle='--', label='End of Crash1')
  #plt.axvline(x=t_start_crash2, color='r', label='Start of Crash2')
  #plt.axvline(x=t_end_crash2, color='r', linestyle='--', label='End of Crash2')
  #plt.legend()
  #plt.plot(t,stocks_sim_array.T)
  #plt.title('Simulated Geometric Brownian Motion for 20 Stocks with Market Crash')
  #plt.xlabel("Years")
  #plt.ylabel("Stock Price")
  #plt.show()


  return stocks_sim_array

# ---------------- Bonds ----------------
def getBonds(T, start_crash1, start_crash2, crash_length1, crash_length2):
    # This function will return Bonds graphs and a vector of the prices for each timestep, ready to be used for portfolios.

    # T: Total time in days (1 year)
    # start_crash1: Start of Crash1
    # start_crash2: Start of Crash2
    # crash_type: P1: 2 shorts crashes (40 days each)
    #             P2: 2 long crashes   (252 days each)
    #             P3: 1 short 1 long
    #             P4: 1 long 1 short




    # Constants and Parameters
    dt = 1                  # Time step (1 day)
    end_crash1 = start_crash1 + crash_length1  # End of Crash1
    end_crash2 = start_crash2 + crash_length2  # End of Crash2

    # Parameters for normal scenario
    a_normal = 0.1          # Speed of reversion
    b_normal = 0.01         # Long term mean level
    sigma_normal = 0.02     # Volatility
    r0 = 0.01               # Initial interest rate

    # Parameters for crash scenarios
    a_crash = 0.95          # Modified speed of reversion during crash
    b_crash = 0.07          # Modified long term mean level during crash
    sigma_crash = 0.07      # Increased volatility during crash

    # Total time steps
    N_total = int(T / dt)

    # Vasicek model functions
    def A(t, T, a):
        return (1 - np.exp(-a * (T - t))) / a

    def D(t, T, a, b, sigma):
        G = (b - ((sigma**2) / (2*a**2)))
        H = (((sigma**2) * (A(t, T, a)**2)) / (4*a))
        return G * (A(t, T, a) - (T-t)) - H

    def bond_price(A, D, rt):
        return np.exp(-A * rt + D)

    def simulate_interest_rate_path(r0, dt, N_total, start_crash1, start_crash2):
        rates = np.zeros(N_total)
        rates[0] = r0
        for t in range(1, N_total):
            if start_crash1 <= t < end_crash1 or start_crash2 <= t < end_crash2:
                a, b, sigma = a_crash, b_crash, sigma_crash
            else:
                a, b, sigma = a_normal, b_normal, sigma_normal

            Wt = np.random.normal() * np.sqrt(dt/T)
            dr = a * (b - rates[t-1]) * dt/T + sigma * Wt
            rates[t] = rates[t-1] + dr
        return rates

    sum_bond_prices = np.zeros(N_total)
    # Plotting bond prices
    #fig1, ax1 = plt.subplots(figsize=(12, 5))
    num_bonds = 10
    for _ in range(num_bonds):
        interest_rates = simulate_interest_rate_path(r0, dt, N_total, start_crash1, start_crash2)
        bond_prices = np.array([bond_price(A(t*dt/T, T/T, a_normal),
                                        D(t*dt/T, T/T, a_normal, b_normal, sigma_normal), rt)
                                for t, rt in enumerate(interest_rates)])
        sum_bond_prices += bond_prices

        # Plot bonds
        #ax1.plot(range(N_total), bond_prices)

    #ax1.axvline(x=start_crash1, color='r', linestyle='--', label='Start of Crash 1')
    #ax1.axvline(x=end_crash1, color='r', linestyle=':', label='End of Crash 1')
    #ax1.axvline(x=start_crash2, color='g', linestyle='--', label='Start of Crash 2')
    #ax1.axvline(x=end_crash2, color='g', linestyle=':', label='End of Crash 2')
    #ax1.set_title('Simulated Bond Prices Paths')
    #ax1.set_xlabel('Time (trading days)')
    #ax1.set_ylabel('Bond price')
    #ax1.legend()

    #plt.tight_layout()
    #plt.show()

    mean_bond_prices = sum_bond_prices / num_bonds
    return mean_bond_prices

#### Commodities #####
def simulate_gbm(S0, mu, sigma, T, dt):
    """
    Simulate Geometric Brownian Motion trajectories.

    :param S0: Initial stock price
    :param mu: Annualized expected return
    :param sigma: Annualized volatility
    :param T: Duration time horizon in years
    :param dt: Time step in years
    :return: Simulated GBM path
    """
    N = int(T / dt)  # Number of time steps
    t = np.linspace(0, T, N)  # Time vector
    W = np.random.standard_normal(size = N)  # Wiener process (Brownian motion)
    W = np.cumsum(W) * np.sqrt(dt)  # Cumulative sum of Wiener increments
    S = S0 * np.exp((mu - 0.5 * sigma ** 2) * t + sigma * W)  # GBM formula
    return S, t


def commodities_crash_sim(T, start_crash1, start_crash2, crash_length1, crash_length2):
  # T: Total time in days
  # start_crash1 : start of crash 1
  # start_crash2 : start of crash 2
  # crash type :
  #   P1 : 2 shorts crashes (40 days each)
  #   P2 : 2 long crashes (252 days each)
  #   P3 : 1 short 1 long
  #   P4 : 1 long 1 short


  # Parameters for the initial simulation
  #T = 1.0                      # time horizon (1 year)
  mu = 0.08/252                  # expected return
  sigma = 0.0136                # volatility
  num_trading_days = 252
  #dt = T / num_trading_days    # time step representing 1 trading day
  S0 = 100                     # initial stock price

  # Parameters for the crash simulation
  num_crash_days = crash_length1                   # number of days the crash lasts
  T_crash = num_crash_days / 252              # crash duration in terms of year fraction
  mu_crash = -0.10/num_crash_days             # negative drift during the crash, value-loosing-[%/year]
  sigma_crash = 0.0283                        # increased volatility during the crash
  t_start_crash1 = start_crash1/252
  t_start_crash2 = start_crash2/252
  t_end_crash1 = (start_crash1+crash_length1)/252
  t_end_crash2 = (start_crash2+crash_length2)/252
  # Combined time steps
  total_days = num_trading_days + crash_length1 + crash_length2
  t = np.linspace(0, T/252, T)

  S0 = 100    # initial stock price
  commodities = ["Gold","Crude oil","Silver","Copper","Natural Gas","Corn","Oat"]
  num_commodities = len(commodities)
  # sigma before crash
  vol_gold_before = 0.0143
  vol_crudeoil_before = 0.0223
  vol_silver_before = 0.0232
  vol_copper_before = 0.0201
  vol_naturalgas_before = 0.0268
  vol_corn_before = 0.0211
  vol_oat_before = 0.0206

    # sigma during crash
  vol_gold_after = 0.0188
  vol_crudeoil_after = 0.0471
  vol_silver_after = 0.0327
  vol_copper_after = 0.0356
  vol_nataralgas_after = 0.0411
  vol_corn_after = 0.0290
  vol_oat_after = 0.0287
  sigma = [vol_gold_before,vol_crudeoil_before,vol_silver_before,vol_copper_before,vol_naturalgas_before,vol_corn_before,vol_oat_before]
  sigma_crash = [vol_gold_after,vol_crudeoil_after,vol_silver_after,vol_copper_after,vol_nataralgas_after,vol_corn_after,vol_oat_after]

  commodities_sim = []
  for i,commodity in enumerate(commodities):
    # pre crash

    pre_crash_duration = start_crash1
    prices_pre_crash, _ = simulate_gbm(S0, mu, sigma[i], pre_crash_duration, 1)

    # crash1
    mu_crash1 = -0.3 / 252
    crash1_duration = crash_length1
    S0_crash1 = prices_pre_crash[-1]  # Starting price for crash phase
    prices_crash_1, _ = simulate_gbm(S0_crash1, mu_crash1, sigma_crash[i], crash1_duration, 1)

    # between crash 1 and crash 2

    between_crash_duration = start_crash2 - (start_crash1 + crash_length1)
    mu_recovery1 = 0.10/252
    S0_between_crash = prices_crash_1[-1]
    prices_between_crash, _ = simulate_gbm(S0_between_crash, mu_recovery1, sigma[i], between_crash_duration, 1)

    # crash2
    mu_crash2 = -0.3/252
    crash2_duration = crash_length2
    S0_crash2 = prices_between_crash[-1]
    prices_crash_2, _ = simulate_gbm(S0_crash2, mu_crash2, sigma_crash[i], crash2_duration, 1)

    # after crash 2
    after_crash_duration = T - (start_crash2 + crash_length2)
    mu_recovery2 = 0.10/252
    S0_after_crash = prices_crash_2[-1]
    prices_after_crash, _ = simulate_gbm(S0_after_crash, mu_recovery2, sigma[i], after_crash_duration, 1)

    # Combine the results for the full trajectory
    full_trajectory = np.concatenate((prices_pre_crash, prices_crash_1, prices_between_crash, prices_crash_2, prices_after_crash ))
    commodities_sim.append(full_trajectory)

  commodities_sim_array = np.array(commodities_sim)


  # Plot
  #plt.figure(figsize=(12, 6))
  # Add the average line
  #average_commodities_price = np.mean(commodities_sim_array.T, axis=1)
  #plt.plot(t, average_commodities_price, 'k-', linewidth=4, label='Average Stock Price')
  # Highlight the crash period with a red vertical line
  #plt.axvline(x=t_start_crash1, color='r', label='Start of Crash1')
  #plt.axvline(x=t_end_crash1, color='r', linestyle='--', label='Start of Crash1')
  #plt.axvline(x=t_start_crash2, color='g', label='Start of Crash2')
  #plt.axvline(x=t_end_crash2, color='g', linestyle='--', label='Start of Crash2')

  #plt.plot(t,commodities_sim_array.T)
  #for i,commodity in enumerate(commodities):
  #  plt.plot(t, commodities_sim_array[i,:].T, label = commodity)
  #plt.title('Simulated Geometric Brownian Motion for Commodities with Market Crash')
  #plt.legend()
  #plt.xlabel("Years")
  #plt.ylabel("Commodity Price")
  #plt.show()

  return commodities_sim_array

#### Stocks #####
def simulate_gbm(S0, mu, sigma, T, dt):
    """
    Simulate Geometric Brownian Motion trajectories.

    :param S0: Initial stock price
    :param mu: Annualized expected return
    :param sigma: Annualized volatility
    :param T: Duration time horizon in years
    :param dt: Time step in years
    :return: Simulated GBM path
    """
    N = int(T / dt)  # Number of time steps
    t = np.linspace(0, T, N)  # Time vector
    W = np.random.standard_normal(size = N)  # Wiener process (Brownian motion)
    W = np.cumsum(W) * np.sqrt(dt)  # Cumulative sum of Wiener increments
    S = S0 * np.exp((mu - 0.5 * sigma ** 2) * t + sigma * W)  # GBM formula
    return S, t


def cash_crash_sim(T, start_crash1, start_crash2, crash_length1, crash_length2):
  # T: Total time in days
  # start_crash1 : start of crash 1
  # start_crash2 : start of crash 2
  # crash type :
  #   P1 : 2 shorts crashes (40 days each)
  #   P2 : 2 long crashes (252 days each)
  #   P3 : 1 short 1 long
  #   P4 : 1 long 1 short



  # Parameters for the initial simulation
  #T = 1.0                      # time horizon (1 year)
  mu = 0.6333 /100 /252             # expected return : average interest rate in 10 years from 2006 - 2016
  mu_crash = 0.6333 /100 /252       # expected return during crash :
  sigma = 0.0                   # volatility of cash  is zero
  #dt = T / num_trading_days    # time step representing 1 trading day
  S0 = 100                      # initial cash value

  # Parameters for the crash simulation
  sigma_crash = 0.0                           ## volatility of cash  is zero
  t_start_crash1 = start_crash1/252
  t_start_crash2 = start_crash2/252
  t_end_crash1 = (start_crash1+crash_length1)/252
  t_end_crash2 = (start_crash2+crash_length2)/252
  # Combined time steps
  t = np.linspace(0, T/252, T)

  S0 = 100    # initial stock price
  num_stocks = 1

  cash_sim = []
  for s in range(num_stocks):
    # pre crash

    pre_crash_duration = start_crash1
    prices_pre_crash, _ = simulate_gbm(S0, mu, sigma, pre_crash_duration, 1)

    # crash1
    crash1_duration = crash_length1
    S0_crash1 = prices_pre_crash[-1]  # Starting price for crash phase
    prices_crash_1, _ = simulate_gbm(S0_crash1, mu_crash, sigma_crash, crash1_duration, 1)

    # between crash 1 and crash 2

    between_crash_duration = start_crash2 - (start_crash1 + crash_length1)
    S0_between_crash = prices_crash_1[-1]
    prices_between_crash, _ = simulate_gbm(S0_between_crash, mu, sigma, between_crash_duration, 1)

    # crash2
    crash2_duration = crash_length2
    S0_crash2 = prices_between_crash[-1]
    prices_crash_2, _ = simulate_gbm(S0_crash2, mu_crash, sigma_crash, crash2_duration, 1)

    # after crash 2
    after_crash_duration = T - (start_crash2 + crash_length2)
    S0_after_crash = prices_crash_2[-1]
    prices_after_crash, _ = simulate_gbm(S0_after_crash, mu, sigma, after_crash_duration, 1)

    # Combine the results for the full trajectory
    full_trajectory = np.concatenate((prices_pre_crash, prices_crash_1, prices_between_crash, prices_crash_2, prices_after_crash ))
    cash_sim.append(full_trajectory)

  cash_sim_array = np.array(cash_sim)


  # Plot
  #plt.figure(figsize=(12, 6))
  # Add the average line
  #average_stock_price = np.mean(cash_sim_array.T, axis=1)
  #plt.plot(t, average_stock_price, 'k-', linewidth=4, label='Average Stock Price')
  # Highlight the crash period with a red vertical line
  #plt.axvline(x=t_start_crash1, color='r', label='Start of Crash1')
  #plt.axvline(x=t_end_crash1, color='r', linestyle='--', label='End of Crash1')
  #plt.axvline(x=t_start_crash2, color='r', label='Start of Crash2')
  #plt.axvline(x=t_end_crash2, color='r', linestyle='--', label='End of Crash2')
  #plt.legend()
  #plt.plot(t,cash_sim_array.T)
  #plt.title('Simulated Geometric Brownian Motion for cash with Market Crash')
  #plt.xlabel("Years")
  #plt.ylabel("Cash Value")
  #plt.show()


  return cash_sim_array

# ------------- Portfolio -------------
import numpy as np
import matplotlib.pyplot as plt
import math

# ------------- PARAMETERS ----------------
# -------General global variables-----------
crashtype = 'P1'                       # P1: short crashes, P2: long crashes, P3: first short, then long, P4: first long, then short
num_trading_days = 252                 # number of trading days per year
T = 10*num_trading_days                # time horizon (10 years)

# number of days the crash lasts
if crashtype == 'P1':     # short crashes
    crash_length = [40, 40]
    crash_color1 = 'red'
    crash_color2 = 'red'
    crash_label1 = r'Short-Term Crash Period'
    crash_label2 = r'Short-Term Crash Period'
elif crashtype == 'P2':   # long crashes
    crash_length = [252, 252]
    crash_color1 = 'darkorange'
    crash_label1 = r'Long-Term Crash Period'
    crash_color2 = 'darkorange'
    crash_label2 = r'Long-Term Crash Period'
elif crashtype == 'P3':   # 1 short 1 long crash
    crash_length = [40, 252]
    crash_color1 = 'red'
    crash_label1 = r'Short-Term Crash Period'
    crash_color2 = 'darkorange'
    crash_label2 = r'Long-Term Crash Period'
elif crashtype == 'P4':   # 1 short 1 long crash
    crash_length = [252, 40]
    crash_color1 = 'darkorange'
    crash_label1 = r'Long-Term Crash Period'
    crash_color2 = 'red'
    crash_label2 = r'Short-Term Crash Period'

# When the crashes occur.
t_crash1=[num_trading_days, int(num_trading_days+crash_length[0])]
t_crash2=[7*num_trading_days, int(7*num_trading_days+crash_length[1])]

# ------------- FUNCTIONS ----------------
commodities_prices = np.mean(commodities_crash_sim(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1]).T, axis=1)
cash_prices = cash_crash_sim(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1]).T.reshape(-1)
stock_prices = np.mean(stock_crash_sim(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1]).T, axis=1)
bond_prices = 100*getBonds(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1])
bond_prices += 100 - bond_prices[0]
real_estate_prices = realestate(T, t_crash1, t_crash2,  crash_length[0], crash_length[1])

wallet1 = 0.6  * bond_prices + 0.1  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
wallet2 = 0.35 * bond_prices + 0.35 * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
wallet3 = 0.2  * bond_prices + 0.5  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
wallet4 = 0.05 * bond_prices + 0.75 * stock_prices  + 0.05 * real_estate_prices  + 0.05 * cash_prices + 0.1  * commodities_prices


# Graph
plt.figure(figsize=(12, 5))
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'STIXGeneral'

plt.plot(range(len(bond_prices)), wallet1, color='blue', label=r'Conservative Portfolio')
plt.plot(range(len(bond_prices)), wallet2, color='green', label=r'Balanced Portfolio')
plt.plot(range(len(bond_prices)), wallet3, color='orange', label=r'Aggressive Portfolio')
plt.plot(range(len(bond_prices)), wallet4, color='red', label=r'Growth Portfolio')

# Highlighting the crash period
plt.axvspan(int(t_crash1[0]), int(t_crash1[1]), facecolor=crash_color1, alpha=0.35, label=crash_label1)
plt.axvspan(int(t_crash2[0]), int(t_crash2[1]), facecolor=crash_color2, alpha=0.35, label=crash_label2)

plt.xlabel(r'Trading Days', fontsize=12)
plt.xlim(0,2520)
plt.ylabel(r'Value', fontsize=12)
plt.title(f'Portfolio Values over {T} Trading Days (10 years)', fontsize=14)

# Adding a secondary x-axis to show years
ax2 = plt.gca().secondary_xaxis('top')
trading_days = np.arange(0, T+1, 252)
years = trading_days / 252
ax2.set_xticks(trading_days)
ax2.set_xticklabels([str(int(year)) for year in years])
ax2.set_xlabel('Years')

plt.legend()
plt.show()

# from tqdm import tqdm
# import numpy as np
# import matplotlib.pyplot as plt

# # ------------- PARAMETERS ----------------
# # -------General global variables-----------
# num_trading_days = 252                 # number of trading days per year
# T = 10 * num_trading_days              # time horizon (10 years)

# break_even_points = []

# crash_length_values = np.linspace(10, 600, 15).round().astype(int)

# for crash_length1 in tqdm(crash_length_values):
#     crash_length = [crash_length1 + 1, 1]

#     break_even_days_runs = []

#     # Run simulation 20 times for each crash_length1
#     for _ in range(100):
#         # Recalculate crash times within the loop
#         t_crash1 = [num_trading_days, int(num_trading_days + crash_length[0])]
#         t_crash2 = [9.5 * num_trading_days, int(9.5 * num_trading_days + crash_length[1])]

#         commodities_prices = np.mean(commodities_crash_sim(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1]).T, axis=1)
#         cash_prices = cash_crash_sim(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1]).T.reshape(-1)
#         stock_prices = np.mean(stock_crash_sim(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1]).T, axis=1)
#         bond_prices = 100 * getBonds(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1])
#         bond_prices += 100 - bond_prices[0]
#         real_estate_prices = realestate(T, t_crash1, t_crash2, crash_length[0], crash_length[1])

#         # Calculate wallet values
#         wallet1 = 0.6  * bond_prices + 0.1  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
#         wallet2 = 0.35 * bond_prices + 0.35 * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
#         wallet3 = 0.2  * bond_prices + 0.5  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
#         wallet4 = 0.05 * bond_prices + 0.75 * stock_prices  + 0.05 * real_estate_prices  + 0.05 * cash_prices + 0.1  * commodities_prices

#         # Find the day when wallet4 goes above wallet1 for the first time after the end of the crash
#         crash_end_day = num_trading_days + crash_length1
#         wallet4_above_wallet1_after_crash = np.where((wallet4 > wallet1) & (np.arange(T) > crash_end_day))[0]
#         if len(wallet4_above_wallet1_after_crash) > 0:
#             break_even_day = wallet4_above_wallet1_after_crash[0] - crash_end_day
#             break_even_days_runs.append(break_even_day)

#     # Calculate mean break-even day if there are valid break-even days
#     if break_even_days_runs:
#         mean_break_even_day = np.mean(break_even_days_runs)
#         break_even_points.append((crash_length1, mean_break_even_day))

# # Plotting
# crash_lengths, mean_break_even_days = zip(*break_even_points)  # Unzipping the list of tuples
# plt.scatter(crash_lengths, mean_break_even_days, marker='s', color='black')
# plt.plot(crash_lengths, mean_break_even_days, color='black')
# plt.xlabel('Crash Length (Trading Days)')
# plt.ylabel('Average Break Even Point (Days after Crash End)')
# plt.title('Average Break Even Points for Different Crash Lengths', fontsize=16)
# plt.show()

def calculate_recovery_time(wallet, crash_start, crash_end):
    pre_crash_value = wallet[crash_start - 1]
    recovery_time = None
    for j in range(crash_end, len(wallet)):
        if wallet[j] >= pre_crash_value:
            recovery_time = j - crash_end
            break
    return recovery_time

from tqdm import tqdm

# ------------- PARAMETERS ----------------
num_trading_days = 252                 # number of trading days per year
T = 10*num_trading_days                # time horizon (10 years)

# When the crashes occur.
t_crash1=[num_trading_days, int(num_trading_days+crash_length[0])]
t_crash2=[9.5*num_trading_days, int(9.5*num_trading_days+crash_length[1])]

recovery_times_wallet1 = []
recovery_times_wallet2 = []
recovery_times_wallet3 = []
recovery_times_wallet4 = []

# Number of simulations per crash length to average over
num_simulations = 100
crash_length_values = np.linspace(10, 2000, 40).round().astype(int)
for crash_length1 in tqdm(crash_length_values):
    avg_recovery_times = [0, 0, 0, 0]
    valid_simulations = [0, 0, 0, 0]

    for _ in range(num_simulations):
        crash_length = [crash_length1 + 1, 1]

        commodities_prices = np.mean(commodities_crash_sim(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1]).T, axis=1)
        cash_prices = cash_crash_sim(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1]).T.reshape(-1)
        stock_prices = np.mean(stock_crash_sim(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1]).T, axis=1)
        bond_prices = 100*getBonds(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1])
        bond_prices += 100 - bond_prices[0]
        real_estate_prices = realestate(T, t_crash1, t_crash2,  crash_length[0], crash_length[1])

        wallet1 = 0.6  * bond_prices + 0.1  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
        wallet2 = 0.35 * bond_prices + 0.35 * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
        wallet3 = 0.2  * bond_prices + 0.5  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
        wallet4 = 0.05 * bond_prices + 0.75 * stock_prices  + 0.05 * real_estate_prices  + 0.05 * cash_prices + 0.1  * commodities_prices

        # Calculate recovery times for each wallet
        recovery_times = [calculate_recovery_time(wallet, t_crash1[0], t_crash1[1]) for wallet in [wallet1, wallet2, wallet3, wallet4]]

        # Accumulate recovery times and count valid simulations
        for i in range(4):
            if recovery_times[i] is not None:
                avg_recovery_times[i] += recovery_times[i]
                valid_simulations[i] += 1

    # Append average recovery time for each wallet, adjusting for the number of valid simulations
    for i, recovery_times_wallet in enumerate([recovery_times_wallet1, recovery_times_wallet2, recovery_times_wallet3, recovery_times_wallet4]):
        if valid_simulations[i] > 0:
            avg_recovery_time = avg_recovery_times[i] / valid_simulations[i]
        else:
            avg_recovery_time = None  # Or some other placeholder if no valid simulations
        recovery_times_wallet.append((crash_length1, avg_recovery_time))

# Plotting
plt.figure(figsize=(10, 6))

for data, color, label, marker in [(recovery_times_wallet1, 'green', 'Conservative', 'o'),
                                   (recovery_times_wallet2, 'royalblue', 'Balanced', '^'),
                                   (recovery_times_wallet3, 'orange', 'Aggressive', 's'),
                                   (recovery_times_wallet4, 'red', 'Growth', 'D')]:
    if data:
        crash_lengths, recovery_days = zip(*data)
        plt.scatter(crash_lengths, recovery_days, color=color, label=label)
        plt.plot(crash_lengths, recovery_days, color=color)

plt.xlabel('Crash Duration (Trading Days)', fontsize=15)
plt.ylabel('Recovery Time (Trading Days)', fontsize=15)
plt.title('Recovery Times for Different Portfolios', fontsize=18)
plt.xlim(0, 1000)
plt.legend(title='Portfolio', fontsize=13)
plt.show()

plt.figure(figsize=(10, 6))

for data, color, label in [(recovery_times_wallet1[:20], 'blue', 'Conservative'),
                           (recovery_times_wallet2[:20], 'orange', 'Balanced'),
                           (recovery_times_wallet3[:20], 'green', 'Aggressive'),
                           (recovery_times_wallet4[:20], 'red', 'Growth')]:
    if data:
        crash_lengths, recovery_days = zip(*data)
        plt.scatter(crash_lengths, recovery_days, color=color, label=label)
        plt.plot(crash_lengths, recovery_days, color=color)

plt.xlabel('Crash Duration (Trading Days)', fontsize=15)
plt.ylabel('Recovery Time (Trading Days)', fontsize=15)
plt.title('Recovery Times for Different Portfolios', fontsize=18)
plt.xlim(0, 1000)
plt.legend(title='Portfolio', fontsize=13)
plt.show()

print(recovery_times_wallet1[:20])



import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# ------------- PARAMETERS ----------------
num_trading_days = 252                 # number of trading days per year
T = 10 * num_trading_days              # time horizon (10 years)

# Number of simulations per crash length to average over
num_simulations = 100
crash_length_values = np.linspace(10, 2000, 40).round().astype(int)

returns_wallet1 = []
returns_wallet2 = []
returns_wallet3 = []
returns_wallet4 = []

for crash_length1 in tqdm(crash_length_values):
    avg_returns = [0, 0, 0, 0]
    valid_simulations = [0, 0, 0, 0]

    for _ in range(num_simulations):
        crash_length = [crash_length1 + 1, 1]
        t_crash1 = [num_trading_days, num_trading_days + crash_length[0]]
        t_crash2 = [2519, 2519 + crash_length[1]]


        commodities_prices = np.mean(commodities_crash_sim(T, t_crash1[0], t_crash2[0], crash_length[0], crash_length[1]).T, axis=1)
        cash_prices = cash_crash_sim(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1]).T.reshape(-1)
        stock_prices = np.mean(stock_crash_sim(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1]).T, axis=1)
        bond_prices = 100*getBonds(T, t_crash1[0], t_crash2[0],  crash_length[0], crash_length[1])
        bond_prices += 100 - bond_prices[0]
        real_estate_prices = realestate(T, t_crash1, t_crash2,  crash_length[0], crash_length[1])

        wallet1 = 0.6  * bond_prices + 0.1  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
        wallet2 = 0.35 * bond_prices + 0.35 * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
        wallet3 = 0.2  * bond_prices + 0.5  * stock_prices  + 0.1  * real_estate_prices  + 0.1 * cash_prices  + 0.1 * commodities_prices
        wallet4 = 0.05 * bond_prices + 0.75 * stock_prices  + 0.05 * real_estate_prices  + 0.05 * cash_prices + 0.1  * commodities_prices

        # Calculate final returns for each wallet
        final_returns = [(wallet[-1] / wallet[0] - 1) * 100 for wallet in [wallet1, wallet2, wallet3, wallet4]]

        # Accumulate returns
        for i in range(4):
            avg_returns[i] += final_returns[i]
            valid_simulations[i] += 1

    # Append average returns for each wallet, adjusting for the number of valid simulations
    for i, avg_return in enumerate(avg_returns):
        avg_return /= valid_simulations[i]
        if i == 0:
            returns_wallet1.append((crash_length1, avg_return))
        elif i == 1:
            returns_wallet2.append((crash_length1, avg_return))
        elif i == 2:
            returns_wallet3.append((crash_length1, avg_return))
        elif i == 3:
            returns_wallet4.append((crash_length1, avg_return))

# Plotting
plt.figure(figsize=(10, 8))

for data, color, label, marker in [(returns_wallet1, 'green', 'Conservative', 'o'),
                                   (returns_wallet2, 'royalblue', 'Balanced', '^'),
                                   (returns_wallet3, 'orange', 'Aggressive', 's'),
                                   (returns_wallet4, 'red', 'Growth', 'D')]:
    if data:
        crash_lengths, returns = zip(*data)
        plt.scatter(crash_lengths, returns, color=color, label=label, marker=marker)
        plt.plot(crash_lengths, returns, color=color)

plt.xlabel('Crash Duration (Trading Days)', fontsize=15)
plt.ylabel('Final Return (%)', fontsize=15)
plt.title('Portfolio Returns vs. Crash Duration', fontsize=18)
plt.xlim(0, 2000)
plt.legend(title='Portfolio', fontsize=13)
plt.show()

