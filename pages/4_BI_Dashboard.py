import streamlit as st
import pandas as pd

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

# Display the first few rows of the dataset for user overview
st.write(data.head())

# chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
# st.bar_chart(chart_data)

with st.sidebar:
    st.title('Filters')
    data["trans_date_trans_time"] = pd.to_datetime(data["trans_date_trans_time"], errors='coerce')
    year_list = list(data["trans_date_trans_time"].dt.year.dropna().unique())[::-1]
    month_list = list(data["trans_date_trans_time"].dt.month_name().dropna().unique())[::-1]
    state_list = list(data["state"].sort_values().dropna().unique())
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    selected_month = st.selectbox('Select a month', month_list, index=len(year_list)-1)
    selected_state = st.selectbox('Select a state', state_list, index=len(year_list)-1)
    df_selected_year = data[data["trans_date_trans_time"].dt.year == selected_year]
    df_selected_month = data[data["trans_date_trans_time"].dt.month_name() == selected_month]
    
    # color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    # selected_color_theme = st.selectbox('Select a color theme', color_theme_list)




# def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
#     heatmap = alt.Chart(input_df).mark_rect().encode(
#             y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
#             x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
#             color=alt.Color(f'max({input_color}):Q',
#                              legend=None,
#                              scale=alt.Scale(scheme=input_color_theme)),
#             stroke=alt.value('black'),
#             strokeWidth=alt.value(0.25),
#         ).properties(width=900
#         ).configure_axis(
#         labelFontSize=12,
#         titleFontSize=12
#         ) 
#     # height=300
#     return heatmap

# make_heatmap()