import streamlit as st
import requests
import pandas as pd_df
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
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.write("DataFrame columns:", pd_df.columns)
#st.stop()

# User input for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        try:
            search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            st.subheader(fruit_chosen + ' Nutrition Information')
            smoothiefroot_response = requests.get("https://smoothiefroot.com/api/fruit/" + search_on)
            #smoothiefroot_response.raise_for_status()  # Raise an exception for bad responses
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        except requests.RequestException as e:
            st.error(f"Error fetching nutrition information for {fruit_chosen}: {e}")
        except KeyError:
            st.error(f"No search value found for {fruit_chosen}")



#if ingredients_list:
#    ingredients_string = ''

#    for fruit_chosen in ingredients_list:
#        ingredients_string += fruit_chosen + ' '

#        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#        st.write('The search value for ', fruit_chosen,' is ', SEARCH_ON, '.')

#        st.subheader(fruit_chosen + 'Nutrition Information')
#        smoothiefroot_response = requests.get("https://smoothiefroot.com/api/fruit/" + SEARCH_ON)
#        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
