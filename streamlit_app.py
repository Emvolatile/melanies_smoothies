import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Streamlit title and description
st.title('🍹 Customize Your Smoothie!')
st.write("Choose the fruits you want in your custom Smoothie!")

# User input for smoothie name
name_on_order = st.text_input('Name your Smoothie:')
if name_on_order:
    st.write(f'The name on your Smoothie will be: {name_on_order}')

# Get Snowflake session and data (mocked here for illustration)
mock_data = {
    'FRUIT_NAME': ['Apple', 'Blueberries', 'Jack Fruit', 'Raspberries', 'Strawberries'],
    'SEARCH_ON': ['Apple', 'Blueberry', 'Jackfruit', 'Raspberry', 'Strawberry']
}
pd_df = pd.DataFrame(mock_data)  # Replace this with actual Snowflake data fetching

# User input for selecting fruits
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df['FRUIT_NAME'],
    max_selections=5
)

# Process selected fruits
if ingredients_list:
    for fruit_chosen in ingredients_list:
        # Find the search_on value
        search_on = "Not found"  # Default value for missing data
        if not pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].empty:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]

        # Display the search value sentence
        st.write(f"The search value for {fruit_chosen} is {search_on} .")

        # Nutrition information header
        st.subheader(f"{fruit_chosen} Nutrition Information")

        # API request for nutrition data
        try:
            smoothiefoot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
            smoothiefoot_response.raise_for_status()
            sf_df = pd.DataFrame(smoothiefoot_response.json())
            st.dataframe(sf_df)
        except requests.exceptions.RequestException as e:
            st.write("error")
            st.write(f"Not found")  # Mimic the "Not Found" row in the table
