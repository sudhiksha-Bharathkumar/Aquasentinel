import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard Configuration
st.set_page_config(page_title="NeerGap Vellore", layout="wide")
st.title("💧 AquaSentinel: NeerGap Vellore")
st.markdown("Predicting contamination risks and optimizing municipal relief during infrastructure transition gaps.")

# Load Synthetic Data (with .copy() so we don't overwrite the base cache)
@st.cache_data
def load_data():
    return pd.read_csv("vellore_wards.csv")
    
df = load_data().copy()

# Sidebar: Environmental Inputs
st.sidebar.header("Environmental & Resource Inputs")
rainfall = st.sidebar.slider("Daily Rainfall (mm)", 0, 100, 10)
test_kits = st.sidebar.number_input("Available Test Kits", min_value=0, max_value=100, value=20)
tankers = st.sidebar.number_input("Available Tanker Trips", min_value=0, max_value=50, value=5)

# --- WHAT-IF SIMULATION LOGIC ---
# Rainfall drives surface sewage ingress, specifically penalizing wards with high septic reliance
rainfall_penalty = (rainfall / 100) * df["Septic_Reliance_Pct"]
df["Risk_Score"] = (df["Risk_Score"] + rainfall_penalty).clip(upper=1.0)

# Recalculate Risk Levels dynamically so the map colors shift
df["Risk_Level"] = pd.cut(df["Risk_Score"], bins=[0, 0.3, 0.6, 1.1], labels=["Green", "Amber", "Red"], right=False)
df["Risk_Level"] = df["Risk_Level"].astype(str)

# --- MAIN DASHBOARD: TRIAGE MAP ---
st.subheader("Interim Ingress Risk Map")
color_map = {"Green": "#00CC96", "Amber": "#FFA15A", "Red": "#EF553B"}

fig = px.scatter_map(
    df, lat="Lat", lon="Lon", color="Risk_Level",
    size="Risk_Score", hover_name="Ward",
    hover_data={"Supply_Days_Per_Week": True, "Septic_Reliance_Pct": True, "Lat": False, "Lon": False},
    color_discrete_map=color_map, 
    zoom=11.5, 
    height=550,
    center={"lat": 12.915, "lon": 79.135}
)
fig.update_layout(map_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# --- GREEDY KNAPSACK OPTIMIZER ---
st.subheader("Triage Action Queue")

# 1. Sort wards by highest dynamic risk first
priority_df = df.sort_values(by="Risk_Score", ascending=False).copy()

# 2. Initialize tracking columns
priority_df["Tankers_Assigned"] = 0
priority_df["Test_Kits_Assigned"] = 0

remaining_tankers = tankers
remaining_kits = test_kits

# 3. Allocate resources greedily based on the simulated scenario
for index, row in priority_df.iterrows():
    if row["Septic_Reliance_Pct"] > 0.6 and remaining_kits > 0:
        priority_df.at[index, "Test_Kits_Assigned"] = 1
        remaining_kits -= 1
        
    if row["Supply_Days_Per_Week"] <= 2 and remaining_tankers > 0:
        priority_df.at[index, "Tankers_Assigned"] = 1
        remaining_tankers -= 1
        
    if remaining_kits == 0 and remaining_tankers == 0:
        break

# 4. Display the prioritized deployment list
action_df = priority_df[(priority_df["Tankers_Assigned"] > 0) | (priority_df["Test_Kits_Assigned"] > 0)]

if action_df.empty:
    st.success("✅ No critical interventions required at current resource levels.")
else:
    st.dataframe(
        action_df[["Ward", "Risk_Level", "Risk_Score", "Tankers_Assigned", "Test_Kits_Assigned"]],
        use_container_width=True,
        hide_index=True
    )
    
    col1, col2 = st.columns(2)
    col1.metric("Unused Tankers", remaining_tankers, delta=f"-{tankers - remaining_tankers} Deployed", delta_color="inverse")
    col2.metric("Unused Test Kits", remaining_kits, delta=f"-{test_kits - remaining_kits} Deployed", delta_color="inverse")