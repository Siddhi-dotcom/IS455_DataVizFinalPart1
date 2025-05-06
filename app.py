import streamlit as st
import pandas as pd
import altair as alt
import ast

# Load dataset
df = pd.read_csv("all_pokemon_data.csv")  # Ensure this file is in the same folder as this script

# Parse stringified lists
df['types'] = df['types'].apply(ast.literal_eval)
df['primary_type'] = df['types'].apply(lambda x: x[0] if isinstance(x, list) and x else None)

st.title("Pokémon Stats Observatory")

# --- Visualization 1: Speed vs Attack for Top X Pokémon ---
st.header("1. Speed vs Attack for Top Pokémon (by Base Experience)")

top_x = st.slider("Select number of top Pokémon", min_value=10, max_value=150, value=100, step=10)
top_df = df.sort_values(by="base_experience", ascending=False).head(top_x)

scatter = alt.Chart(top_df).mark_circle(size=80).encode(
    x=alt.X('attack', title='Attack'),
    y=alt.Y('speed', title='Speed'),
    tooltip=['name', 'attack', 'speed', 'base_experience'],
    color='primary_type'
).properties(
    width=700,
    height=400,
    title=f"Top {top_x} Pokémon: Attack vs Speed"
)

st.altair_chart(scatter, use_container_width=True)

st.markdown("""
**What this chart shows:**  
This scatter plot visualizes the relationship between **Attack** and **Speed** for the top Pokémon ranked by **Base Experience**. Each point represents a Pokémon, color-coded by its primary type.

**Conclusion:**  
This chart helps visualize how top Pokémon balance attack and speed. Some Pokémon are strong in both, while others specialize. For example, within the top 150, Fighting and Fairy types have the highest average speed (≈129 and 122 respectively), while Ground and Grass types lead in average attack (≈140 and 132 respectively).
The slider allows users to explore how these dynamics shift as different numbers of high-experience Pokémon are included—highlighting the flexibility and depth in offensive team strategies.
""")

# --- Visualization 2: Interactive Filter by Type ---
st.header("2. Highest Base Experience Pokémon by Type")

# Dropdown to filter by type
selected_type = st.selectbox(
    "Select a primary Pokémon type to explore",
    sorted(df['primary_type'].dropna().unique())
)

filtered_df = df[df['primary_type'] == selected_type]
top_by_type = filtered_df.sort_values('base_experience', ascending=False).head(10)

bar_chart = alt.Chart(top_by_type).mark_bar().encode(
    x=alt.X('base_experience', title='Base Experience'),
    y=alt.Y('name', sort='-x', title='Pokémon Name'),
    tooltip=['name', 'base_experience']
).properties(
    width=700,
    height=400,
    title=f'Top Pokémon by Base Experience - Type: {selected_type.capitalize()}'
)

st.altair_chart(bar_chart, use_container_width=True)

st.markdown(f"""
**What this chart shows:**  
This interactive chart lets you select a Pokémon **type** and view the top Pokémon by **base experience** within that category. The bar chart dynamically updates based on your selection.

**Conclusion:**  
This chart highlights the top Pokémon by base experience within the selected type. For example, in the Bug type, Pokémon like Genesect, Pheromosa, and Buzzwole stand out with base experience above 270—marking them as rare and powerful compared to typical Bug-types.
It allows for quick comparisons across types to see which Pokémon are the strongest within their category and how base experience varies across the Pokémon universe
""")
