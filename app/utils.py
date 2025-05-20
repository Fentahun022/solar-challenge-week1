# app/utils.py

import pandas as pd
import streamlit as st
import os
import plotly.express as px # Using Plotly Express for interactivity
import seaborn as sns # Can still use seaborn/matplotlib if preferred
import matplotlib.pyplot as plt

# Cache data loading to improve performance
@st.cache_data # Use st.cache_data for data, st.cache_resource for non-data like ML models
def load_country_data(country_name):
    """Loads the cleaned data for a specific country."""
    filename_map = {
        "Benin": "benin_clean.csv",
        "Sierra Leone": "sierraleone_clean.csv",
        "Togo": "togo_clean.csv"
    }
    filename = filename_map.get(country_name)
    if not filename:
        return pd.DataFrame() # Return empty DataFrame if country name is invalid

    # Try to find the data directory relative to this utils.py file or from project root
    # This assumes app/ is one level down from the project root where data/ also is.
    
    # Path relative to the current file (utils.py inside app/)
    # So, ../data/filename
    data_dir_relative_to_app = os.path.join(os.path.dirname(__file__), '..', 'data')
    file_path_relative = os.path.join(data_dir_relative_to_app, filename)

    # Fallback: Path from project root (if app is run from project root, e.g. streamlit run app/main.py)
    data_dir_from_root = "data"
    file_path_from_root = os.path.join(data_dir_from_root, filename)

    file_path_to_load = None
    if os.path.exists(file_path_relative):
        file_path_to_load = file_path_relative
    elif os.path.exists(file_path_from_root):
        file_path_to_load = file_path_from_root
        
    if file_path_to_load:
        try:
            df = pd.read_csv(file_path_to_load, index_col='Timestamp', parse_dates=True)
            df['Country'] = country_name # Add country column for combined plots
            return df
        except FileNotFoundError:
            st.error(f"Error: Cleaned data file '{filename}' not found at '{file_path_to_load}'.")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Error loading data for {country_name}: {e}")
            return pd.DataFrame()
    else:
        st.error(f"Could not determine path for data file '{filename}'. Checked relative and root paths.")
        return pd.DataFrame()


@st.cache_data
def load_all_countries_data(country_list=["Benin", "Sierra Leone", "Togo"]):
    """Loads and combines data for all specified countries."""
    all_dfs = []
    for country in country_list:
        df = load_country_data(country)
        if not df.empty:
            all_dfs.append(df)
    
    if not all_dfs:
        return pd.DataFrame() # Return empty if no data could be loaded
        
    return pd.concat(all_dfs, ignore_index=False) # Keep original Timestamp index


def create_comparison_boxplot(df_combined, metric, title):
    """Creates a comparison boxplot using Plotly Express."""
    if df_combined.empty or metric not in df_combined.columns:
        return None
    fig = px.box(df_combined, x='Country', y=metric, color='Country',
                 title=title, labels={metric: f"{metric} (Units)"}) # Add units later
    fig.update_layout(title_x=0.5) # Center title
    return fig

def create_ghi_ranking_table(df_combined):
    """Creates a table ranking countries by average GHI."""
    if df_combined.empty or 'GHI' not in df_combined.columns:
        return pd.DataFrame() # Return empty DataFrame

    # Calculate mean GHI only during potential productive hours
    df_daytime = df_combined[df_combined['GHI'] > 50]
    if df_daytime.empty:
        return pd.DataFrame({"Message": ["No daytime GHI data (GHI > 50 W/m^2) available for ranking."]})

    avg_ghi = df_daytime.groupby('Country')['GHI'].mean().sort_values(ascending=False).reset_index()
    avg_ghi.rename(columns={'GHI': 'Average Daytime GHI (W/m²)'}, inplace=True)
    avg_ghi.index = avg_ghi.index + 1 # Start ranking from 1
    return avg_ghi

def create_seaborn_boxplot(df_combined, metric, title):
    """Creates a comparison boxplot using Seaborn (for static image if needed)."""
    if df_combined.empty or metric not in df_combined.columns:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Data not available", ha='center', va='center')
        return fig

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=df_combined, x='Country', y=metric, palette='Set2', ax=ax)
    unit = 'W/m²' if 'HI' in metric or 'Mod' in metric else '°C' if 'T' in metric else ''
    ax.set_title(title, fontsize=14)
    ax.set_ylabel(f'{metric} ({unit})', fontsize=12)
    ax.set_xlabel('Country', fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle=':', alpha=0.7, axis='y')
    return fig