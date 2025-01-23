# Import Python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Title and description for the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custom Smoothie!
    """
)

# User input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ', name_on_order)

# Get Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark dataframe to a Pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

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
