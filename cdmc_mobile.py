import streamlit as st
from datetime import datetime
import requests #Live auto-check
import os
import streamlit.components.v1 as components
import pytz # Philippines Time Zone
# Force Python to find your 'Image' folder relative to this script
base_path = os.path.dirname(__file__)

# Checks Youtube for LIVE Status
def check_youtube_live():
    url = "https://www.youtube.com/@CDMCVideos/live"
    try:
        response = requests.get(url, timeout=5)
        if '{"text" : "watching"}' in response.text:
            return True
        return False
    except:
        st.sidebar.warning("⚠️ Please check your internet connection")
        return False

# Function to read text from Content Folder
def load_text(filename):
    target_path = os.path.join(base_path, "Content", filename)
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Content coming soon..."

# App like look in the browser

# Countdown - Set to Manila Time
manila_tz = pytz.timezone('Asia/Manila')
now_in_manila = datetime.now(manila_tz)
hour = now_in_manila.hour

if hour < 12:
    st.write("☀️ **Good Morning, CDMC Family!**")
elif hour < 18:
    st.write("🌤️ **Good Afternoon, CDMC Family!**")
else:
    st.write("🌙 **Good Evening, CDMC Family!**")

# Path for logo
logo_path = os.path.join(os.path.dirname(__file__), "cdmc_logo.png")

st.set_page_config(
    page_title="CDMC Portal", 
    page_icon=logo_path,
    initial_sidebar_state="auto"
    )
# App icon on Mobile Force Fix
st.markdown (
    f"""
    <link rel="apple-touch-icon" href="cdmc_logo.png">
    <link rel="shortcut icon" href="cdmc_logo.png">
    """,
    unsafe_allow_html=True
    )
st.image(logo_path, width=150)

st.title("⛪ CDMC Las Pinas Portal")
st.write("Welcome to the Christian Disciples of Missionary Church")
st.sidebar.image(logo_path, width=100) # Sidebar Logo

# Sidebar for Navigation
# Initialize the page if it's the first time opening the app
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

# Define a function to change pages
def ch_pg(name):
    st.session_state.page = name
    # This toast pops up at the bottom to tell the user the page changed!
    st.toast(f"Switched to {name}")

# --- SIDEBAR MENU ---
st.sidebar.write("### Dashboard")

# Custom Rounded Buttons for Menu
st.sidebar.button("🏠 Home", use_container_width=True, on_click=ch_pg, args=['Home'])
st.sidebar.button("🎉 Events", use_container_width=True, on_click=ch_pg, args=['Events'])
st.sidebar.button("📖 Daily Verse", use_container_width=True, on_click=ch_pg, args=['Daily Verse'])
st.sidebar.button("🙏 Prayer Requests", use_container_width=True, on_click=ch_pg, args=['Prayer Requests'])
st.sidebar.button("📸 Gallery", use_container_width=True, on_click=ch_pg, args=['Gallery'])
st.sidebar.button("📹 Live Links", use_container_width=True, on_click=ch_pg, args=['Live Links'])

# Set the choice variable based on the session state
choice = st.session_state.page

st.sidebar.divider()
st.sidebar.subheader("📢 Announcements")
st.sidebar.write("* **Prayer Meeting:** _Wednesday @ 7:30 PM_")
st.sidebar.write("* **Sunday School:** _@ 8:30 AM_")
st.sidebar.write("* **Sunday Service:** _@ 10:00 AM_")

if choice == "Home":
    # One line of code to show the whole text
    st.subheader("Mission")
    church_mission = load_text("mission.txt")
    st.info(church_mission)

    st.subheader("Vision")
    church_vision = load_text("vision.txt")
    st.info(church_vision)

    st.divider()

    st.subheader("Church News")
    church_news = load_text("news.txt")
    st.info(church_news)
    st.divider()
    st.subheader("📍 Visit Us")
        
        # HTML code that brings Google Maps
    map_html = """
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1049.6703935196374!2d120.98532882073297!3d14.45161637107129!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3397cdfdadb88a19%3A0x99c795a7b7224ae7!2sChristian%20Disciples%20Missionary%20Church!5e0!3m2!1sen!2sph!4v1778168466833!5m2!1sen!2sph" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    """
        # This line tells Streamlit to run that HTML code
    components.html(map_html, height=360)
        
    st.info("⛪ **CDMC Las Piñas**")

