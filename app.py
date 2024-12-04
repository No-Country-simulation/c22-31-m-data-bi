import streamlit as st

# Initialize session state for logged_in status if not already set
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Function for handling user login
def login():
    """
    Displays the login button and sets the 'logged_in' session state to True
    when the button is clicked. Also triggers a rerun to update the page.
    """
    if st.button("Log in"):
        st.session_state.logged_in = True  # Set logged_in to True
        st.rerun()  # Rerun the app to update session state


# Function for handling user logout
def logout():
    """
    Displays the logout button and sets the 'logged_in' session state to False
    when the button is clicked. Also triggers a rerun to update the page.
    """
    if st.button("Log out"):
        st.session_state.logged_in = False  # Set logged_in to False
        st.rerun()  # Rerun the app to update session state


# Define the login page with the appropriate title and icon
login_page = st.Page(login, title="Log in", icon=":material/login:")

# Define the logout page with the appropriate title and icon
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# Define different pages for navigation after login
home = st.Page(
    "pages/1_home.py",
    title="Home",
    icon=":material/home:",
    default=True
    )
data_exploration = st.Page(
    "pages/2_data_exploration.py",
    title="Data Exploration",
    icon=":material/data_exploration:"
    )
data_preprocessing = st.Page(
    "pages/3_data_preprocessing.py",
    title="Data Preprocessing",
    icon=":material/transform:"
    )
bi_dashboard = st.Page(
    "pages/4_bi_dashboard.py",
    title="BI Dashboard",
    icon=":material/dashboard:"
    )
predictive_modeling = st.Page(
    "pages/5_predictive_modeling.py",
    title="Predictive Modeling",
    icon=":material/model_training:"
    )
advanced_analysis = st.Page(
    "pages/6_advanced_analysis.py",
    title="Advanced Analysis",
    icon=":material/analytics:"
    )
real_time_detection = st.Page(
    "pages/7_real_time_detection.py",
    title="Real Time Detection",
    icon=":material/timeline:"
    )
reports = st.Page(
    "pages/8_reports.py",
    title="Reports",
    icon=":material/sim_card_download:"
    )
about = st.Page(
    "pages/9_about.py",
    title="About",
    icon=":material/info:"
    )

# Conditional navigation logic based on logged_in session state
if st.session_state.logged_in:
    # If logged in, show the navigation menu with pages
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Main Menu": [
                home,
                data_exploration,
                data_preprocessing,
                bi_dashboard,
                predictive_modeling,
                advanced_analysis,
                real_time_detection,
                reports,
                about
                ]
        }
    )
else:
    # If not logged in, only show the login page
    pg = st.navigation([login_page])

# Run the selected page based on navigation
pg.run()
