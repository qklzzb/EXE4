import sqlite3

# Create a database or connect to an existing one
conn = sqlite3.connect("library.db")

# Create tables if they don't exist
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                    BookID TEXT PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    ISBN TEXT,
                    Status TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    UserID TEXT PRIMARY KEY,
                    Name TEXT,
                    Email TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID TEXT PRIMARY KEY,
                    BookID TEXT,
                    UserID TEXT,
                    ReservationDate TEXT,
                    FOREIGN KEY (BookID) REFERENCES Books (BookID),
                    FOREIGN KEY (UserID) REFERENCES Users (UserID)
                )''')
conn.commit()


def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    cursor.execute("INSERT INTO Books VALUES (?, ?, ?, ?, ?)",
                   (book_id, title, author, isbn, status))
    conn.commit()


def find_book_details(book_id):
    cursor.execute('''SELECT Books.*, Reservations.UserID, Reservations.ReservationDate
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      WHERE Books.BookID = ?''', (book_id,))
    result = cursor.fetchone()
    if result:
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        if result[5]:
            print("Reserved by UserID:", result[5])
            print("Reservation Date:", result[6])
        else:
            print("Not reserved")
    else:
        print("Book not found")


def find_reservation_status(text):
    if text.startswith("LB"):
        cursor.execute("SELECT Status FROM Books WHERE BookID=?", (text,))
        result = cursor.fetchone()
        if result:
            print("Book Status:", result[0])
        else:
            print("Book not found")
    elif text.startswith("LU"):
        cursor.execute("SELECT BookID FROM Reservations WHERE UserID=?", (text,))
        results = cursor.fetchall()
        if results:
            print("Books reserved by UserID:")
            for row in results:
                print(row[0])
        else:
            print("User not found or has not reserved any books")
    elif text.startswith("LR"):
        cursor.execute('''SELECT Books.BookID, Books.Title, Reservations.ReservationID
                          FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          WHERE Reservations.ReservationID = ?''', (text,))
        result = cursor.fetchone()
        if result:
            print("BookID:", result[0])
            print("Title:", result[1])
            print("ReservationID:", result[2])
        else:
            print("Reservation not found")
    else:
        print("Invalid input")


def find_all_books():
    cursor.execute('''SELECT Books.*, Users.Name, Users.Email, Reservations.ReservationDate
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
    results = cursor.fetchall()
    for result in results:
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        print("Reserved by:", result[5])
        print("User Email:", result[6])
        print("Reservation Date:", result[7])
        print("=" * 30)


def update_book_details(book_id):
    new_status = input("Enter new status: ")
    cursor.execute("UPDATE Books SET Status=? WHERE BookID=?", (new_status, book_id))
    cursor.execute("UPDATE Reservations SET ReservationDate=NULL WHERE BookID=?", (book_id,))
    conn.commit()


def delete_book(book_id):
    cursor.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
    cursor.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
    conn.commit()


# User interface
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's details by BookID")
    print("3. Find reservation status")
    print("4. Find all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        book_id = input("Enter BookID: ")
        find_book_details(book_id)
    elif choice == "3":
        text = input("Enter BookID, UserID, ReservationID, or Title: ")
        find_reservation_status(text)
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        book_id = input("Enter BookID to update: ")
        update_book_details(book_id)
    elif choice == "6":
        book_id = input("Enter BookID to delete: ")
        delete_book(book_id)
    elif choice == "7":
        break

# Close the database connection
conn.close()
