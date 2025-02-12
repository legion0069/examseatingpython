🎓 Exam Seating Arrangement System
Overview
The Exam Seating Arrangement System is a streamlined web application built using Streamlit, allowing exam organizers to efficiently manage and visualize seating arrangements for students during exams. It enables real-time updates for seating assignments and faculty allocation, with intuitive search functionality for quickly locating students by their roll numbers.

The system ensures that the seating arrangement is tailored to the number of rooms, rows, columns, and faculty members, making the seating process hassle-free and efficient.

Features
Custom Room Configuration: Dynamically choose the number of rooms, rows, and columns for seating arrangements.
File Upload: Upload CSV files for students and faculty members, automatically populating the seating arrangements.
Faculty Assignment: Assign faculty to different rooms automatically.
Real-Time Search: Quickly search for a student’s seating position by entering their roll number.
View Modes: Toggle between viewing all rooms or individual rooms, with easy navigation.
Downloadable CSV: Download the seating arrangements of all rooms as a CSV file.
Responsive and Interactive UI: A clean and user-friendly interface that can be accessed via any modern web browser.
Demo
Visit the live demo to see how the app works in action! (You can provide a link here if applicable.)

Requirements
To run the Exam Seating Arrangement System, you'll need the following:

Python 3.x (preferably 3.7+)
Streamlit
Pandas
Install the required libraries using pip:

bash
Copy
Edit
pip install streamlit pandas
Setup Instructions
Clone or Download the Repository: Clone this repository or download it as a ZIP file.

Upload Required Files:

Student CSV: Must contain a "Roll Number" column with the student roll numbers.
Faculty CSV: A list of faculty names.
Customize Room Settings:

Configure the number of rooms, rows, columns, and faculty members from the sidebar.
Enter the exam start and end time.
Run the Application:

Navigate to the project directory and run the following command to launch the Streamlit app:

bash
Copy
Edit
streamlit run app.py
View the Dashboard: Open the application in your browser at the default URL (http://localhost:8501).

How to Use
Upload CSV Files:

Upload the Student CSV and Faculty CSV through the sidebar to load the data.
Room Configuration:

Configure the number of rooms, rows, and columns as required.
Optionally rename rooms for customization.
Search for a Student:

Use the search box at the top to find a student by their roll number.
View the Seating Arrangement:

Choose between viewing All Rooms or Individual Room.
Check the seating assignments for each room along with the assigned faculty and exam timings.
Download the CSV:

Once the seating arrangements are generated, you can download the entire seating plan as a CSV file.
Example Screenshots
Student Search Feature
Seating Arrangement Display
Room Configuration Sidebar
Downloadable CSV Option
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Streamlit for providing an easy-to-use framework for building web applications.
Pandas for data processing and handling CSVs.
