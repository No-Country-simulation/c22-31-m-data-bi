import streamlit as st

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

# show the navigation menu with pages
pg = st.navigation(
        {"Main Menu": [
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

# Run the selected page based on navigation
pg.run()
