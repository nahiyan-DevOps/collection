import streamlit as st
import mysql.connector
import random

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

# Function to fetch documents from the database
def fetch_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM documents")
    documents = cursor.fetchall()
    cursor.close()
    conn.close()
    return documents

# Function to fetch a document by ID
def fetch_document_by_id(document_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, data FROM documents WHERE id = %s", (document_id,))
    document = cursor.fetchone()
    cursor.close()
    conn.close()
    return document

# Function to insert a new document into the database
def insert_document(title, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    document_id = random.randint(1000, 9999)  # Generate a random integer ID
    cursor.execute("INSERT INTO documents (id, name, data) VALUES (%s, %s, %s)", (document_id, title, content))
    conn.commit()
    cursor.close()
    conn.close()

# Function to remove a document from the database
def remove_document(document_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = %s", (document_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Streamlit app
def main():
    st.title("Document Editor and Viewer")
    section = st.sidebar.radio("Select Section", ("View Documents", "Create Document"))

    if section == "View Documents":
        view_documents_section()
    elif section == "Create Document":
        create_document_section()

# Section to view documents
def view_documents_section():
    st.header("View Documents")
    documents = fetch_documents()
    if len(documents) == 0:
        st.write("No documents available.")
    else:
        for document in documents:
            document_id, title = document
            st.subheader(title)
            if st.button(f"Remove Document - {title}"):
                remove_document(document_id)
                st.info(f"Document '{title}' removed.")
            if st.button(f"View Document - {title}"):
                document_content = fetch_document_by_id(document_id)[1]
                st.write(document_content, unsafe_allow_html=True)

# Section to create a document
def create_document_section():
    st.header("Create Document")
    document_title = st.text_input("Document Title")
    document_content = st.text_area("Document Content", height=300)

    if st.button("Save Document"):
        if document_title and document_content:
            try:
                insert_document(document_title, document_content)
                st.success("Document created successfully!")
                st.empty()
                st.info(f"Title: {document_title}")
                st.write(document_content)
            except Exception as e:
                st.error("Error occurred while creating the document.")
                st.error(str(e))
        else:
            st.warning("Please provide both a title and content for the document.")

# Run the app
if __name__ == "__main__":
    main()
