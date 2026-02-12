# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

# Get active Snowflake session
session = get_active_session()

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
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders 
            (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon='👍')
    else:
        st.warning("Please enter a name and choose ingredients.")
