import streamlit as st
import json
import pandas as pd

# Load and Save Library Data
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Initialize Library
library = load_library()

# Inject custom CSS and JavaScript
st.markdown("""
    <style>
        .stApp {
            background-color: #2e3b4e;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        section[data-testid="stSidebar"] {
            background-color: #1f2a38 !important;
            padding-top: 40px;
        }
        section[data-testid="stSidebar"] * {
            color: #a0a0a0 !important;
        }

        .main-box {
            background-color: #3c4759;
            color: #f0f0f0;
            padding: 30px;
            border-radius: 12px;
            margin: 20px auto;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            width: 90%;
            max-width: 1000px;
        }
        .main-box h1 {
            color: #4B8BBE;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 30px;
            font-weight: 700;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
        }
        h1, h2 {
            color: #6baed6 !important;
        }
        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.95em;
            width: 100%;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        .styled-table thead tr {
            background-color: #4B8BBE;
            color: #ffffff;
            text-align: left;
            font-weight: 600;
        }
        .styled-table th, .styled-table td {
            padding: 12px 15px;
            border: 1px solid #3a4a5d;
        }
        .styled-table tbody tr {
            background-color: black;
            color: #e0e0e0;
            border-bottom: 2px solid #3a4a5d;
        }
        .styled-table tbody tr:nth-child(even) {
            background-color: #364152;
        }
        .styled-table tbody tr:hover {
            background-color: #3c4759;
            color: #ffffff;
        }
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            background-color: black !important;
            color: #ffffff !important;
            border: 1px solid #4B8BBE !important;
            border-radius: 6px !important;
            padding: 10px 12px !important;
        }
        .stTextInput label, .stNumberInput label, .stTextArea label,
        .stSelectbox label, .stCheckbox label {
            color: #f0f0f0 !important;
            font-size: 1rem !important;
        }
        .stSelectbox select {
            background-color: black !important;
            color: #ffffff !important;
            border: 1px solid #4B8BBE !important;
        }
        .stButton button {
            background-color: #4B8BBE;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }
        .stButton button:hover {
            background-color: #3578A3;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        .stCheckbox .st-c7 {
            background-color: black !important;
            border: 1px solid #4B8BBE;
        }
        .stAlert {
            border-radius: 8px;
            padding: 15px;
        }
        .stSuccess {
            background-color: rgba(46, 125, 50, 0.8) !important;
            border-left: 4px solid #1b5e20 !important;
            color: #1b5e20 !important;
        }
        .stWarning {
            background-color: rgba(255, 193, 7, 0.2) !important;
            border-left: 4px solid #ffc107 !important;
            color: #ffe082 !important;
        }
    </style>

    <script>
    const mediaQuery = window.matchMedia("(max-width: 991px)");
    function closeSidebarOnClick() {
        const observer = new MutationObserver((mutationsList, observer) => {
            for (let mutation of mutationsList) {
                if (mutation.type === 'childList') {
                    const sidebar = window.parent.document.querySelector("aside[data-testid='stSidebar']");
                    const overlay = window.parent.document.querySelector("div[data-testid='stSidebarOverlay']");
                    if (sidebar && overlay && mediaQuery.matches) {
                        overlay.click();
                    }
                }
            }
        });

        const targetNode = window.parent.document.querySelector("body");
        if (targetNode) {
            observer.observe(targetNode, { childList: true, subtree: true });
        }
    }
        function autoCloseSidebar() {
        const mediaQuery = window.matchMedia("(max-width: 991px)");
        if (!mediaQuery.matches) return;

        const sidebarOverlay = window.parent.document.querySelector("div[data-testid='stSidebarOverlay']");
        if (!sidebarOverlay) return;

        const menuItems = window.parent.document.querySelectorAll("section[data-testid='stSidebar'] button");
        menuItems.forEach(btn => {
            btn.addEventListener("click", () => {
                setTimeout(() => {
                    sidebarOverlay.click();
                }, 300);
            });
        });
    }

        window.addEventListener("load", () => {
            setTimeout(autoCloseSidebar, 1000);
        });

        window.addEventListener('DOMContentLoaded', closeSidebarOnClick);
    </script>
""", unsafe_allow_html=True)

st.markdown("<div class='main-box'><h1>📚 Personal Library Manager</h1>", unsafe_allow_html=True)

# Sidebar Menu
menu = st.sidebar.radio(
    "📋 Menu Options",
    ["📖 Display Library", "➕ Add Book", "❌ Remove Book", "🔍 Search Book", "💾 Save and Exit"],
    index=0
)

