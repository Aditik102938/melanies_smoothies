# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# App title
st.title(":Cup_with_straw: Customize your smoothie! cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")

# Live preview text
if name_on_order:
    st.write(f"The name on your Smoothie will be: {name_on_order}")

# Snowflake session
session = get_active_session()

# Load fruit options
fruit_df = session.table("smoothies.public.fruit_options") \
                  .select(col("FRUIT_NAME"))

fruit_list = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# Ingredient selection
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Submit order
if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    if st.button("Submit Order"):
        session.sql(insert_stmt).collect()
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")

