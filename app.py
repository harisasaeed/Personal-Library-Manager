import streamlit as st
import json
import os

# File to store book data
LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read_status):
    book = {
        "Title": title,
        "Author": author,
        "Year": year,
        "Genre": genre,
        "Read": read_status
    }
    library.append(book)
    save_library(library)
    st.success("✅ Book added successfully!")

def remove_book(library, title):
    library[:] = [book for book in library if book["Title"].lower() != title.lower()]
    save_library(library)
    st.success("❌ Book removed successfully!")

def search_books(library, keyword):
    return [book for book in library if keyword.lower() in book["Title"].lower() or keyword.lower() in book["Author"].lower()]

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, percentage_read

def main():
    st.title("📚 Personal Library Manager by ChatGPT")
    user_name = st.text_input("👤 Enter your name:", key="username")
    if not user_name:
        st.warning("⚠️ Please enter your name to continue.")
        return
    
    st.write(f"👋 Welcome, {user_name}!")
    library = load_library()

    menu = ["📖 Add a Book", "🗑️ Remove a Book", "🔍 Search for a Book", "📚 Display All Books", "📊 Display Statistics"]
    choice = st.sidebar.selectbox("📜 Menu", menu)

    if choice == "📖 Add a Book":
        with st.form("add_book_form"):
            title = st.text_input("📕 Title")
            author = st.text_input("✍️ Author")
            year = st.number_input("📅 Publication Year", min_value=0, step=1)
            genre = st.text_input("🎭 Genre")
            read_status = st.checkbox("✅ Read")
            submitted = st.form_submit_button("➕ Add Book")
            if submitted and title and author and genre:
                add_book(library, title, author, year, genre, read_status)
    
    elif choice == "🗑️ Remove a Book":
        title = st.text_input("❌ Enter the title of the book to remove")
        if st.button("🗑️ Remove Book") and title:
            remove_book(library, title)
    
    elif choice == "🔍 Search for a Book":
        keyword = st.text_input("🔎 Enter title or author to search")
        if st.button("🔍 Search") and keyword:
            results = search_books(library, keyword)
            for book in results:
                st.write(f"📖 **{book['Title']}** by ✍️ {book['Author']} ({book['Year']}) - 🎭 {book['Genre']} - {'✅ Read' if book['Read'] else '📖 Unread'}")
            if not results:
                st.warning("⚠️ No matching books found.")
    
    elif choice == "📚 Display All Books":
        if library:
            for book in library:
                st.write(f"📖 **{book['Title']}** by ✍️ {book['Author']} ({book['Year']}) - 🎭 {book['Genre']} - {'✅ Read' if book['Read'] else '📖 Unread'}")
        else:
            st.info("📭 Your library is empty.")
    
    elif choice == "📊 Display Statistics":
        total, percentage = display_statistics(library)
        st.write(f"📚 **Total books:** {total}")
        st.write(f"📈 **Percentage read:** {percentage:.2f}%")

if __name__ == "__main__":
    main()