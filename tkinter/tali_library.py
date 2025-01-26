import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import sqlite3


global book_title_entry, return_date_entry
logged_in_student_id = None

def create_books_table():
    conn = sqlite3.connect("data_base.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        author TEXT,
        availability TEXT
    )
    """)
    conn.commit()
    conn.close()
# Create the Students table if it doesn't exist
def create_students_table():
    try:
        conn = sqlite3.connect("data_base.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error creating Students table: {e}")

 # Connect to the database
def create_librarian_table():
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Librarians (
        librarian_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)
    # Insert default librarian credentials
    try:
        cursor.execute("""
        INSERT INTO Librarians (name, email)
        VALUES (?, ?)
        ON CONFLICT(email) DO NOTHING
        """, ('Librarian Name', 'librarian@gmail.com'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()

# Create Borrowed Books Table
def create_borrowed_books():
    conn = sqlite3.connect("data_base.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS BorrowedBooks (
        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        date_borrowed DATE NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)
    )
    """)
    conn.commit()
    conn.close()

# Create Borrow Request Table
def create__borrow_request_books():
    conn = sqlite3.connect("data_base.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS BorrowRequests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        request_date DATE NOT NULL,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (book_id) REFERENCES books(book_id)  -- Corrected foreign key reference
    )
    """)
    conn.commit()
    conn.close()

# Create Return Request Table
def create_return_request_books():
    conn = sqlite3.connect("data_base.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS ReturnRequests (
        return_request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        borrow_id INTEGER NOT NULL,
        request_date DATE NOT NULL,
        FOREIGN KEY (borrow_id) REFERENCES BorrowedBooks(borrow_id)
    )
    """)
    conn.commit()
    conn.close()
def reset_borrow_requests_table():
    """Drop and recreate the BorrowRequests table with the correct schema."""
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Drop BorrowRequests if it exists
    cursor.execute("DROP TABLE IF EXISTS BorrowRequests")

    # Recreate BorrowRequests
    create__borrow_request_books()

    conn.close()

# Database Initialization
def database_initialization():
    create_librarian_table()
    create_books_table()
    create_students_table()
    create_borrowed_books()
    create__borrow_request_books()
    create_return_request_books()
    reset_borrow_requests_table()
   
