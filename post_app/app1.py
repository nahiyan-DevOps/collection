import streamlit as st
import mysql.connector
from PIL import Image
from io import BytesIO

# Database connection details
db_connection = {
    "host": "192.168.0.204",
    "port": 3306,
    "user": "scraper",
    "password": "123",
    "database": "collection",
}

# Function to establish a database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_connection)
    return conn

# Function to fetch photos from the database
def fetch_photos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, data FROM photo")
    photos = cursor.fetchall()
    cursor.close()
    conn.close()
    return photos

# Function to insert a new photo into the database
def insert_photo(name, data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO photo (name, data) VALUES (%s, %s)", (name, data))
    conn.commit()
    cursor.close()
    conn.close()

# Streamlit app
def main():
    st.title("Photo Viewer and Uploader")
    section = st.sidebar.radio("Select Section", ("View Photos", "Add Photo"))

    if section == "View Photos":
        view_photos_section()
    elif section == "Add Photo":
        add_photo_section()

# Section to view photos
def view_photos_section():
    st.header("View Photos")
    photos = fetch_photos()
    if len(photos) == 0:
        st.write("No photos available.")
    else:
        col1, col2, col3 = st.columns(3)
        for i in range(0, len(photos), 3):
            for j, photo in enumerate(photos[i:i+3]):
                name, data = photo
                img = Image.open(BytesIO(data))
                with col1 if j == 0 else col2 if j == 1 else col3:
                    st.image(img, use_column_width=True)
                    caption_style = f"font-size: 18px;"
                    st.markdown(f"<p style='{caption_style}'>{name}</p>", unsafe_allow_html=True)
                    if st.button(f"Remove Photo - {name}"):
                        remove_photo(name)
                        st.info(f"Photo '{name}' removed.")

# Function to remove a photo from the database
def remove_photo(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM photo WHERE name = %s", (name,))
    conn.commit()
    cursor.close()
    conn.close()

# Function to convert image to JPEG format
def convert_image_to_jpeg(image):
    # Convert image to RGB format if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Create a BytesIO object to store the JPEG image data
    jpeg_data = BytesIO()
    image.save(jpeg_data, format="JPEG")
    jpeg_data.seek(0)

    return jpeg_data.read()

# Section to add a photo
def add_photo_section():
    st.header("Add Photo")
    photo_name = st.text_input("Photo Name")
    photo_file = st.file_uploader("Upload Photo")

    if st.button("Add Photo"):
        if photo_name and photo_file:
            try:
                # Open the image using PIL
                image = Image.open(photo_file)

                # Convert the image to JPEG format
                jpeg_data = convert_image_to_jpeg(image)

                # Insert the JPEG data into the database
                insert_photo(photo_name, jpeg_data)
                st.success("Photo added successfully!")
            except Exception as e:
                st.error("Error occurred while adding the photo.")
                st.error(str(e))
        else:
            st.warning("Please provide both a name and a photo file.")



# Run the app
if __name__ == "__main__":
    main()