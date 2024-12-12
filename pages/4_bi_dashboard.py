import streamlit as st
import pandas as pd
import altair as alt
import json
import requests
import os
import base64
alt.data_transformers.enable("vegafusion")

# Load CSS file
def load_css():
    """Carga el archivo CSS en la aplicación de Streamlit."""
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def add_logo_to_header():
    """Agrega el logo al encabezado utilizando la clase definida en CSS."""
    logo_path = os.path.join("static", "riskova_logo.png")
    logo_base64 = get_base64_image(logo_path)
    st.markdown(
        f"""
        <style>
        [data-testid="stHeader"]::before {{
            background-image: url('data:image/png;base64,{logo_base64}');
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_base64_image(image_path):
    """Convierte una imagen local en un string Base64."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# load css file and add logo
load_css()
add_logo_to_header()

# Application title
st.title("BI Dashboard")

# Temporary file path for saving and loading datasets
TEMP_FILE_PATH = "dataset/dataset.csv"

# Check if the dataset is already loaded in the session state
if "data" not in st.session_state:
    try:
        # Attempt to load the dataset from the temporary file
        data = pd.read_csv(TEMP_FILE_PATH)
        st.session_state["data"] = data  # Store the dataset in session state
        st.info("Dataset loaded from the temporary file.")
    except FileNotFoundError:
        # If the file does not exist, notify the user and stop execution
        st.warning("No dataset has been loaded. Go back to 'Home' to upload the data.")
        st.stop()  # Stop further execution if no dataset is found

# Load the dataset from session state
data = st.session_state["data"]

#Date columns added to data
data["trans_date_trans_time"] = pd.to_datetime(data["trans_date_trans_time"], errors='coerce')
data['date'] = data["trans_date_trans_time"].dt.date
data['month'] = data["trans_date_trans_time"].dt.month_name()
data['year'] = data["trans_date_trans_time"].dt.year

# Display the first few rows of the dataset for user overview
st.write(data.head())
# Year filter contents
year_list = list(data["year"].dropna().unique())[::-1]
selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)

# Yearly summary metrics
year_transactions = data.loc[data['year'] == selected_year]['amt'].count()
year_legit_transactions = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 0)]['amt'].count()
year_fraud_transactions = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1)]['amt'].count()
year_transactions_amt = data.loc[data['year'] == selected_year]['amt'].sum()
year_legit_transactions_amt = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 0)]['amt'].sum()
year_fraud_transactions_amt = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1)]['amt'].sum()
avg_monthly_transactions = year_transactions/len(data.loc[data['year']==selected_year]['month'].unique())
avg_monthly_ftransactions = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1)].shape[0]
avg_monthly_tamount = data.loc[(data['year'] == selected_year)]['amt'].sum()/len(data.loc[data['year']==selected_year]['month'].unique())
avg_monthly_famount = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1)]['amt'].sum()/len(data.loc[data['year']==selected_year]['month'].unique())

# Yearly summary display
st.header(f'{selected_year} Summary', divider='gray')
col0, col1, col2, col3 = st.columns(4)

with col0:
    st.metric(label ="Total transactions", value = '{:,}'.format(year_transactions))
    st.metric(label =f"Total amount", value = str('$' + '{:,}'.format(round(year_transactions_amt/1000))) + 'k')

with col1:
    st.metric(label ="Legitimate", value = '{:,}'.format(year_legit_transactions))
    st.metric(label ="Legit. Amount", value =str('$' + '{:,}'.format(round(year_legit_transactions_amt/1000))) + 'k')

with col2:
    st.metric(label ="Fraudulent",value = '{:,}'.format(year_fraud_transactions))
    st.metric(label ="Fraud. Aumount", value =str('$' + '{:,}'.format(round(year_fraud_transactions_amt/1000))) + 'k')

with col3:
    st.metric(label ="Fraud/legit ratio (n)", value = '{:.2f}%'.format((year_fraud_transactions/year_legit_transactions)*100))
    st.metric(label ="Fraud/legit ratio ($)", value = '{:.2f}%'.format((year_fraud_transactions_amt/year_legit_transactions_amt)*100))

# Crate df for transactions
transactions_df = pd.DataFrame(data.loc[data['year']==selected_year].groupby(["date", "is_fraud"])['amt'].sum()).reset_index()

# Label mapping
label_mapping = {
    1: "Fraudulent",
    0: "Legitimate"}

# Custom colors
custom_colors = {
    "Legitimate": "#1f77b4",
    "Fraudulent": "#ff7f0e"}

# Apply mapping
transactions_df["custom_is_fraud"] = transactions_df["is_fraud"].map(label_mapping)

# Line chart
chart = (
    alt.Chart(transactions_df)
    .mark_line()
    .encode(
        x=alt.X("date:T", title="Transaction Date"),
        y=alt.Y("amt:Q", title="Transaction Amount (USD)"),
        color=alt.Color(
            "custom_is_fraud:N",
            scale=alt.Scale(domain=list(custom_colors.keys()), range=list(custom_colors.values())),
            legend=alt.Legend(title="Transaction Type"),
        ),
        tooltip=[
            alt.Tooltip("date:T", title="Date "),
            alt.Tooltip("amt:Q", title="Amount ($)", format="$,.2f"),
            alt.Tooltip("custom_is_fraud:N", title='Type')
            ]
        ,
    )
    .properties(width=700, height=400)
    .interactive()
)

