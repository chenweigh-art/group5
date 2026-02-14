import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="Chi-Town Sentinel", layout="wide", page_icon="🛡️")
st.title("🛡️ Chicago Crime Analysis (2015-2024)")

# --- DATA LOADING (Optimized for Memory) ---
@st.cache_data(show_spinner="Connecting to Sentinel Data Stream...")
def load_data():
    path = "chicago_crime_train_2015_2024_processed.csv"
    
    if not os.path.exists(path):
        st.error(f"🚨 File '{path}' not found. Ensure Git LFS push finished.")
        return None
        
    try:
        # 1. FIX: Read only necessary columns to save RAM on Streamlit Cloud
        cols_to_use = ['Date', 'District', 'Primary Type', 'Arrest', 'Latitude', 'Longitude']
        df = pd.read_csv(path, usecols=cols_to_use, low_memory=False)
        
        # 2. FIX: Convert Date to datetime and handle the 2015-2024 range
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']) # Remove rows where date failed
        
        df['Year'] = df['Date'].dt.year.astype(int)
        df['Hour'] = df['Date'].dt.hour.astype(int)
        
        # Feature Engineering (from your notebook)
        df["Time_Period"] = df["Hour"].apply(
            lambda x: "Early Morning (0-6)" if 0<=x<6 else 
                    "Morning (6-12)" if 6<=x<12 else 
                    "Afternoon (12-18)" if 12<=x<18 else "Night (18-24)"
        )
        return df
    except Exception as e:
        st.error(f"Data Connection Error: {e}")
        return None

df = load_data()

if df is not None:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Sentinel Controls")
    # Dynamically set slider range based on actual data
    min_year, max_year = int(df['Year'].min()), int(df['Year'].max())
    year_range = st.sidebar.slider("Select Analysis Period", min_year, max_year, (min_year, max_year))
    
    # 3. FIX: Filter copy to avoid 'SettingWithCopy' warnings
    f_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📅 Temporal Trends", "🗺️ Spatial Study", "📊 Statistical Correlations"])

    with tab1:
        st.header("Temporal Trends & District Breakdown")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Yearly Crime Volume")
            # Using value_counts() as per your original logic
            y_counts = f_df['Year'].value_counts().sort_index().reset_index()
            y_counts.columns = ['Year', 'count']
            st.plotly_chart(px.bar(y_counts, x='Year', y='count', color='count', color_continuous_scale='Blues'), use_container_width=True)
        with c2:
            st.subheader("Top 15 Police Districts")
            d_counts = f_df['District'].value_counts().head(15).reset_index()
            d_counts.columns = ['District', 'count']
            st.plotly_chart(px.bar(d_counts, x='count', y='District', orientation='h', color_discrete_sequence=['navy']), use_container_width=True)

    with tab2:
        st.header("Geospatial Hotspots")
        # Sample for performance (important for the 1M row file)
        map_df = f_df.dropna(subset=['Latitude', 'Longitude']).sample(min(10000, len(f_df)))
        st.plotly_chart(px.scatter_mapbox(map_df, lat="Latitude", lon="Longitude", color="Primary Type",
                                        zoom=10, mapbox_style="carto-positron", height=600), use_container_width=True)

    with tab3:
        st.header("Arrest Efficiency & Significance")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Arrest Rate by Time Period")
            a_rate = f_df.groupby("Time_Period")["Arrest"].mean().reset_index()
            a_rate["Arrest %"] = a_rate["Arrest"] * 100
            st.plotly_chart(px.bar(a_rate, x="Time_Period", y="Arrest %", text_auto='.1f'), use_container_width=True)
        with col_b:
            st.subheader("Crime Type vs. Time Heatmap")
            # Logic from correlation.ipynb
            top_crimes = f_df["Primary Type"].value_counts().nlargest(10).index
            ct = pd.crosstab(f_df[f_df["Primary Type"].isin(top_crimes)]["Primary Type"], f_df["Time_Period"])
            st.plotly_chart(px.imshow(ct, text_auto=True, color_continuous_scale='YlOrRd'), use_container_width=True)

else:
    st.info("Awaiting data stream... Ensure Git LFS push to 'master' finished.")