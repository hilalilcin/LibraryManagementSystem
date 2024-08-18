# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:18:40 2024

@author: hilal
"""

import sqlite3
from datetime import datetime



#Creating Database and tables
def create_database():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                    )
    ''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author_id INTEGER, 
                    available INTEGER DEFAULT 1, 
                    FOREIGN KEY (author_id) REFERENCES authors(id)
                    )
    ''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL
                    )
    ''')
    
    
    c.execute('''CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER, 
                    user_id INTEGER,
                    loan_date DATE,
                    return_date DATE,
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    )
    ''')
    
    conn.commit()
    print('Database and tables are created succesfully.')
    conn.close()
    


#Method to view books 
def view_books():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()
    
    c.execute('''
        SELECT books.id, books.title, authors.name AS author,books.available 
        FROM books
        JOIN authors ON books.author_id = authors.id
        ''')
        
    rows = c.fetchall() 
    
    print('\nBOOKS:')
    
    for row in rows:
        print(f"ID: {row[0]}, Title: {row[1]}, Author: {row[2]}, Available: {row[3]}")
        
    conn.close()
        
    
# Method to add books
def add_book():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()
    title = input('Please enter the title of the book:')
    author_name = input('Please enter the author name of the book:')
    
    # Checking Author Name
    c.execute('SELECT id FROM authors WHERE name = ?',(author_name,))
    author = c.fetchone()
    
    if author is None:
        c.execute('INSERT INTO authors (name) VALUES (?)',(author_name,)) 
        author_id = c.lastrowid
    else:
        author_id = author[0]
        
    
    c.execute('INSERT INTO books (title,author_id) VALUES (?,?)',(title,author_id))
    conn.commit()
    print('Book was added.')
    conn.close()

# Removing book
def remove_book():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()
    
    view_books()
    book_id = int(input('Please Enter the ID of the book you want to remove:'))
    c.execute('DELETE FROM books WHERE id = ?',(book_id,))
    conn.commit()
    print('Book was removed succesfully..')
    conn.close()   
    
# Adding Users 
def add_user():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()
    
    username = input('Please enter the name of User:')
    c.execute('INSERT INTO users (username) VALUES (?)',(username,)) 
    conn.commit()
    print('User was added succesfully.')
    conn.close() 
    
# Loaning Book
def loan_book():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()
    
    view_books()
    book_id = int(input('Please Enter the ID of the book you want to loan:'))
    username = input('Please enter the name of User:')
    c.execute('SELECT id FROM users WHERE username = ?',(username,))
    user = c.fetchone()
    
    if user is None:
        print('There is no user. Please first add a user')
        conn.close()
        return
    
    user_id = user[0]
    c.execute('UPDATE books SET available = 0 WHERE id = ?',(book_id,))
    loan_date = datetime.now().date()
    c.execute('INSERT INTO loans (book_id, user_id, loan_date) VALUES(?,?,?)',
              (book_id,user_id,loan_date))
    
    conn.commit()
    print('The book was loaned succesfully.')
    conn.close()
    

# Method to remove book
def return_book():
    conn = sqlite3.connect('library_management.db')
    c = conn.cursor()

    username = input("Please enter the user name: ")

    c.execute('''
        SELECT loans.id, books.title
        FROM loans
        JOIN books ON loans.book_id = books.id
        JOIN users ON loans.user_id = users.id
        WHERE users.username = ? AND loans.return_date IS NULL
    ''', (username,))

    loans = c.fetchall()

    if not loans:
        print("There is no book to remove.")
        conn.close()
        return

    print("\nBooks that need to be returned:")
    for loan in loans:
        print(f"Loan ID: {loan[0]}, Book Title: {loan[1]}")

    loan_id = int(input("Enter the Loan ID of the book you want to return: "))

    return_date = datetime.now().date()
    c.execute('UPDATE loans SET return_date = ? WHERE id = ?', (return_date, loan_id))
    c.execute('''
        UPDATE books
        SET available = 1
        WHERE id = (SELECT book_id FROM loans WHERE id = ?)
    ''', (loan_id,))

    conn.commit()
    print("The book was returned successfully.")
    conn.close()




def menu():
    while True:
        print("\nLibrary Management System")
        print("1. View Books")
        print("2. Add Book")
        print("3. Remove Book")
        print("4. Add User")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Exit")

        choice = input("Make your choice (1-7): ")

        if choice == '1':
            view_books()
        elif choice == '2':
            add_book()
        elif choice == '3':
            remove_book()
        elif choice == '4':
            add_user()
        elif choice == '5':
            loan_book()
        elif choice == '6':
            return_book()
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    create_database()
    menu() 