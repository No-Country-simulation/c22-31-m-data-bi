import streamlit as st
import pandas as pd
import os


# Load CSS file
def load_css():
    css_path = os.path.join("styles", "styles.css")
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load styles and text
load_css()



# Application title
st.title("BI Dashboard")

# Temporary file path for saving and loading datasets
TEMP_FILE_PATH = "data/dataset.csv"

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

# Sidebar filter
with st.sidebar:
    st.title('Filters')
    year_list = list(data["year"].dropna().unique())[::-1]
    month_list = list(data["month"].dropna().unique())[::-1]
    state_list = list(data["state"].sort_values().dropna().unique())
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    selected_month = st.selectbox('Select a month', month_list, index=len(year_list)-1)
    selected_state = st.selectbox('Select a state', state_list, index=len(year_list)-1)

# Yearly summary metrics
year_transactions = data.loc[data['year'] == selected_year]['amt'].count()
year_transactions_amt = data.loc[data['year'] == selected_year]['amt'].sum()
avg_monthly_transactions = year_transactions/len(data.loc[data['year']==selected_year]['month'].unique())
avg_monthly_ftransactions = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1)].shape[0]
avg_monthly_tamount = data.loc[(data['year'] == selected_year)]['amt'].sum()/len(data.loc[data['year']==selected_year]['month'].unique())
avg_monthly_famount = data.loc[(data['year'] == selected_year) & (data['is_fraud'] == 1)]['amt'].sum()/len(data.loc[data['year']==selected_year]['month'].unique())

print(data.loc[data['year']==selected_year]['month'].unique())

# Yearly summary display
st.header(f'{selected_year} Summary', divider='gray')
col0, col1, col2 = st.columns(3)

with col0:
    st.metric(label =f"Total transactions", value = '{:,}'.format(year_transactions))
    st.metric(label =f"Transacted amount", value = str('$' + '{:,}'.format(round(year_transactions_amt/1000))) + 'k')

with col1:
    st.metric(label ="Avg. monthly transactions", value = '{:,}'.format(round(avg_monthly_transactions)))
    st.metric(label ="Avg. monthly transacted amount", value = ('$' + '{:,}'.format(round(avg_monthly_tamount/1000))) + 'k')

with col2:
    st.metric(label = "Avg. fraudulent transactions", value= '{:,}'.format(avg_monthly_ftransactions))
    st.metric(label = "Avg. monthly fraudulent transacted amount", value = ('$' + '{:,}'.format(round(avg_monthly_famount/1000))) + 'k')

yearly_line_chart = data.loc[data['year']==selected_year].groupby("date")['amt'].sum()
st.line_chart(yearly_line_chart)
fyearly_line_chart = data.loc[(data['year']==selected_year) & (data['is_fraud']==1)].groupby("date")['amt'].sum()
st.line_chart(fyearly_line_chart)