# Create functions for every button to display widgets and call it
def  treeview_view_books():
    # Books and its category
    global books_by_category
    books_by_category = {
        "Office Administration": [
            {"title": "Administrative Office Management", "author": "Pattie Odgers", "availability": "Available"},
            {"title": "Administrative Professional", "author": "Karin M. Stulz", "availability": "Available"},
        ],
        "Hospitality Management": [
            {"title": "Introduction to Hospitality Management", "author": "John R. Walker", "availability": "Available"},
            {"title": "Hospitality Management and Organisational Behaviour", "author": "Laurie Jay Mullins", "availability": " Available"},
            {"title": "Accommodations Operations and Management", "author": "author", "availability": "Available"},
            {"title": "Introduction to Hospitality Management", "author": "author", "availability": "Available"},
            {"title": "Gastronomy and the Dining Experience", "author": "John R. Walker", "availability": "Available"},
            {"title": "Forecasting Tourism Demand", "author": "Gopal Verma", "availability": "Available"},
            {"title": "Food Structure Engineering and Design for Improved Nutrition, Health and Well Being", "author": "Cerquiera Pastrana", "availability": "Available"},
            {"title": "Food Science and Nutrition: An Integrated Approach", "author": "Burnett", "availability": "Available"},
            {"title": "Food Production Operations", "author": "Parvinder S. Bali", "availability": "Available"},
            {"title": "Food Science and Health: Diet and Disease", "author": "author", "availability": "Available"},
            {"title": "Battery Management Systems and Its Applicationst", "author": "Tan Vezzini Fan Khare Xu Wei", "availability": "Available"},
            {"title": "Food and Beverage Management in the Luxury Hotel Industry", "author": "Boussard", "availability": "Available"},
            {"title": "Festival and Special Event Planning", "author": "Allen Harris Jago", "availability": "Available"},
            {"title": "Dining Etiquettes: Essential Table Manners", "author": "'Larsen & Keller", "availability": "Available"},
            {"title": "Customer Service in Travel & Tourism", "author": "author", "availability": "Available"},
            {"title": "Customer Care, Service & Hospitality Ethics", "author": "author", "availability": "Available"},
            {"title": "Cultural Tourism", "author": "Hilary du Cros and Bob McKercher", "availability": "Available"},
            {"title": "Conferences and Conventions", "author": "Tony Rogers and Peter Wynn-Moylan", "availability": "Available"},
            {"title": "Community Involvement in Tourism Development", "author": "Arjona", "availability": "Available"},
            {"title": "Bakery & Confectionery Technology', ' ", "author": "Khalid Bashir Kulsum Jan Shumaila Jan Mehvish Habib", "availability": "Available"},

        ],
        "Computer Engineering": [
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": " Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
            {"title": "Digital Design and Computer Architecture", "author": "David Monley", "availability": "Available"},
            {"title": "The Hardware/Software Interface", "author": "David Patterson", "availability": "Available"},
        ],
        
        
        
        "Information Technology": [
            {"title": "Learn Python", "author": "Al Sweigart", "availability": "Available"},
            {"title": "JavaScript for Kids", "author": "Nick Morgan", "availability": "Available"},
            {"title": "A Cost Based Approach to Project Management", "author": "Mehmet, Nihat, Hanioğlu", "availability": "Available"},
            {"title": "Advanced Database Management Systems", "author": "author", "availability": "Available"},
            {"title": "AI-Enabled 6G Networks and Applications", "author": "Gupta Ragab Mansour Khamparia Khanna", "availability": "Available"},
            {"title": "AI and Machine Learning for Network and Security Management", "author": "Wu Ge Li", "availability": "Available"},
            {"title": "An Object-Oriented Python Cookbook in Quantum Information Theory and Quantum Computing", "author": "M.S. Ramkarthik", "availability": "Available"},
            {"title": "Applied Mathematics in Engineering", "author": "Moreira", "availability": "Available"},
            {"title": "Application of Nanotechnology in Mining Processes", "author": "Kankeu et al", "availability": "Available"},
            {"title": "Artiticial Intelligence-Based Smart Power Systems", "author": "Padmanaban", "availability": "Available"},
            {"title": "Aritificial Intelligence: Concepts, Techniques and Application", "author": "Keller", "availability": "Available"},
            {"title": "Artificial Intelligence and Machine Learning in Smart City Planning", "author": "Basetti, Shiva, Ungarala, Rangarajan", "availability": "Available"},
            {"title": "Artificial Intelligence for Science", "author": "Choudhary, Fox, Hey", "availability": "Available"},
            {"title": "Battery Management Systems and Its Applications", "author": "Tan, Vezzini, Fan, Khare, Xu, Wei", "availability": "Available"},
            {"title": "Basic Computer Coding: C++", "author": "author", "availability": "Available"},
            {"title": "Basic Electrical and Electronics Engineering", "author": "author", "availability": "Available"},
            {"title": "Building Electro-Optical Systems", "author": "Hobbs", "availability": "Available"},
            {"title": "Computer Networking: An Innovative Approach", "author": "Martin", "availability": "Available"},
            {"title": "Computer Services Management", "author": "author", "availability": "Available"},
            {"title": "C++ Programming", "author": "Jones", "availability": "Available"},
        ],
        "PE": [
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
            {"title": "Sports Science", "author": "Dr. Smith", "availability": "Available"},
            {"title": "Yoga for All", "author": "Patricia Allen", "availability": "Available"},
        ],
    } 
    # Insert datbase
    conn = sqlite3.connect("data_base.db")
    c = conn.cursor()

    for category, books in books_by_category.items():
        for book in books:
            # Check if book already exists in the database (ignoring availability)
            c.execute("""SELECT * FROM books WHERE category = ? AND title = ? AND author = ?""",
                    (category, book['title'], book['author']))
            existing_book = c.fetchone()
            if existing_book is None:
                c.execute("""INSERT INTO books (category, title, author, availability)
                            VALUES (?, ?, ?, ?)""",
                        (category, book['title'], book['author'], book['availability']))

    conn.commit()
    conn.close()

def query():
  conn = sqlite3.connect("data_base.db")
  c = conn.cursor()

  c.execute("SELECT  * FROM books")
  records = c.fetchall()
#   print(records)

  print_records = ''
  for record in records:
    print_records += str(record[1]) +" "+ str(record[2]) +" "+ str(record[3])+ "\n" +"\n"
  query_label = ctk.CTkLabel(
    main_area_frame,
    text=print_records,
    font=("Arial",12),
    fg_color="#DCDEDE",
    text_color="black",
    pady=20,
    justify="left")
  query_label.pack(pady=10,padx=10,anchor='w', ipadx=30)

  conn.commit()

  conn.close()

def fetch_books():
  conn = sqlite3.connect("data_base.db")
  c = conn.cursor()

  c.execute("SELECT  category, title, author, availability FROM books")
  rows = c.fetchall()

  conn.commit()

  conn.close()
  return rows
  # Display books in the Treeview
def display_books_in_treeview(tree):
  for item in tree.get_children():
      tree.delete(item)

  books = fetch_books()
  category_dict = {}
  for category, title, author, availability in books:
      category_dict.setdefault(category, []).append((title, author, availability))

  for category, books in category_dict.items():
      parent_row = tree.insert("", "end", values=(category, "", "", ""))
      for title, author, availability in books:
          tree.insert(parent_row, "end", values=("", title, author, availability))




def database_treeview():
    treeview_view_books()

    style = ttk.Style(main_area_frame)
    style.theme_use("default")
    style.configure("Treeview.Heading",
    font=("Arial",12, "bold"),
    background="#A90503",
    foreground="white",
    relief="flat")

    style.map("Treeview.Heading", 
    background =[("active ","#A90503"), ("pressed", "#A90503")],
    foreground =[("active ", "white"), ("pressed", "white")])

    # Create the Treeview
    tree = ttk.Treeview(main_area_frame, columns=("Category", "Title", "Author", "Availability"), show="headings", height=20)
    #tree.pack(fill=tk.BOTH, expand=True)
    tree.pack(fill='both',expand=True, pady=10)

    # Define the columns
    tree.heading("Category", text="Category")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Availability", text="Availability")

    tree.column("Category", anchor=tk.W, width=130) 
    tree.column("Title", anchor=tk.W, width=479)     
    tree.column("Author", anchor=tk.W, width=130)   
    tree.column("Availability", anchor=tk.CENTER, width=115)  

    display_books_in_treeview(tree)
    


