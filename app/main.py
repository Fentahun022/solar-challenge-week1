# app/main.py

import streamlit as st
import pandas as pd
from utils import load_all_countries_data, create_comparison_boxplot, create_ghi_ranking_table, load_country_data, create_seaborn_boxplot
import plotly.express as px

# Page Configuration (set this as the first Streamlit command)
st.set_page_config(
    page_title="MoonLight Solar Analysis Dashboard",
    page_icon="☀️",
    layout="wide", # "centered" or "wide"
    initial_sidebar_state="expanded" # "auto", "expanded", "collapsed"
)

# --- Load Data ---
# Load data for all countries for comparative views
df_all_countries = load_all_countries_data()

# --- Sidebar ---
st.sidebar.title("🌍 MoonLight Energy Solutions")
st.sidebar.markdown("## Solar Investment Analysis")

page = st.sidebar.radio(
    "Navigate",
    ("Cross-Country Comparison", "Individual Country EDA", "About")
)
st.sidebar.markdown("---")
st.sidebar.info(
    "This dashboard presents an analysis of solar irradiance and environmental data "
    "to support strategic solar investments."
)

# --- Main Page Content ---

if page == "Cross-Country Comparison":
    st.header("📊 Cross-Country Solar Resource Comparison")
    st.markdown("Comparing key solar metrics across Benin, Sierra Leone, and Togo.")

    if df_all_countries.empty:
        st.warning("Could not load data for comparison. Please check data files.")
    else:
        # --- Metric Selection for Boxplot ---
        st.subheader("Metric Distribution Comparison")
        metrics_available = ['GHI', 'DNI', 'DHI', 'Tamb', 'TModA', 'TModB', 'RH', 'WS']
        # Filter for metrics actually present in the loaded data
        metrics_present = [m for m in metrics_available if m in df_all_countries.columns]

        if not metrics_present:
            st.info("No common metrics found in the loaded datasets for boxplot comparison.")
        else:
            selected_metric_boxplot = st.selectbox(
                "Select Metric for Boxplot:",
                options=metrics_present,
                index=metrics_present.index('GHI') if 'GHI' in metrics_present else 0, # Default to GHI
                help="Choose a metric to see its distribution across countries."
            )

            # --- Boxplot Display ---
            if selected_metric_boxplot:
                # Using Plotly for interactive plots
                boxplot_fig = create_comparison_boxplot(
                    df_all_countries,
                    selected_metric_boxplot,
                    f"{selected_metric_boxplot} Distribution by Country"
                )
                if boxplot_fig:
                    st.plotly_chart(boxplot_fig, use_container_width=True)
                else:
                    st.info(f"Could not generate boxplot for {selected_metric_boxplot}.")
            
                # # Alternative: Using Seaborn/Matplotlib (static image)
                # st.markdown("### Static Boxplot (Seaborn/Matplotlib)")
                # static_boxplot_fig = create_seaborn_boxplot(
                #     df_all_countries,
                #     selected_metric_boxplot,
                #     f"{selected_metric_boxplot} Distribution by Country (Static)"
                # )
                # st.pyplot(static_boxplot_fig)


        st.markdown("---")
        # --- Top Regions Table (GHI Ranking) ---
        st.subheader("☀️ Country Ranking by Average Daytime GHI")
        st.markdown("Countries ranked by their average Global Horizontal Irradiance (GHI) during daytime (GHI > 50 W/m²).")
        
        ranking_table_df = create_ghi_ranking_table(df_all_countries)
        if not ranking_table_df.empty:
            # Nicer display for the table
            st.dataframe(
                ranking_table_df.style.format({'Average Daytime GHI (W/m²)': "{:.2f}"})
                                 .highlight_max(subset=['Average Daytime GHI (W/m²)'], color='lightgreen')
                                 .set_properties(**{'font-size': '10pt', 'width': '200px'}),
                use_container_width=True
            )
        else:
            st.info("Could not generate GHI ranking table. Data might be missing or insufficient.")


elif page == "Individual Country EDA":
    st.header("🔍 Individual Country EDA Insights")
    
    country_options = ["Benin", "Sierra Leone", "Togo"]
    selected_country_eda = st.selectbox(
        "Select Country to Explore:",
        options=country_options,
        index=0,
        help="Choose a country to view its specific EDA highlights."
    )

    if selected_country_eda:
        st.markdown(f"### Exploring Data for: **{selected_country_eda}**")
        df_country = load_country_data(selected_country_eda)

        if df_country.empty:
            st.warning(f"Could not load data for {selected_country_eda}.")
        else:
            st.subheader("Data Overview")
            st.dataframe(df_country.head())
            
            st.subheader("Time Series of GHI")
            if 'GHI' in df_country.columns:
                # Simple line chart using Plotly Express
                fig_ts_ghi = px.line(df_country.reset_index(), x='Timestamp', y='GHI', # reset_index if Timestamp is index
                                     title=f'GHI Time Series for {selected_country_eda}')
                st.plotly_chart(fig_ts_ghi, use_container_width=True)
            else:
                st.info("GHI data not available for selected country.")

            # You can add more plots here specific to individual country EDA
            # For example, a histogram of a selected variable, or a wind rose if you implement it in utils
            st.subheader("Distribution of Ambient Temperature (Tamb)")
            if 'Tamb' in df_country.columns:
                fig_hist_tamb = px.histogram(df_country, x='Tamb', nbins=50,
                                             title=f'Ambient Temperature Distribution for {selected_country_eda}')
                st.plotly_chart(fig_hist_tamb, use_container_width=True)
            else:
                st.info("Tamb data not available for selected country.")


elif page == "About":
    st.header("ℹ️ About This Dashboard")
    st.markdown("""
    This dashboard was developed as part of the **MoonLight Energy Solutions - Solar Challenge Week 1**.
    
    **Objective:** To analyze solar irradiance and environmental data from Benin, Sierra Leone, and Togo
    to identify key trends and insights, supporting strategic decisions for solar investments.

    **Data Source:** Aggregated Solar Radiation Measurement Data.
    
    **Key Features:**
    - **Cross-Country Comparison:** Side-by-side visualization of key solar metrics.
    - **Individual Country EDA:** Basic exploration of data for each selected country.
    - **GHI Ranking:** A simple ranking of countries based on average daytime GHI.
    
    Built with **Streamlit** and **Plotly Express**.
    """)
    st.markdown("---")
    st.markdown("Developed by: **Fentahun Amare**")


# To run this app:
# 1. Navigate to your project root in the terminal (where 'app/' folder is)
# 2. Make sure your virtual environment is activated.
# 3. Run: streamlit run app/main.py