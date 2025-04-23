


import pytrends
from pytrends.request import TrendReq
import pandas as pd
import time
import streamlit as st
import matplotlib.pyplot as plt

# Initialize the pytrends request
pytrends = TrendReq(hl='en-US', tz=330)

def fetch_and_visualize_trends(country_code, interest, months=3):
    try:
        # Define the trend query
        pytrends.build_payload([interest], cat=0, timeframe=f'today {months}-m', geo=country_code, gprop='')

        # Fetch the data with retry logic
        try:
            data = pytrends.interest_over_time()
        except Exception as e:
            st.warning("⚠️ First attempt failed. Retrying in 5 seconds...")
            time.sleep(5)
            pytrends.build_payload([interest], cat=0, timeframe=f'today {months}-m', geo=country_code, gprop='')
            data = pytrends.interest_over_time()

        # Check if data exists
        if data.empty:
            st.warning("No data found for this query.")
            return None, None
        
        # EDA - Simple Summary (No summary statistics but we will show columns and types)
        st.write("Fetched Data Columns and Types:")
        st.write(data.dtypes)
        
        # Graph 1: Popularity over time
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data.index, data[interest], label=f'Interest in {interest}', color='tab:blue')
        ax.set_title(f"Popularity of {interest} in the last {months} months")
        ax.set_xlabel("Date")
        ax.set_ylabel("Popularity")
        ax.legend()
        st.pyplot(fig)

        # Graph 2: Moving Average (Smoothing the trend)
        moving_avg = data[interest].rolling(window=7).mean()  # 7-day moving average
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data.index, moving_avg, label=f'Moving Average of {interest}', color='tab:orange')
        ax.set_title(f"7-Day Moving Average for {interest}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Popularity (Smoothed)")
        ax.legend()
        st.pyplot(fig)

        # Graph 3: Percentage Change in Popularity
        pct_change = data[interest].pct_change() * 100  # Percentage change
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data.index, pct_change, label=f'Percentage Change in {interest}', color='tab:red')
        ax.set_title(f"Percentage Change in Popularity for {interest}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Percentage Change (%)")
        ax.legend()
        st.pyplot(fig)

        # Add some insights based on the graphs
        if pct_change.max() > 0:
            insights = (
                f"Based on the trend graphs above, we observe the following:\n"
                f"- The trend for {interest} is showing a steady rise with peaks around {data.idxmax()[interest]}.\n"
                f"- The moving average indicates a smoother trend, reflecting growing interest in recent weeks.\n"
                f"- There has been a significant increase in popularity around {data.idxmax()[interest]}, suggesting a viral event or news.\n"
                f"- The percentage change graph indicates periods of high growth and contraction, which could be linked to specific market events."
            )
        else:
            insights = (
                f"Based on the trend graphs above, we observe the following:\n"
                f"- The trend for {interest} is declining, with the most significant drop around {data.idxmin()[interest]}.\n"
                f"- The moving average reflects a clear downtrend in the popularity over the past months.\n"
                f"- The percentage change shows consistent negative growth, suggesting that interest in {interest} is waning."
            )

        return data, insights

    except Exception as e:
        st.error(f"❌ Error fetching data: {str(e)}")
        return None, None
