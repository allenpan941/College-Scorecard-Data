import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from statsmodels.formula.api import ols
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="US College Data Insights Dashboard", layout="wide")

@st.cache_data
def load_and_clean_data():
    try:
        # Added 'r' before strings to handle Windows backslashes correctly
        df2020 = pd.read_csv(r"D:\Work\Econometrics\College_Scorecard_Raw_Data_10032025\MERGED2020_21_PP.csv", low_memory=False)
        df2023 = pd.read_csv(r"D:\Work\Econometrics\College_Scorecard_Raw_Data_10032025\MERGED2023_24_PP.csv", low_memory=False)
        
        cols = ["UNITID", "INSTNM", "SAT_AVG", "MD_EARN_WNE_P10", "AVGFACSAL", "CONTROL", "UGDS_MEN"]
        cols2 = ["UNITID", "LATITUDE", "LONGITUDE"]
        
        # Merge datasets
        mysample = df2020[cols].merge(df2023[cols2], on="UNITID", how='left').copy()
        
        # Convert to numeric
        for col in cols[2:]:
            mysample[col] = pd.to_numeric(mysample[col], errors='coerce')
            
        # Drop rows where earnings are missing
        mysample = mysample.dropna(subset=['MD_EARN_WNE_P10'])
        mysample = mysample.rename(columns={"MD_EARN_WNE_P10": "Earnings"})
        
        # Map control types to English labels
        control_map = {1: "Public", 2: "Private Non-Profit", 3: "Private For-Profit"}
        mysample['School_Type'] = mysample['CONTROL'].map(control_map)
        
        return mysample
    except FileNotFoundError:
        st.error("Data files not found. Please ensure the CSV files exist at the specified paths.")
        return pd.DataFrame()

df = load_and_clean_data()

if not df.empty:
    # --- Sidebar Interaction ---
    st.sidebar.header("📊 Filter Console")
    
    # 1. School Type Filter
    selected_types = st.sidebar.multiselect(
        "Select Institution Type", 
        options=df['School_Type'].unique(), 
        default=df['School_Type'].unique()
    )

    # 2. SAT Score Range Filter
    # Dropping NaNs for min/max calculation to avoid errors
    valid_sat = df['SAT_AVG'].dropna()
    min_sat, max_sat = int(valid_sat.min()), int(valid_sat.max())
    sat_range = st.sidebar.slider("SAT Score Range", min_sat, max_sat, (min_sat, max_sat))

    # Execute Filtering
    filtered_df = df[
        (df['School_Type'].isin(selected_types)) & 
        (df['SAT_AVG'].between(sat_range[0], sat_range[1]) | df['SAT_AVG'].isna())
    ]

    # --- Main Page Display ---
    st.title("🎓 US College Academic Performance & Earnings Analysis")
    st.markdown("This dashboard explores how **SAT scores** and **faculty salaries** correlate with student earnings 10 years after entry, using **College Scorecard** data.")

    # Row 1: Key Metric Cards
    m1, m2, m3 = st.columns(3)
    m1.metric("Institutions Analyzed", f"{len(filtered_df):,}")
    m2.metric("Avg. Median Earnings", f"${filtered_df['Earnings'].mean():,.0f}")
    m3.metric("Max Earnings Level", f"${filtered_df['Earnings'].max():,.0f}")

    # Row 2: Interactive Charts
    tab1, tab2, tab3 = st.tabs(["📈 Correlation Analysis", "🗺️ Geographic Distribution", "🔬 Statistical Model"])

    with tab1:
        st.subheader("SAT Score vs. Earnings (10 Years Post-Entry)")
        fig = px.scatter(
            filtered_df, x="SAT_AVG", y="Earnings", 
            color="School_Type", hover_name="INSTNM",
            trendline="ols", 
            labels={"SAT_AVG": "Average SAT Score", "Earnings": "Median Annual Earnings ($)"},
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Earnings Distribution Across the US")
        
        # Filter rows for mapping
        map_cols = ['LATITUDE', 'LONGITUDE', 'Earnings', 'AVGFACSAL']
        map_df = filtered_df.dropna(subset=map_cols)
        
        if not map_df.empty:
            fig_map = px.scatter_mapbox(
                map_df, 
                lat="LATITUDE", 
                lon="LONGITUDE", 
                color="Earnings", 
                size="AVGFACSAL", 
                hover_name="INSTNM", 
                zoom=3,
                mapbox_style="carto-positron",
                height=600,
                color_continuous_scale=px.colors.sequential.Viridis,
                labels={"Earnings": "Earnings ($)", "AVGFACSAL": "Faculty Salary"}
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("Insufficient geographic or salary data available for the current filters.")
        

    with tab3:
        st.subheader("Multiple Linear Regression (OLS)")
        # Prepare data for model
        model_data = filtered_df.dropna(subset=['Earnings', 'SAT_AVG', 'AVGFACSAL', 'CONTROL'])
        
        if len(model_data) > 30:
            model = ols("Earnings ~ SAT_AVG + AVGFACSAL + C(CONTROL)", data=model_data).fit()
            
            # Display results
            col_res1, col_res2 = st.columns([1, 2])
            with col_res1:
                st.write("**Model Metrics:**")
                st.write(f"R-squared: `{model.rsquared:.3f}`")
                st.write(f"Adj. R-squared: `{model.rsquared_adj:.3f}`")
            with col_res2:
                st.write("**Parameter Interpretation:**")
                st.info("For every 1 point increase in SAT score, predicted earnings increase by approx. **${:.2f}**".format(model.params['SAT_AVG']))
            
            with st.expander("View Detailed Regression Report"):
                st.text(model.summary())
        else:
            st.warning("Sample size is too small for a robust regression analysis with current filters.")

    # Data Table Preview
    with st.expander("👀 View Filtered Raw Data"):
        st.dataframe(filtered_df.sort_values("Earnings", ascending=False))

else:
    st.info("Please ensure your data files are correctly loaded.")