# Display Library
if menu == "📖 Display Library":
    st.markdown("<h1>🗂️ Your Library Collection</h1>", unsafe_allow_html=True)
    if library:
        df = pd.DataFrame(library)
        df.rename(columns={
            "title": "Title",
            "author": "Author",
            "year": "Year",
            "genre": "Genre"
        }, inplace=True)
        df['Read Status'] = df['read_status'].apply(lambda x: '✅ Read' if x else '📖 Unread')
        df = df.drop(columns=['read_status'])
        st.markdown(
            f'<div style="overflow-x: auto;">'
            f'<table class="styled-table">{df.to_html(index=False, escape=False, classes="styled-table")}</table></div>',
            unsafe_allow_html=True
        )
        st.markdown(f"<p style='color:#b0b0b0; text-align:right;'>Total Books: {len(library)}</p>", unsafe_allow_html=True)
    else:
        st.warning("Your library is Empty. Add Some Books to get Started!")

# Add Book
elif menu == "➕ Add Book":
    st.markdown("<h1>✍️ Add a New Book</h1>", unsafe_allow_html=True)

    def clear_form_on_next_run():
        st.session_state.title_input = ""
        st.session_state.author_input = ""
        st.session_state.year_input = 2025
        st.session_state.genre_input = ""
        st.session_state.read_status_input = False
        del st.session_state["just_added"]

    if st.session_state.get("just_added"):
        clear_form_on_next_run()

    st.session_state.setdefault("title_input", "")
    st.session_state.setdefault("author_input", "")
    st.session_state.setdefault("year_input", 2025)
    st.session_state.setdefault("genre_input", "")
    st.session_state.setdefault("read_status_input", False)

    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", placeholder="Enter Book Title", key="title_input")
            author = st.text_input("Author", placeholder="Author's Name", key="author_input")
        with col2:
            year = st.number_input("Year", min_value=1800, max_value=2025, step=1, key="year_input")
            genre = st.text_input("Genre", placeholder="Fiction, Sci‑Fi, etc.", key="genre_input")
        st.markdown("<label style='color: black; font-weight: 500;'>👉 📚 I've Read This Book!</label>", unsafe_allow_html=True)
        read_status = st.checkbox("", key="read_status_input")

        submitted = st.form_submit_button("📥 Add to Library")

        if submitted:
            if title and author:
                library.append({
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read_status": read_status
                })
                save_library()
                st.success(f"Added '{title}' to Your Library Successfully!")
                st.session_state["just_added"] = True
                st.rerun()
            else:
                st.warning("Please fill in at least Title and Author fields")

# Remove Book
elif menu == "❌ Remove Book":
    st.markdown("<h1>🗑️ Remove a Book</h1>", unsafe_allow_html=True)

    if library:
        book_titles = [book["title"] for book in library]
        selected_book = st.selectbox("Select a Book to Remove", book_titles)
        confirm_removal = st.checkbox("", key="confirm_removal_input")
        st.markdown("<label style='color: black; font-weight: 500;'>⚠️ Please Confirm Removal by Clicking The Checkbox!</label>", unsafe_allow_html=True)

        if st.button("Remove Book"):
            if confirm_removal:
                book_to_remove = next((book for book in library if book["title"] == selected_book), None)
                if book_to_remove:
                    library.remove(book_to_remove)
                    save_library()
                    st.success(f"✅ Removed '{selected_book}' From Your Library.")
                    st.rerun()
            else:
                st.warning("Please Confirm Removal by Clicking the Checkbox.")
    else:
        st.warning("Your Library is Empty. There's Nothing to Remove.")

# Search Book
elif menu == "🔍 Search Book":
    st.markdown("<h1>🔍 Search Your Library</h1>", unsafe_allow_html=True)
    search_term = st.text_input("Search by Title or Author", placeholder="Enter Search Term")

    if search_term:
        results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
        if results:
            st.markdown(f"<p style='color:#b0b0b0;'>Found {len(results)} matching books:</p>", unsafe_allow_html=True)
            result_df = pd.DataFrame(results)
            result_df.rename(columns={"title": "Title", "author": "Author", "year": "Year", "genre": "Genre"}, inplace=True)
            result_df['Read Status'] = result_df['read_status'].apply(lambda x: '✅ Read' if x else '📖 Unread')
            result_df = result_df.drop(columns=['read_status'])
            st.markdown(
                f'<div style="overflow-x: auto;">'
                f'<table class="styled-table">{result_df.to_html(index=False, escape=False, classes="styled-table")}</table></div>',
                unsafe_allow_html=True
            )
        else:
            st.warning("No Books Found Matching Your Search")

# Save and Exit
elif menu == "💾 Save and Exit":
    save_library()
    st.markdown("<h2 style='color: green;'>✅ Your Library has been Saved Successfully!</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#e0e0e0;'>👋 Thank You for using the Library Manager</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#b0b0b0;'>Come back soon to manage your growing collection!</p>", unsafe_allow_html=True)
    st.stop()

# Close wrapper div
st.markdown("</div>", unsafe_allow_html=True)
