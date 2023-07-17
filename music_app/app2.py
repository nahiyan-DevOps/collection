import streamlit as st
import mysql.connector
import os
from pydub import AudioSegment
from pydub.playback import play

# Database connection details
db_connection = {
    "host": "localhost",
    "port": 3306,
    "user": "scraper",
    "password": "123",
    "database": "collection",
}

# Function to establish a database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_connection)
    return conn

# Function to fetch audio files from the database
def fetch_audio_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, data FROM music")
    audio_files = cursor.fetchall()
    cursor.close()
    conn.close()
    return audio_files

# Function to insert a new audio file into the database
def insert_audio_file(name, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO music (name, data) VALUES (%s, %s)", (name, data))
    conn.commit()
    cursor.close()
    conn.close()

# Function to remove an audio file from the database
def remove_audio_file(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM music WHERE name = %s", (name,))
    conn.commit()
    cursor.close()
    conn.close()

# Streamlit app
def main():
    st.title("Audio Player and Uploader")
    section = st.sidebar.radio("Select Section", ("View Audio Files", "Upload Audio File"))

    if section == "View Audio Files":
        view_audio_files_section()
    elif section == "Upload Audio File":
        upload_audio_file_section()

# Section to view audio files
def view_audio_files_section():
    st.header("View Audio Files")
    audio_files = fetch_audio_files()
    if len(audio_files) == 0:
        st.write("No audio files available.")
    else:
        for audio in audio_files:
            name, data = audio
            st.write(f"**{name}**")
            st.audio(data, format="audio/mp3")
            if st.button(f"Remove Audio - {name}"):
                remove_audio_file(name)
                st.info(f"Audio file '{name}' removed.")

# Section to upload an audio file
def upload_audio_file_section():
    st.header("Upload Audio File")
    audio_name = st.text_input("Audio Name")
    audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])

    if st.button("Upload"):
        if audio_name and audio_file:
            try:
                audio_data = audio_file.read()
                insert_audio_file(audio_name, audio_data)
                st.success("Audio file uploaded successfully!")
            except Exception as e:
                st.error("Error occurred while uploading the audio file.")
                st.error(str(e))
        else:
            st.warning("Please provide both a name and an audio file.")

# Run the app
if __name__ == "__main__":
    main()
