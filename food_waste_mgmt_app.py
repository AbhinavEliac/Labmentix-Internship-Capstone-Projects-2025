import streamlit as st
import pandas as pd
import pandasql as psql
import numpy as np
import sqlite3 as s3
import plotly.express as px

# Creting File Source Dictionary
file_links = {
    "providers": "https://drive.google.com/file/d/1w0VNPxZAsOsR1El2i4VMRUfnHT8SYTeG/view?usp=drive_link",
    "receivers": "https://drive.google.com/file/d/1m23Wp5qLvmaOJRXU45rXRqLoLcBkPiGk/view?usp=drive_link",
    "food_listings": "https://drive.google.com/file/d/1UF5qZPSE1iMkF26gO3pqdOQXFCbrn_4G/view?usp=drive_link",
    "claims": "https://drive.google.com/file/d/1Ygz091ivERJnP0N4YDaJYw01rQ0k5aUm/view?usp=drive_link"
}

# Loading files as csv into Dataframes

try:
    providers_df = pd.read_csv(f"https://drive.google.com/uc?id={file_links['providers'].split('/d/')[1].split('/')[0]}")
except Exception as e:
    st.error(f"Error loading providers: {e}")

try:
    receivers_df = pd.read_csv(f"https://drive.google.com/uc?id={file_links['receivers'].split('/d/')[1].split('/')[0]}")
except Exception as e:
    st.error(f"Error loading providers: {e}")

try:
    food_listings_df = pd.read_csv(f"https://drive.google.com/uc?id={file_links['food_listings'].split('/d/')[1].split('/')[0]}")
except Exception as e:
    st.error(f"Error loading providers: {e}")

try:
    claims_df = pd.read_csv(f"https://drive.google.com/uc?id={file_links['claims'].split('/d/')[1].split('/')[0]}")
except Exception as e:
    st.error(f"Error loading providers: {e}")

# Connecting to SQLite database (creates file if not exists)
conn = s3.connect("food_waste.db")    

# Storing all DataFrames in SQL tables
providers_df.to_sql("providers", conn, if_exists = "replace", index = False)
receivers_df.to_sql("receivers", conn, if_exists = "replace", index = False)
food_listings_df.to_sql("food_listings", conn, if_exists = "replace", index = False)
claims_df.to_sql("claims", conn, if_exists = "replace", index = False)

def get_providers(conn):
    return pd.read_sql_query("SELECT * FROM providers", conn)

def get_receivers(conn):
    return pd.read_sql_query("SELECT * FROM receivers", conn)

def get_food_listings(conn):
    return pd.read_sql_query("SELECT * FROM food_listings", conn)

def get_claims(conn):
    return pd.read_sql_query("SELECT * FROM claims", conn)

st.title("Food Waste Management Application")

tab_names = ["Home", "Food Providers & Receivers", "Food Listings & Availability", "Claims & Distribution", "Analysis & Insights"]
tabs = st.tabs(tab_names)

