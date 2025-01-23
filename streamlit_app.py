import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title('🍹 Customize Your Smoothie!')
st.write("Choose the fruits you want in your custom Smoothie!")

# User input for smoothie name
name_on_order = st.text_input('Name your Smoothie:')
st.write(f'The name on your Smoothie will be: {name_on_order}')

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)  # Debug: Display the DataFrame

# User selects fruits for ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df['FRUIT_NAME'],
    max_selections=5
)

if ingredients_list:
    for fruit_chosen in ingredients_list:
        # Normalize text for matching
        fruit_chosen = fruit_chosen.strip().lower()
        pd_df['FRUIT_NAME'] = pd_df['FRUIT_NAME'].str.lower()
        
        # Safely access SEARCH_ON column
        if not pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].empty:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        else:
            search_on = "Not Found"
            st.write(f"No matching fruit found for: {fruit_chosen}")

        # Output fruit info
        st.subheader(f"{fruit_chosen.capitalize()} Nutrition Information")
        try:
            smoothiefoot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
            smoothiefoot_response.raise_for_status()
            sf_df = pd.DataFrame(smoothiefoot_response.json())
            st.dataframe(sf_df)
        except requests.exceptions.RequestException as e:
            st.write(f"Error fetching data for {fruit_chosen}: {e}")