# Display linechart
st.altair_chart(chart, use_container_width=True)

# Filter the dataframe based on selections
filtered_data = data.copy()

# month filter
month_list = list(data["month"].dropna().unique())[::-1]
selected_month = st.selectbox('Select a month',options=["All"] + month_list, index=len(year_list)-1)

# Apply filtering conditionally
if selected_month != "All":
    # Filter by both state and month
    filtered_data = filtered_data[filtered_data["month"] == selected_month]
    filtered_data = filtered_data.groupby(['month', 'state', 'is_fraud'])['amt'].sum().reset_index()

else:
    # Filter by state only
    filtered_data = filtered_data.groupby(['month', 'state', 'is_fraud'])['amt'].sum().reset_index()
    filtered_data['month'] = 'All'

# # Aggregated data
# aggregated_data = (
#     filtered_data.groupby(['state', 'is_fraud'], as_index=False)
#     .agg(total_amount=('amt', 'sum'))
# )

# URL of the GeoJSON data
url = "https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json"


@st.cache_data
def load_geojson(url):
    response = requests.get(url)
    return json.loads(response.text)

geojson_url = "https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json"
geojson_data = load_geojson(geojson_url)

# Add column with state id
us_states_df = pd.read_csv("https://gist.githubusercontent.com/dantonnoriega/bf1acd2290e15b91e6710b6fd3be0a53/raw/11d15233327c8080c9646c7e1f23052659db251d/us-state-ansi-fips.csv", skipinitialspace=True)
us_states_df.rename(columns= {"stname":"state_name", "st":"state_id", "stusps":"state"}, inplace=True)
filtered_data = filtered_data.merge(us_states_df, on='state', how='left')

# # Altair expects a simplified topology
from vega_datasets import data as v_data
us_states = alt.topo_feature(geojson_url, "states")

import streamlit as st

# Add a filter to toggle transaction type
transaction_type = st.selectbox("Select Transaction Type", ["Fraudulent", "Legitimate"], key="transaction_type")
is_fraud_filter = 1 if transaction_type == "Fraudulent" else 0

# Filter data based on selection
filtered_chart_data = filtered_data[filtered_data["is_fraud"] == is_fraud_filter]

# Create a single map
single_chart = alt.Chart(us_states).mark_geoshape(stroke='black', strokeWidth=0.1).encode(
    color=alt.Color(
        "amt:Q",
        scale=alt.Scale(domain=[0, filtered_chart_data[filtered_chart_data['is_fraud'] == is_fraud_filter]["amt"].max()], range=["#ffd7b5", "#ff7f0e"] if is_fraud_filter else ["#b5d7ff", "#1f77b4"]),
        title=f"Transaction Amount ($)", legend=alt.Legend(format="$,.0f")
    ),
    tooltip=[
        alt.Tooltip("state_name:N", title="State"),
        alt.Tooltip("amt:Q", title=f"{transaction_type} Amount ($)", format="$,.0f")
    ]
).transform_lookup(
    lookup="id",
    from_=alt.LookupData(filtered_chart_data, "state_id", ["state_name", "amt"])
).project(
    type="albersUsa"
).properties(
    title=f"{transaction_type} transactions by state - Year: {selected_year} | Month: {selected_month}",
    width=800,
    height=500
)

st.altair_chart(single_chart, use_container_width=True)


# state filter
state_list = list(data["state"].sort_values().dropna().unique())
selected_state = st.selectbox('Select a state', options=["All"]+ state_list, index=len(year_list)-1)

# state metrics
year_state_transactions = data.loc[(data['year'] == selected_year) & (data['state'] == selected_state)]['amt'].count()
year_state_legit_transactions = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 0) & (data['state'] == selected_state)]['amt'].count()
year_state_fraud_transactions = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1) & (data['state'] == selected_state)]['amt'].count()
year_state_transactions_amt = data.loc[(data['year'] == selected_year) & (data['state'] == selected_state)]['amt'].sum()
year_state_legit_transactions_amt = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 0) & (data['state'] == selected_state)]['amt'].sum()
year_state_fraud_transactions_amt = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1) & (data['state'] == selected_state)]['amt'].sum()

# state summary 
if selected_state != "All":
    st.subheader(f'{selected_state} {selected_year} Summary', divider='gray')
    col0, col1, col2, col3 = st.columns(4)
    
    with col0:
        st.metric(label =f"{selected_month[:3]}. {selected_year} transactions", value = '{:,}'.format(year_state_transactions))
        st.metric(label =f"Total amount", value = str('$' + '{:,}'.format(round(year_state_transactions_amt))))
    
    with col1:
        st.metric(label ="Legitimate", value = '{:,}'.format(year_state_legit_transactions))
        st.metric(label ="Legit. Amount", value =str('$' + '{:,}'.format(round(year_state_legit_transactions_amt))))
    
    with col2:
        st.metric(label ="Fraudulent",value = '{:,}'.format(year_state_fraud_transactions))
        st.metric(label ="Fraud. Aumount", value =str('$' + '{:,}'.format(round(year_state_fraud_transactions_amt))))
    
    with col3:
        st.metric(label ="Fraud/legit ratio (n)", value = '{:.2f}%'.format((year_state_fraud_transactions/year_state_legit_transactions)*100))
        st.metric(label ="Fraud/legit ratio ($)", value = '{:.2f}%'.format((year_state_fraud_transactions_amt/year_state_legit_transactions_amt)*100))