with tabs[0]:
    st.title("Home")
    st.write("Welcome to the Food Waste Management Dashboard")

    # Getting counts
    provider_count = len(get_providers(conn))
    receiver_count = len(get_receivers(conn))
    food_listing_count = len(get_food_listings(conn))
    claims_count = len(get_claims(conn))

    # Displaying counts in colorful boxes
    col1, col2, col3, col4 = st.columns(4)
    box_style = "padding:20px;border-radius:10px;text-align:center;min-width:120px;"

    with col1:
        st.markdown(
            f"""
            <div style="background-color:#1abc9c;{box_style}">
                <h3 style="color:white;">Providers</h3>
                <h2 style="color:white;">{provider_count}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div style="background-color:#3498db;{box_style}">
                <h3 style="color:white;">Receivers</h3>
                <h2 style="color:white;">{receiver_count}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div style="background-color:#e67e22;{box_style}">
                <h3 style="color:white;">Food Listings</h3>
                <h2 style="color:white;">{food_listing_count}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""
            <div style="background-color:#9b59b6;{box_style}">
                <h3 style="color:white;">Claims</h3>
                <h2 style="color:white;">{claims_count}</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # Bar Charts
    st.markdown("### Provider & Receiver Types")
    bar1, bar2 = st.columns(2)
    with bar1:
        if "Type" in providers_df.columns:
            prov_type_counts = providers_df["Type"].value_counts().sort_values(ascending=False)
            st.bar_chart(prov_type_counts)
            st.caption("Providers by Type")
        else:
            st.info("No 'Type' column in providers data.")
    with bar2:
        if "Type" in receivers_df.columns:
            recv_type_counts = receivers_df["Type"].value_counts().sort_values(ascending=False)
            st.bar_chart(recv_type_counts)
            st.caption("Receivers by Type")
        else:
            st.info("No 'Type' column in receivers data.")

    # Pie Charts
    st.markdown("### Meal, Food, and Claim Status Distribution")
    pie1, pie2, pie3 = st.columns(3)

    with pie1:
        if "Meal_Type" in food_listings_df.columns:
            meal_counts = food_listings_df["Meal_Type"].value_counts()
            fig = px.pie(values=meal_counts.values, names=meal_counts.index, title="Meal Type")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No 'Meal_Type' column in food listings.")

    with pie2:
        if "Food_Type" in food_listings_df.columns:
            foodtype_counts = food_listings_df["Food_Type"].value_counts()
            fig = px.pie(values=foodtype_counts.values, names=foodtype_counts.index, title="Food Type")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No 'Food_Type' column in food listings.")

    with pie3:
        if "Status" in claims_df.columns:
            status_counts = claims_df["Status"].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, title="Claim Status")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No 'Status' column in claims data.")

    # try:
    #     st.write("Providers Table from SQL Database:")
    #     st.dataframe(get_providers(conn))
    #     st.write("Receivers Table from SQL Database:")
    #     st.dataframe(get_receivers(conn))
    #     st.write("Food Listings Table from SQL Database:")
    #     st.dataframe(get_food_listings(conn))
    #     st.write("Claims Table from SQL Database:")
    #     st.dataframe(get_claims(conn))
    # except Exception as e:
    #     st.error(f"Error fetching tables from SQL: {e}")



with tabs[1]:

    st.subheader("How many food providers and receivers are there in each city?")
    st.write("Number of Food Providers")
    query_1_a = '''
    SELECT City, COUNT(DISTINCT Name) AS provider_count
    FROM providers
    GROUP BY City
    '''
    fwmgmt_q_1 = pd.read_sql_query(query_1_a, conn)
    st.dataframe(fwmgmt_q_1)
    st.write("Number of Food Receivers")
    query_1_b = '''
    SELECT City, COUNT(DISTINCT Name) AS receiver_count
    FROM receivers
    GROUP BY City
    '''
    fwmgmt_q_1_b = pd.read_sql_query(query_1_b, conn)
    st.dataframe(fwmgmt_q_1_b)

    st.subheader("Which type of food provider (restaurant, grocery store, etc.) contributes the most food?")
    query_2 = '''
    SELECT Type, COUNT(DISTINCT Name) AS provider_count
    FROM providers
    GROUP BY Type
    ORDER BY provider_count DESC
    LIMIT 1
    '''
    fwmgmt_q_2 = pd.read_sql_query(query_2, conn)
    st.dataframe(fwmgmt_q_2)

    st.subheader("What is the contact information of food providers in a specific city?")
    city_name = st.text_input("Enter city name:")
    if city_name:
        try:
            query_2_b = f'''
            SELECT Name, Contact
            FROM providers
            WHERE City = '{city_name}'
            '''
            fwmgmt_q_2_b = pd.read_sql_query(query_2_b, conn)
            st.dataframe(fwmgmt_q_2_b)
        except Exception as e:
            st.error(f"No Data: {e}")

    st.subheader("Which receivers have claimed the most food?")
    query_4 = '''
    SELECT r.Name, COUNT(c.Food_ID) AS claims_count
    FROM receivers AS r
    JOIN claims AS c ON r.Receiver_ID = c.Receiver_ID
    GROUP BY r.Name
    ORDER BY claims_count DESC
    LIMIT 5
    '''
    fwmgmt_q_4 = pd.read_sql_query(query_4, conn)
    st.dataframe(fwmgmt_q_4)

with tabs[2]:
 
    st.subheader("What is the total quantity of food available from all providers?")
    query_5 = '''
    SELECT p.Name, SUM(f.Quantity) AS total_quantity
    FROM providers AS p
    JOIN food_listings AS f ON p.Provider_ID = f.Provider_ID
    GROUP BY p.Name
    ORDER BY total_quantity DESC
    '''
    fwmgmt_q_5 = pd.read_sql_query(query_5, conn)
    st.dataframe(fwmgmt_q_5)

    st.subheader("Which city has the highest number of food listings?")
    query_6 = '''
    SELECT Location, COUNT(*) AS listing_count
    FROM food_listings
    GROUP BY Location
    ORDER BY listing_count DESC
    LIMIT 1
    '''
    fwmgmt_q_6 = pd.read_sql_query(query_6, conn)
    st.dataframe(fwmgmt_q_6)

    st.subheader("What are the most commonly available food types?")
    query_7 = '''
    SELECT Food_Type, COUNT(*) AS type_count
    FROM food_listings
    GROUP BY Food_Type
    ORDER BY type_count DESC
    '''
    fwmgmt_q_7 = pd.read_sql_query(query_7, conn)
    st.dataframe(fwmgmt_q_7)

with tabs[3]:

    st.subheader("How many food claims have been made for each food item?")
    query_8 = '''
    SELECT f.Food_Name, COUNT(*) AS claims_count
    FROM food_listings AS f
    JOIN claims AS c ON f.Food_ID = c.Food_ID
    GROUP BY f.Food_Name
    ORDER BY claims_count DESC
    '''
    fwmgmt_q_8 = pd.read_sql_query(query_8, conn)
    st.dataframe(fwmgmt_q_8)

    st.subheader("Which provider has had the highest number of successful food claims?")
    query_9 = '''
    SELECT p.Name, COUNT(c.Claim_ID) AS claims_count
    FROM providers AS p
    JOIN food_listings AS f ON p.Provider_ID = f.Provider_ID
    JOIN claims AS c ON f.Food_ID = c.Food_ID
    WHERE c.Status = 'Completed'
    GROUP BY p.Name
    ORDER BY claims_count DESC
    LIMIT 1
    '''
    fwmgmt_q_9 = pd.read_sql_query(query_9, conn)
    st.dataframe(fwmgmt_q_9)

    st.subheader("What percentage of food claims are completed vs. pending vs. canceled?")
    query_10 = '''
    SELECT Status, COUNT(Status) * 100.0 / (SELECT COUNT(*) FROM claims) AS status_percentage
    FROM claims
    GROUP BY Status
    '''
    fwmgmt_q_10 = pd.read_sql_query(query_10, conn)
    st.dataframe(fwmgmt_q_10)

with tabs[4]:
 
    st.subheader("What is the average quantity of food claimed per receiver?")
    query_11 = '''
    SELECT AVG(claimed_quantity) AS average_claimed_quantity
    FROM (
        SELECT r.Receiver_ID, SUM(f.Quantity) AS claimed_quantity
        FROM receivers AS r
        JOIN claims AS c ON r.Receiver_ID = c.Receiver_ID
        JOIN food_listings AS f ON c.Food_ID = f.Food_ID
        WHERE c.Status = 'Completed'
        GROUP BY r.Receiver_ID
    ) AS subquery
    '''
    fwmgmt_q_11 = pd.read_sql_query(query_11, conn)
    st.dataframe(fwmgmt_q_11)

    st.subheader("Which meal type (breakfast, lunch, dinner, snacks) is claimed the most?")
    query_12 = '''
    SELECT f.Meal_Type, COUNT(c.Claim_ID) AS claims_count
    FROM food_listings AS f
    JOIN claims AS c ON f.Food_ID = c.Food_ID
    GROUP BY f.Meal_Type
    ORDER BY claims_count DESC
    LIMIT 1
    '''
    fwmgmt_q_12 = pd.read_sql_query(query_12, conn)
    st.dataframe(fwmgmt_q_12)

    st.subheader("What is the total quantity of food donated by each provider?")
    query_13 = '''
    SELECT p.Name, SUM(f.Quantity) AS total_donated
    FROM providers AS p
    JOIN food_listings AS f ON p.Provider_ID = f.Provider_ID
    JOIN claims AS c ON f.Food_ID = c.Food_ID
    GROUP BY p.Name
    ORDER BY total_donated DESC
    '''
    fwmgmt_q_13 = pd.read_sql_query(query_13, conn)
    st.dataframe(fwmgmt_q_13)

    