# Button functions
def view_books():
    reset_button_colors()
    view_books_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()
    ctk.CTkLabel(main_area_frame, 
    text="BOOK LISTS",
    fg_color='#DCDEDE',
    text_color='black',font=('Helvetica', 30)).pack(pady=10)
    database_treeview()


def borrow_book():
    reset_button_colors()
    borrow_book_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()

    ctk.CTkLabel(main_area_frame, 
                 text="BORROW A BOOK",
                 fg_color='#DCDEDE',
                 text_color='black',
                 font=('Helvetica', 30)).pack(pady=10)

    # Input fields
    ctk.CTkLabel(main_area_frame, text="Enter book title:", text_color="black").pack()
    book_title_entry = ctk.CTkEntry(main_area_frame, text_color="black",fg_color="white",placeholder_text="Book title",width=300)
    book_title_entry.pack(pady=(0, 10))
    
    ctk.CTkLabel(main_area_frame, text="Enter today's date:", text_color="black").pack()
    borrow_date_entry = ctk.CTkEntry(main_area_frame,fg_color="white", text_color="black",placeholder_text="YYYY-MM-DD",width=300)
    borrow_date_entry.pack(pady=(0, 20))

    # Borrow button logic
    def process_borrow_request():
        book_title = book_title_entry.get()
        borrow_date = borrow_date_entry.get()

        if not book_title or not borrow_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        global logged_in_student_id
        if logged_in_student_id is None:
            messagebox.showerror("Error", "No user is logged in.")
            return

        conn = sqlite3.connect("data_base.db")
        cursor = conn.cursor()

        try:
            # Check if the book exists
            cursor.execute("SELECT book_id, availability FROM books WHERE title = ?", (book_title,))
            book = cursor.fetchone()

            if book:
                book_id, availability = book
                if availability == "Available":
                    # Only insert a borrow request without changing availability
                    cursor.execute(
                        "INSERT INTO BorrowRequests (student_id, book_id, request_date) VALUES (?, ?, ?)",
                        (logged_in_student_id, book_id, borrow_date)
                    )
                    conn.commit()
                    messagebox.showinfo("Success", f"Borrow request for '{book_title}' has been submitted and awaits librarian approval.")
                else:
                    messagebox.showerror("Error", f"The book '{book_title}' is currently unavailable.")
            else:
                messagebox.showerror("Error", f"The book '{book_title}' does not exist in the library.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    # Attach borrow logic to the button
    ctk.CTkButton(main_area_frame, text="Borrow", text_color="white", fg_color='#A90503',
                  command=process_borrow_request).pack(pady=50)


def return_book():
    reset_button_colors()
    return_book_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()

    ctk.CTkLabel(main_area_frame, 
                 text="RETURN A BOOK", 
                 fg_color='#DCDEDE', 
                 text_color='black',
                 font=('Helvetica', 30)).pack(pady=10)

    # Return Book Input Fields
    ctk.CTkLabel(main_area_frame, text="Enter book title:", text_color="black").pack()
    book_title_entry = ctk.CTkEntry(main_area_frame, fg_color="white",text_color="black",placeholder_text="Book title", width=300)
    book_title_entry.pack(pady=(0, 10))

    ctk.CTkLabel(main_area_frame, text="Enter today's date:", text_color="black").pack()
    return_date_entry = ctk.CTkEntry(main_area_frame,fg_color="white", text_color="black",placeholder_text="YYYY-MM-DD", width=300)
    return_date_entry.pack(pady=(0, 20))

    # Return button logic
    def process_return_request():
        global logged_in_student_id
        book_title = book_title_entry.get()
        return_date = return_date_entry.get()

        if not book_title or not return_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if logged_in_student_id is None:
            messagebox.showerror("Error", "No user is logged in.")
            return

        conn = sqlite3.connect("data_base.db")
        cursor = conn.cursor()

        try:
            # Check if the book exists in BorrowedBooks
            cursor.execute(
                """SELECT BorrowedBooks.borrow_id, books.book_id
                    FROM BorrowedBooks
                    INNER JOIN books ON BorrowedBooks.book_id = books.book_id
                    WHERE books.title = ? AND BorrowedBooks.student_id = ?""",
                (book_title, logged_in_student_id)
            )
            record = cursor.fetchone()

            if record:
                borrow_id, book_id = record

                # Insert into ReturnRequests for librarian approval
                cursor.execute(
                    "INSERT INTO ReturnRequests (borrow_id, request_date) VALUES (?, ?)",
                    (borrow_id, return_date)
                )
                conn.commit()
                messagebox.showinfo("Success", f"The return request for '{book_title}' has been submitted. Awaiting librarian approval.")
            else:
                messagebox.showerror("Error", f"The book '{book_title}' is not currently borrowed by you.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    # Attach return logic to the button
    ctk.CTkButton(main_area_frame, text="Return", text_color="white", fg_color='#A90503',
                  command=process_return_request).pack(pady=50)



def view_borrowed_books():
    reset_button_colors()
    view_borrowed_books_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()

    ctk.CTkLabel(main_area_frame, 
                 text="VIEW BORROWED BOOKS", 
                 fg_color='#DCDEDE', 
                 text_color='black',
                 font=('Helvetica', 30)).pack(pady=10)

    # Create TreeView
    tree = ttk.Treeview(main_area_frame, columns=("Student Name", "Email", "Book Title", "Borrow Date"), show="headings")

    tree.heading("Student Name", text="Student Name")
    tree.heading("Email", text="Email")
    tree.heading("Book Title", text="Book Title")
    tree.heading("Borrow Date", text="Borrow Date")

  
    tree.column("Student Name", anchor="center", width=150)
    tree.column("Email", anchor="center", width=250)
    tree.column("Book Title", anchor="center", width=350)  
    tree.column("Borrow Date", anchor="center", width=150)
    tree.pack(fill="both", expand=True, pady=20, padx=10)

    # Fetch and display borrowed books
    def fetch_borrowed_books():
        conn = sqlite3.connect("data_base.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT Students.name, Students.email, Books.title, BorrowedBooks.date_borrowed 
                FROM BorrowedBooks
                INNER JOIN Students ON BorrowedBooks.student_id = Students.student_id
                INNER JOIN Books ON BorrowedBooks.book_id = Books.book_id
                """
            )
            records = cursor.fetchall()

            # Clear existing rows in TreeView
            for row in tree.get_children():
                tree.delete(row)

            # Insert new rows
            for record in records:
                tree.insert("", "end", values=record)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    fetch_borrowed_books()
    
def logout():
    reset_button_colors()
    logout_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()
    ctk.CTkLabel(main_area_frame,
                text="THANK YOU FOR USING THE LIBRARY APP", 
                fg_color='#DCDEDE', 
                text_color='black',
                font=("Helvetica",30)
                ).pack(pady=10)

    # Create Frame for logout confirmation
    def logout_frame_destroy():
        clear_main_area()
    #   logout_frame.destroy()
        image_frame()


    logout_frame = ctk.CTkFrame(main_area_frame,
                            width=400,
                            height=200, 
                            fg_color="#DCDEDE",
                            border_color="red", 
                            border_width=3)
    logout_frame.place(x=10, y=300)
    ctk.CTkLabel(logout_frame, 
                 text="Are you sure you want to \nLogout?", 
                 text_color="black", font=('Arial',25)).place(x=50, y=20)

    ctk.CTkButton(logout_frame, 
                  text="NO", 
                  width=80,
                  command=logout_frame_destroy,cursor='hand2').place(x=50, y= 150)
    
    ctk.CTkButton(logout_frame,
                  text="YES",
                  width=80,
                  command=show_login_screen,cursor='hand2').place(x=280, y= 150)    

# Librarian sidebar buttons --------------------------------------
def request_borrow_book(student_id, book_id, request_date):
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    # Check if book is available
    cursor.execute("SELECT availability FROM Books WHERE book_id = ?", (book_id,))
    book_status = cursor.fetchone()

    if book_status and book_status[0] == "Available":
        # Create a borrow request
        cursor.execute(
            "INSERT INTO BorrowRequests (student_id, book_id, request_date) VALUES (?, ?, ?)",
            (student_id, book_id, request_date)
        )
        # Update book availability
        cursor.execute("UPDATE Books SET availability = 'Not Available' WHERE book_id = ?", (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Borrow request submitted.")
    else:
        messagebox.showerror("Error", "Book is not available.")

    conn.close()

# Approve Borrow Request Logic
def approve_borrow_request(request_id, date_borrowed):
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    try:
        # Fetch request details
        cursor.execute("SELECT student_id, book_id FROM BorrowRequests WHERE request_id = ?", (request_id,))
        request = cursor.fetchone()

        if request:
            student_id, book_id = request

            # Add the borrow record to BorrowedBooks
            cursor.execute(
                "INSERT INTO BorrowedBooks (student_id, book_id, date_borrowed) VALUES (?, ?, ?)",
                (student_id, book_id, date_borrowed)
            )
            # Update the book's availability
            cursor.execute(
                "UPDATE Books SET availability = 'Not Available' WHERE book_id = ?", (book_id,)
            )
            # Delete the borrow request as it has been approved
            cursor.execute("DELETE FROM BorrowRequests WHERE request_id = ?", (request_id,))
            conn.commit()
            messagebox.showinfo("Success", "Borrow request approved. The book is now marked as Not Available.")
        else:
            messagebox.showerror("Error", "Request not found.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        conn.close()

# Return Request Logic
def request_return_book(borrow_id, request_date):
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    # Create a return request
    cursor.execute(
        "INSERT INTO ReturnRequests (borrow_id, request_date) VALUES (?, ?)",
        (borrow_id, request_date)
    )
    conn.commit()
    messagebox.showinfo("Success", "Return request submitted.")
    conn.close()

# Approve Return Request Logic
def approve_return_request(return_request_id):
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    # Fetch request details
    cursor.execute("SELECT borrow_id FROM ReturnRequests WHERE return_request_id = ?", (return_request_id,))
    request = cursor.fetchone()

    if request:
        borrow_id = request[0]
        # Fetch book ID from borrow record
        cursor.execute("SELECT book_id FROM BorrowedBooks WHERE borrow_id = ?", (borrow_id,))
        book = cursor.fetchone()

        if book:
            book_id = book[0]
            # Update book availability
            cursor.execute("UPDATE Books SET availability = 'Available' WHERE book_id = ?", (book_id,))
            # Remove borrow record
            cursor.execute("DELETE FROM BorrowedBooks WHERE borrow_id = ?", (borrow_id,))
            # Remove return request
            cursor.execute("DELETE FROM ReturnRequests WHERE return_request_id = ?", (return_request_id,))
            conn.commit()
            messagebox.showinfo("Success", "Return request approved.")
    else:
        messagebox.showerror("Error", "Request not found.")

    conn.close()

# Display Borrow Requests in TreeView
def display_borrow_requests(tree):
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    # Corrected SQL query
    cursor.execute("""
        SELECT BorrowRequests.request_id, Students.name, books.title, BorrowRequests.request_date 
        FROM BorrowRequests
        INNER JOIN Students ON BorrowRequests.student_id = Students.student_id
        INNER JOIN books ON BorrowRequests.book_id = books.book_id
    """)
    requests = cursor.fetchall()
    
    # Clear existing rows in treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert rows into treeview
    for request in requests:
        tree.insert("", "end", values=request)

    conn.close()

# Display Return Requests in TreeView
def display_return_requests(tree):
    conn = sqlite3.connect("data_base.db")
    cursor = conn.cursor()

    # Corrected SQL query
    cursor.execute("""
        SELECT ReturnRequests.return_request_id, Students.name, books.title, ReturnRequests.request_date
        FROM ReturnRequests
        INNER JOIN BorrowedBooks ON ReturnRequests.borrow_id = BorrowedBooks.borrow_id
        INNER JOIN Students ON BorrowedBooks.student_id = Students.student_id
        INNER JOIN books ON BorrowedBooks.book_id = books.book_id
    """)
    requests = cursor.fetchall()

    # Clear existing rows in treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert rows into treeview
    for request in requests:
        tree.insert("", "end", values=request)

    conn.close()


# borrow request
def borrow_request():
    reset_button_colors()
    borrow_request_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()

    ctk.CTkLabel(main_area_frame, text="BORROW REQUEST",
                 fg_color='#DCDEDE', text_color='black', font=('Helvetica', 30)).pack(pady=10)

    # Create TreeView
    tree = ttk.Treeview(main_area_frame, columns=("Request ID","Student Name", "Book Title", "Date"), show="headings")
    tree.heading("Request ID", text="Request ID")
    tree.heading("Student Name", text="Student Name")
    tree.heading("Book Title", text="Book Title")
    tree.heading("Date", text="Date")

    tree.column("Request ID", anchor="center", width=100)
    tree.column("Student Name", anchor="center", width=300)
    tree.column("Book Title", anchor="center", width=470)  
    tree.column("Date", anchor="center", width=150)
    tree.pack(fill="both", expand=True, pady=20, padx=10)

    # Approve and Cancel Buttons
    def approve_request():
        selected_item = tree.focus()
        if selected_item:
            request_id = tree.item(selected_item, "values")[0]
            date_borrowed = "2025-01-23"  
            approve_borrow_request(request_id, date_borrowed)
            display_borrow_requests(tree)
        else:
            messagebox.showerror("Error", "No request selected.")

    def cancel_request():
        selected_item = tree.focus()
        if selected_item:
            request_id = tree.item(selected_item, "values")[0]
            conn = sqlite3.connect("data_base.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM BorrowRequests WHERE request_id = ?", (request_id,))
            conn.commit()
            conn.close()
            display_borrow_requests(tree)
        else:
            messagebox.showerror("Error", "No request selected.")

    ctk.CTkButton(main_area_frame, text="Approve", command=approve_request, fg_color="#28A745", text_color="white").pack(side="left", padx=20, pady=10)
    ctk.CTkButton(main_area_frame, text="Cancel", command=cancel_request, fg_color="#DC3545", text_color="white").pack(side="right", padx=20, pady=10)

    # Display Borrow Requests in TreeView
    display_borrow_requests(tree)


# return request
def return_request():
    reset_button_colors()
    return_request_button.configure(fg_color="black", text_color="#ECC917")
    clear_main_area()

    ctk.CTkLabel(main_area_frame, text="RETURN REQUEST",
                 fg_color='#DCDEDE', text_color='black', font=('Helvetica', 30)).pack(pady=10)

    # Create TreeView
    tree = ttk.Treeview(main_area_frame, columns=("Request ID","Student Name", "Book Title", "Date"), show="headings")
    tree.heading("Request ID", text="Request ID")
    tree.heading("Student Name", text="Student Name")
    tree.heading("Book Title", text="Book Title")
    tree.heading("Date", text="Date")

    tree.column("Request ID", anchor="center", width=100)
    tree.column("Student Name", anchor="center", width=400)
    tree.column("Book Title", anchor="center", width=470)
    tree.column("Date", anchor="center", width=150)

    tree.pack(fill="both", expand=True, pady=20, padx=10)

    # Approve and Cancel Buttons
    def approve_request():
        selected_item = tree.focus()
        if selected_item:
            return_request_id = tree.item(selected_item, "values")[0]
            approve_return_request(return_request_id)
            display_return_requests(tree)
        else:
            messagebox.showerror("Error", "No request selected.")

    def cancel_request():
        selected_item = tree.focus()
        if selected_item:
            return_request_id = tree.item(selected_item, "values")[0]
            conn = sqlite3.connect("data_base.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ReturnRequests WHERE return_request_id = ?", (return_request_id,))
            conn.commit()
            conn.close()
            display_return_requests(tree)
        else:
            messagebox.showerror("Error", "No request selected.")

    ctk.CTkButton(main_area_frame, text="Approve", command=approve_request, fg_color="#28A745", text_color="white").pack(side="left", padx=20, pady=10)
    ctk.CTkButton(main_area_frame, text="Cancel", command=cancel_request, fg_color="#DC3545", text_color="white").pack(side="right", padx=20, pady=10)

    # Display Return Requests in TreeView
    display_return_requests(tree)

# return request



# Other Functions 

def clear_main_area():
    """Clears all widgets in the main area."""
    for widget in main_area_frame.winfo_children():
        widget.destroy()

def reset_button_colors():
    """Resets all sidebar button colors to the default state."""
    for button in sidebar_buttons:
        button.configure(fg_color="#ECC917", text_color="black")

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# The login screen
def show_login_screen():
    clear_window()

    # # Function to connect to the database
    def connect_to_db():
        return sqlite3.connect("data_base.db") 


    # Validate name and email
    def validate_name_and_email(name, email):
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        name_pattern = r'^[a-zA-Z\s.,]+$'

        errors = []
        if name == "":
            errors.append("• Name field is required.")
        elif not re.match(name_pattern, name):
            errors.append("• Name should only contain letters and spaces.")
        if email == "":
            errors.append("• Email field is required.")
        elif not re.match(email_pattern, email):
            errors.append("• Please enter a valid email address.")
        if errors:
            messagebox.showerror("Invalid Input", "\n".join(errors))
            return False
        return True

    # Login Frame
    login_frame = ctk.CTkFrame(root, fg_color="white")
    login_frame.pack(fill="both", expand=True)

    # Sidebar
    sidebar = ctk.CTkFrame(login_frame, width=320, height=700, fg_color="#DCDEDE")
    sidebar.pack_propagate(False)
    sidebar.pack(side="right", fill="both", ipady=10, ipadx=30, expand=True)

    # Sidebar Logo and Text
    pup_logo_path = "pngkey.com-phillies-logo-png-528919.png"
    pup_logo = ctk.CTkImage(dark_image=Image.open(pup_logo_path), size=(140, 140))
    ctk.CTkLabel(sidebar, text="", image=pup_logo, fg_color="#DCDEDE").pack(pady=(50, 40))

    ctk.CTkLabel(sidebar, text="PUP-PARANAQUE CITY",
                 font=("Arial", 20), fg_color="#DCDEDE",
                 text_color="red").pack()
    ctk.CTkLabel(sidebar, text="CAMPUS LIBRARY",
                 font=("Arial", 20), fg_color="#DCDEDE",
                 text_color="red").pack(pady=(0, 25))

    # Login Fields
    name_entry = ctk.CTkEntry(sidebar, font=("Arial", 17), placeholder_text="Name (Last, First M.I)",
                              corner_radius=5, fg_color="white", text_color="black",
                              placeholder_text_color="#706b61", height=33, border_color="#DCDEDE")
    name_entry.pack(pady=(50, 15), padx=10, fill="x")
    email_entry = ctk.CTkEntry(sidebar, font=("Arial", 17), placeholder_text="Email",
                               corner_radius=5, fg_color="white", text_color="black",
                               placeholder_text_color="#706b61", height=33, border_color="#DCDEDE")
    email_entry.pack(pady=(0, 20), padx=10, fill="x")

    # Login Button
    def login():
        global logged_in_student_id
        user_name = name_entry.get().strip()
        user_email = email_entry.get().strip()

        if validate_name_and_email(user_name, user_email):
            try:
                conn = sqlite3.connect("data_base.db")
                cursor = conn.cursor()

                # Check if the student exists
                cursor.execute("SELECT student_id FROM Students WHERE email = ?", (user_email,))
                existing_student = cursor.fetchone()

                if existing_student:
                    logged_in_student_id = existing_student[0]  # Set the logged-in student ID
                    messagebox.showinfo("Welcome Back", f"Welcome back, {user_name}!")
                else:
                    # Insert new student and get ID
                    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (user_name, user_email))
                    conn.commit()
                    logged_in_student_id = cursor.lastrowid  # Save the ID of the new student
                    messagebox.showinfo("Login Successful", f"Welcome, {user_name}!")

                conn.close()
                show_main_menu()

            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error during login: {e}")

    ctk.CTkButton(sidebar, text="Sign in", font=("Arial", 16),
                  fg_color="#0CC0DF", text_color="white",
                  height=30, command=login, cursor='hand2').pack(padx=10, fill="x")
                  

    # LIBRARIAN FUNCTION
    def librarian_login():
        frame_librarian = ctk.CTkFrame(right_side, width=300, height=320, fg_color="#DCDEDE")
        frame_librarian.pack(side="left", padx=100)

        def close():
            frame_librarian.destroy()
        
        def librarian_frame_signin():
                
            librarian_name = librarian_name_entry.get().strip()
            librarian_email = librarian_email_entry.get().strip()

            # Connect to the database
            conn = sqlite3.connect('data_base.db')
            cursor = conn.cursor()

            # Query to fetch librarian by email
            cursor.execute("SELECT * FROM Librarians WHERE email = ?", (librarian_email,))
            librarian = cursor.fetchone()

            if librarian is None:
                # No librarian with that email
                messagebox.showerror("Login Error", "Incorrect email. Access denied.")
                conn.close()
                return
            else:
                # Check if the name matches
                if librarian_name != librarian[1]:  # librarian[1] is the name from the DB
                    messagebox.showerror("Login Error", "Incorrect name. Access denied.")
                    conn.close()
                    return

            # If login is successful, proceed to show the librarian menu
            messagebox.showinfo("Login Successful", f"Welcome, {librarian_name}!")
            show_librarian_menu()  # Proceed to the librarian menu/dashboard

            conn.close()  # Close the connection after use


        ctk.CTkButton(frame_librarian, text="❌", 
        height=30, 
        cursor="hand2",
        text_color="red",
        fg_color="#DCDEDE", width=50,
        command=close).place(x=246, y=10)

        librarian_name_entry = ctk.CTkEntry(frame_librarian, font=("Arial", 15), placeholder_text="Name",
                              corner_radius=5, fg_color="white", text_color="black",
                              placeholder_text_color="#706b61", height=30, border_color="#DCDEDE", width=250)
        librarian_name_entry.place(x=20, y=100)
        librarian_email_entry = ctk.CTkEntry(frame_librarian, font=("Arial", 15), placeholder_text="Email",
                                    corner_radius=5, fg_color="white", text_color="black",
                                    placeholder_text_color="#706b61", height=30, border_color="#DCDEDE",width=250)
        librarian_email_entry.place(x=20, y=150)

        ctk.CTkButton(frame_librarian, text="Sign in", font=("Arial", 16),
                  fg_color="#0CC0DF", text_color="white",
                  height=30, command=librarian_frame_signin, cursor='hand2', width=250).place(x=20, y=220)

    ctk.CTkButton(sidebar, text="Librarian", font=("Arial", 16),
                  fg_color="#003785", text_color="white",
                  height=30, command=librarian_login, cursor='hand2').pack(pady=10, padx=10, fill="x")


    
    # Right Side Image
    right_side = ctk.CTkFrame(login_frame, width=1100, height=720)
    right_side.pack_propagate(False)
    right_side.pack(side="right", expand=True, fill="both")

    pup_image_path = "pup_image.jpeg"
    pup_image = ctk.CTkImage(dark_image=Image.open(pup_image_path), size=(1100, 700))
    ctk.CTkLabel(right_side, text="", image=pup_image, fg_color="#DCDEDE").place(relwidth=1, relheight=1)
   

    # PUP IMAGE
    # global pup_image
    pup_image_path = ("pup_image.jpeg")
    pup_image = ctk.CTkImage(dark_image=Image.open(pup_image_path), size=(1100,710))
    pup_image_label = ctk.CTkLabel(right_side, text="", image=pup_image, fg_color="#DCDEDE")
    pup_image_label.place(relwidth=1, relheight=1)  # Cover the frame completely



# The main content
def show_main_menu():
    clear_window()
    # Frame for main menu
    frame = ctk.CTkFrame(root, fg_color="#A90503")
    frame.pack(expand=True, fill='both')

    # Frame for buttons
    sidebar_frame = ctk.CTkFrame(frame, fg_color="#A90503", width=300)
    sidebar_frame.pack_propagate(False)
    sidebar_frame.pack(side='left', fill="both", expand=True)

      # PUP LOGO in FRAME BUTTONS
    pup_logo_path = ("pngkey.com-phillies-logo-png-528919.png")
    pup_logo = ctk.CTkImage(dark_image=Image.open(pup_logo_path), size=(120,120))
    pup_logo_label = ctk.CTkLabel(sidebar_frame, text="", image=pup_logo, fg_color="#A90503")
    pup_logo_label.pack(pady=(40, 30))

    # PUP Text
    ctk.CTkLabel(
        sidebar_frame, text="PUP PARANAQUE CITY", font=("Helvetica", 20)
    ).pack()
    ctk.CTkLabel(
        sidebar_frame, text="CAMPUS LIBRARY", font=("Helvetica", 20)
    ).pack(pady=(0, 35))

    # Initialize sidebar buttons
    global sidebar_buttons, view_books_button, borrow_request_button, borrow_book_button, return_book_button, view_borrowed_books_button, logout_button 
    sidebar_buttons = []

    view_books_button = ctk.CTkButton(
        sidebar_frame,
        text="View Books",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=view_books,
        cursor='hand2'
    )
    view_books_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(view_books_button)



    borrow_book_button = ctk.CTkButton(
        sidebar_frame,
        text="Borrow Book",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=borrow_book,
        cursor='hand2'
    )
    borrow_book_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(borrow_book_button)

    return_book_button = ctk.CTkButton(
        sidebar_frame,
        text="Return Book",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=return_book,
        cursor='hand2'
    )
    return_book_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(return_book_button)

    # view_borrowed_books_button = ctk.CTkButton(
    #     sidebar_frame,
    #     text="View Borrowed Books",
    #     font=("Lora", 18),
    #     fg_color="#ECC917",
    #     text_color="black",
    #     height=40,
    #     corner_radius=20,
    #     hover_color="#DCDEDE",
    #     command=view_borrowed_books,
    #     cursor='hand2'
    # )
    # view_borrowed_books_button.pack(pady=10, padx=20, fill="x")
    # sidebar_buttons.append(view_borrowed_books_button)

    logout_button = ctk.CTkButton(
        sidebar_frame,
        text="Log-out",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=logout,
        cursor='hand2'
    )

    logout_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(logout_button)

    # Frame for main area/right side
    global main_area_frame
    main_area_frame = ctk.CTkFrame(frame, width=1200, fg_color="#DCDEDE", height=750)
    main_area_frame.pack_propagate(False)
    main_area_frame.pack(side="right", expand=True, fill="both")
    
    global image_frame
    def image_frame():
        # Placeholder text on the main area
        # Load and resize the image for CTkImage
        image_path = ("pup_image.jpeg")
        # Create CTkImage for use in CTkLabel

        image2 = Image.open(image_path)
        login_img2 = ctk.CTkImage(dark_image=image2, size=(1200, 730))  # Define global image
        global main_area_text
        main_area_text = ctk.CTkLabel(
            main_area_frame, text="",image=login_img2, font=("Helvetica", 20), fg_color="#DCDEDE", text_color="black"
        )
        main_area_text.pack()
    image_frame()

# Page for Librarian ------------------------------------------------------------------------
def show_librarian_menu():
    clear_window()
    # Frame for main menu
    frame = ctk.CTkFrame(root, fg_color="#A90503")
    frame.pack(expand=True, fill='both')

    # Frame for buttons
    sidebar_frame = ctk.CTkFrame(frame, fg_color="#A90503", width=260)
    sidebar_frame.pack_propagate(False)
    sidebar_frame.pack(side='left', fill="both", expand=True)

      # PUP LOGO in FRAME BUTTONS
    pup_logo_path = ("pngkey.com-phillies-logo-png-528919.png")
    pup_logo = ctk.CTkImage(dark_image=Image.open(pup_logo_path), size=(120,120))
    pup_logo_label = ctk.CTkLabel(sidebar_frame, text="", image=pup_logo, fg_color="#A90503")
    pup_logo_label.pack(pady=(40, 30))

    # PUP Text
    ctk.CTkLabel(
        sidebar_frame, text="PUP PARANAQUE CITY", font=("Helvetica", 20)
    ).pack()
    ctk.CTkLabel(
        sidebar_frame, text="CAMPUS LIBRARY", font=("Helvetica", 20)
    ).pack(pady=(0, 35))

    # Initialize sidebar buttons
    global sidebar_buttons, view_books_button, borrow_request_button,  return_request_button, view_borrowed_books_button, logout_button 
    sidebar_buttons = []

    view_books_button = ctk.CTkButton(
        sidebar_frame,
        text="View Books",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=view_books,
        cursor='hand2'
    )
    view_books_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(view_books_button)



    borrow_request_button = ctk.CTkButton(
        sidebar_frame,
        text="Borrow request",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=borrow_request,
        cursor='hand2'
    )
    borrow_request_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(borrow_request_button)

    return_request_button = ctk.CTkButton(
        sidebar_frame,
        text="Return request",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=return_request,
        cursor='hand2'
    )
    return_request_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(return_request_button)

    view_borrowed_books_button = ctk.CTkButton(
        sidebar_frame,
        text="View Borrowed Books",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=view_borrowed_books,
        cursor='hand2'
    )
    view_borrowed_books_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(view_borrowed_books_button)

    logout_button = ctk.CTkButton(
        sidebar_frame,
        text="Log-out",
        font=("Lora", 18),
        fg_color="#ECC917",
        text_color="black",
        height=40,
        corner_radius=20,
        hover_color="#DCDEDE",
        command=logout,
        cursor='hand2'
    )

    logout_button.pack(pady=10, padx=20, fill="x")
    sidebar_buttons.append(logout_button)

    # Frame for main area/right side
    global main_area_frame
    main_area_frame = ctk.CTkFrame(frame, width=1000, fg_color="#DCDEDE", height=680)
    main_area_frame.pack_propagate(False)
    main_area_frame.pack(side="right", expand=True, fill="both")
    
    global image_frame
    def image_frame():
        # Placeholder text on the main area
        # Load and resize the image for CTkImage
        image_path = ("pup_image.jpeg")
        # Create CTkImage for use in CTkLabel

        image2 = Image.open(image_path)
        login_img2 = ctk.CTkImage(dark_image=image2, size=(1400, 730))  # Define global image
        global main_area_text
        main_area_text = ctk.CTkLabel(
            main_area_frame, text="",image=login_img2, font=("Helvetica", 20), fg_color="#DCDEDE", text_color="black"
        )
        main_area_text.pack()
    image_frame()        

root = ctk.CTk()
root.geometry('1350x680')
root.resizable(False,False)
database_initialization()

show_main_menu()
root.mainloop()