import streamlit as st
import pandas as pd
import base64
import random
from io import StringIO

# Page configuration
st.set_page_config(page_title="Seating Arrangement", layout="wide", initial_sidebar_state="expanded")
with open("examseating/examseating/image2.jpg", "rb") as img_file:
    base64_string = base64.b64encode(img_file.read()).decode()
# Custom CSS for styling
st.markdown(f"""
    <style>
    body {{
        background-image: url("data:image/jpg;base64,{base64_string}");
        background-color: #f5f5f5; /* Light background */
        color: black; 
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        
    }}
    .stApp {{
        font-family: 'Arial', sans-serif;
        background-color: rgba(255, 255, 255, 0.8); /* Optional: Add a white overlay for better readability */
        border-radius: 10px;
        padding: 10px;
        color: black;
    }}
    .header {{
        background-color: rgba(0, 150, 136, 0.8); /* Adjust opacity for overlay effect */
        color: white;
        padding: 20px;
        text-align: center;
        font-size: 24px;
        border-radius: 10px;
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# Title section
st.markdown("<div class='header'>🎓 Exam Seating Arrangement System</div>", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("Upload Files")
student_csv = st.sidebar.file_uploader("Upload Student CSV", type="csv")
faculty_csv = st.sidebar.file_uploader("Upload Faculty CSV", type="csv")

# Room and seating configuration
st.sidebar.header("Room Configuration")
num_rooms = st.sidebar.number_input("Number of Rooms", min_value=1, value=2)
num_rows = st.sidebar.number_input("Rows per Room", min_value=1, value=5)
num_columns = st.sidebar.number_input("Columns per Room", min_value=1, value=6)

# Manual exam timing inputs
st.sidebar.header("Exam Timing")
exam_start_time = st.sidebar.text_input("Start Time (e.g., 09:00 AM)", value="09:00 AM")
exam_end_time = st.sidebar.text_input("End Time (e.g., 12:00 PM)", value="12:00 PM")

# Room names and customization
room_names = [f"Room {i+1}" for i in range(num_rooms)]
custom_room_names = room_names.copy()
room_to_change = st.sidebar.selectbox("Select Room to Rename", room_names)
new_room_name = st.sidebar.text_input(f"Rename {room_to_change}", value=room_to_change)

if new_room_name != room_to_change:
    custom_room_names[room_names.index(room_to_change)] = new_room_name

# Search Feature at the top
st.markdown("<div class='section-title'>🔍 Search for a Student</div>", unsafe_allow_html=True)
search_roll_number = st.text_input("Enter Roll Number")

# Processing student data
if student_csv:
    try:
        student_df = pd.read_csv(student_csv)
        if "Roll Number" not in student_df.columns:
            st.error("Student CSV must contain a 'Roll Number' column.")
        else:
            student_roll_numbers = student_df["Roll Number"].tolist()
    except Exception as e:
        st.error(f"Error reading student file: {e}")
else:
    st.warning("Please upload a student CSV file.")

# Processing faculty data
if faculty_csv:
    try:
        faculty_df = pd.read_csv(faculty_csv)
        if faculty_df.empty or len(faculty_df.columns) < 1:
            st.error("Faculty CSV must contain at least one column with names.")
        else:
            faculty_names = faculty_df.iloc[:, 0].dropna().tolist()
    except Exception as e:
        st.error(f"Error reading faculty file: {e}")
else:
    st.warning("Please upload a faculty CSV file.")

# Ensure data availability
if student_csv and faculty_csv:
    total_seats_per_room = num_rows * num_columns
    total_seats = total_seats_per_room * num_rooms

    if len(student_roll_numbers) > total_seats:
        st.error("Not enough seats for the number of students.")
    elif len(faculty_names) < num_rooms:
        st.error("Not enough faculty names for the number of rooms.")
    else:
        # Allocate students to seats
        seating_arrangements = []
        student_index = 0

        for room_idx in range(num_rooms):
            room_seating = []
            for row in range(num_rows):
                row_seating = []
                for col in range(num_columns):
                    if student_index < len(student_roll_numbers):
                        row_seating.append(student_roll_numbers[student_index])
                        student_index += 1
                    else:
                        row_seating.append("Empty")
                room_seating.append(row_seating)
            seating_arrangements.append(room_seating)

        # Faculty assignment
        random.shuffle(faculty_names)
        room_faculty = dict(zip(custom_room_names, faculty_names[:num_rooms]))

        # Search Functionality
        room_found = None
        if search_roll_number:
            found = False
            for room_idx, room_name in enumerate(custom_room_names):
                for row_idx, row in enumerate(seating_arrangements[room_idx]):
                    if search_roll_number in row:
                        col_idx = row.index(search_roll_number)
                        room_found = room_name
                        found = True
                        break
                if found:
                    break
            if not found:
                st.error(f"Student {search_roll_number} not found.")

        # Display results
        st.markdown("<div class='section-title'>Seating Arrangements</div>", unsafe_allow_html=True)
        
        if room_found:
            # Show the room with the highlighted roll number
            room_idx = custom_room_names.index(room_found)
            st.markdown(
                f"<div class='room-card'><h3>{room_found}</h3>"
                f"<p><b>Faculty:</b> {room_faculty[room_found]}<br>"
                f"<b>Exam Time:</b> {exam_start_time} - {exam_end_time}</p></div>",
                unsafe_allow_html=True
            )
            
            room_df = pd.DataFrame(seating_arrangements[room_idx], columns=[f"Seat {i+1}" for i in range(num_columns)])

            # Highlight the searched roll number
            room_df = room_df.applymap(lambda x: f"<span class='highlight'>{x}</span>" if str(x) == search_roll_number else x)

            st.markdown(room_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        else:
            # Show all rooms when no search or search not found
            selected_view = st.radio("View Mode", ["All Rooms", "Individual Room"])

            if selected_view == "All Rooms":
                all_data = []
                for room_idx, room_name in enumerate(custom_room_names):
                    st.markdown(
                        f"<div class='room-card'><h3>{room_name}</h3>"
                        f"<p><b>Faculty:</b> {room_faculty[room_name]}<br>"
                        f"<b>Exam Time:</b> {exam_start_time} - {exam_end_time}</p></div>",
                        unsafe_allow_html=True
                    )
                    room_df = pd.DataFrame(seating_arrangements[room_idx], columns=[f"Seat {i+1}" for i in range(num_columns)])
                    
                    # Highlight search result if there's any
                    if search_roll_number:
                        room_df = room_df.applymap(lambda x: f"<span class='highlight'>{x}</span>" if str(x) == search_roll_number else x)

                    st.markdown(room_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                    room_df.insert(0, "Room Name", room_name)
                    all_data.append(room_df)

                # Download option for all rooms
                all_rooms_csv = pd.concat(all_data)
                csv_buffer = StringIO()
                all_rooms_csv.to_csv(csv_buffer, index=False)
                st.download_button("Download All Room Arrangements as CSV", data=csv_buffer.getvalue(), file_name="all_rooms.csv")

            elif selected_view == "Individual Room":
                selected_room = st.selectbox("Select Room", custom_room_names)
                room_idx = custom_room_names.index(selected_room)
                st.markdown(
                    f"<div class='room-card'><h3>{selected_room}</h3>"
                    f"<p><b>Faculty:</b> {room_faculty[selected_room]}<br>"
                    f"<b>Exam Time:</b> {exam_start_time} - {exam_end_time}</p></div>",
                    unsafe_allow_html=True
                )
                room_df = pd.DataFrame(seating_arrangements[room_idx], columns=[f"Seat {i+1}" for i in range(num_columns)])

                # Highlight the searched roll number
                if search_roll_number:
                    room_df = room_df.applymap(lambda x: f"<span class='highlight'>{x}</span>" if str(x) == search_roll_number else x)

                st.markdown(room_df.to_html(escape=False, index=False), unsafe_allow_html=True)
