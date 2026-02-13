# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

st.title("🥤 Customize Your Smoothie! 🥤")

# ⚠️ DO NOT create a connection
# In SiS, session already exists

# -----------------------------
# ORDER ENTRY SECTION
# -----------------------------
st.subheader("Create a Smoothie Order")

name_on_order = st.text_input("Name on Smoothie:")

# Get fruit list from FRUIT_OPTIONS table
fruit_df = session.table("smoothies.public.fruit_options") \
    .select(col("FRUIT_NAME")) \
    .collect()

fruit_list = [row["FRUIT_NAME"] for row in fruit_df]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

if st.button("Submit Order"):
    if name_on_order and ingredients_list:
        ingredients_string = " ".join(ingredients_list)

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(name_on_order + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}" + name_on_order)
        sf_df = st.dataframe(data=smoothiesfroot_response.json(), use_container_width=True)


        insert_stmt = f"""
            INSERT INTO smoothies.public.orders 
            (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        

        session.sql(insert_stmt).collect()

        st.success("Your Smoothie is ordered!", icon="👍")

    else:
        st.warning("Please enter a name and choose ingredients.")