elif choice == "Events":
    st.subheader("Upcoming Events")
    st.info("🟢 _Family Day ~ 30th May 2026_")

elif choice == "Daily Verse":
    st.header("📖 Verse of the Day")
    st.success("'I can do all things through Christ who strengthens me.' - Philippians 4:13")
    st.header("📖 Daily Reading Plan") # Manual Update Weekly
    st.info("Todays Reading: **Esther 4:1-17**")

    if st.checkbox("I have finished today's reading"):
        st.balloons() # Celebration animation
        st.success("Great job! Keep growing in the LORD.")

elif choice == "Prayer Requests":
    st.header("🙏 Prayer Wall")
    st.write("Share your burdens with us.")

    # Direct URL to your sheet's export function
    sheet_id = "1miF0T_P-4WvARbATi1QE-3JvkL5Zlx6ork-gRgjR8go"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

    with st.form(key="prayer_form"):
        name = st.text_input("Name (Optional)")
        request = st.text_area("How can we pray for you?")
        submit_button = st.form_submit_button(label="Submit Request")

        if submit_button:
            if request:
                import pandas as pd
                from datetime import datetime
                import pytz
                
                # Setup time
                manila_tz = pytz.timezone('Asia/Manila')
                timestamp = datetime.now(manila_tz).strftime("%Y-%m-%d %H:%M")
                
                st.balloons()
                st.success(f"Thank you {name if name else 'friend'}, your request has been noted! (This version is for viewing; I will help you link the 'Write' function next.)")
            else:
                st.warning("Please enter a prayer request.")

    st.divider()
    
    # 3. Your Prayer Support Button (Fellowship)
    st.subheader("🤝 Pray with Others")
    st.write("Click below to let the community know you are praying for the current requests.")
    
    if st.button("🙏 I am praying for this"):
        st.success("Amen! Your fellowship in prayer has been noted.")
        st.toast("You've joined the prayer circle!", icon="✨")

elif choice == "Gallery":
    st.header("📸 CDMC Activity Gallery")
    st.subheader("VBS Kalinga ⛰")
    
    # 1. Get the folder where your cdmc_mobile.py is saved
    base_path = os.path.dirname(__file__)

    # 2. Build the full path to your images
    img1_path = os.path.join(base_path, "Image", "VBS Kalinga", "img1.jpeg")
    img2_path = os.path.join(base_path, "Image", "VBS Kalinga", "img2.jpeg")
    img3_path = os.path.join(base_path, "Image", "VBS Kalinga", "img3.jpeg")
    img4_path = os.path.join(base_path, "Image", "VBS Kalinga", "img4.jpeg")

    # 3. Display them in a single column for landscape view
    st.image(img1_path, caption="☆⎯Classroom⎯✿", use_container_width=True)
    st.divider() # Line between each landscape photo
    st.image(img2_path, caption="☆⎯Snack Time⎯✿", use_container_width=True)
    st.divider()
    st.image(img3_path, caption="☆⎯Activity⎯✿", use_container_width=True)
    st.divider()
    st.image(img4_path, caption="☆⎯Activity⎯✿", use_container_width=True)
    st.divider()

elif choice == "Live Links":
    st.header("📹 CDMC Live Stream")
    is_live = check_youtube_live()

    if is_live:
        st.error("🔴 WE ARE LIVE! Click below to join the service.")
        st.video("https://www.youtube.com/@CDMCVideos")
    else:
        st.info("Check back Sunday at 10:00 AM for our next Live Service.")
        st.link_button("Watch Past Sermons", "https://www.youtube.com/@CDMCVideos/streams")

    st.divider()
    st.write("Follow us on Facebook for daily updates:")
    st.link_button("Go to CDMC Facebook", "https://web.facebook.com/cdmc.lp/?_rdc=1&_rdr") 


