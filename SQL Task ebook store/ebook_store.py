# Import SQLite module
import sqlite3

# Define function to enter a book into the database
def enter_book():
    # Get the book id from the user
    # Loop until user provides the correct id
    id_check = False
    while id_check == False:
        # Error handling to make sure user enters an integer
        try:
            book_id = int(input("Please provide the id of the book you want to enter:"))
            id_check = True
            print("Valid id provided.")
            print("=" * 70)
        except ValueError:
            print("Incorrect id provided. Please try again.")
            id_check = False

    title_check = False
    # Get title name from user
    title_name = input("What is the title of the book?:\n")
    while title_check == False:
        # If less than 3 characters are entered then it is an invalid title
        if len(title_name) < 3:
            print("Invalid title provided. Please try again.")
            title_name = input("What is the title of the book?:\n")
        else:
            print("Valid title provided.")
            print("=" * 70)
            title_check = True
            
    author_check = False
    # Get author name from user
    author_name = input("Who is the author of the book?:\n")
    while author_check == False:
        # If less than 2 characters are entered then it is an invalid title
        if len(author_name) < 2:
            print("Invalid input provided. Please try again.")
            author_name = input("Who is the author of the book?:\m")
        else:
            print("Valid input provided.")
            print("=" * 70)
            author_check = True
            
    # Get the book quantity from the user
    # Loop until user provides a valid number
    qty_check = False
    while qty_check == False:
        try:
            qty = int(input("Please provide the amount of the books you want to enter:"))
            qty_check = True
            print("Valid quantity provided.")
            print("=" * 70)
        except ValueError:
            print("Incorrect input provided. Please try again.")
            qty_check = False

    # Register information to the database
    # Roll back if any information error is detected
    try:
        cursor.execute('''INSERT INTO ebookstore(id, Title, Author, Qty)
VALUES(?,?,?,?)''', (book_id, title_name, author_name, qty))
        db.commit()
        print("Data has been registered to the database.")
        print('=' *70)
    except Exception as e:
        print("DATA ERROR! Data has been rolled back. Please try entering data again.")
        print('=' * 70)
        db.rollback()

def update_book():
    # Get the the ID from the user
    # Validate user information for ID
    id_check = False
    while id_check == False:
        try:
            id_update = int(input("Provide ID of book you want to update:"))
            id_check = True
        except ValueError:
            print("Input provided is invalid. Please try again")
    # Provide a menu for the use to choose what they want to update
    while True:
        print("=" * 70)
        update_choice = input("""
What information do you want to update? Please select the number of your choice
1. Book Title
2. Book Author
3. Book Quantity
0. Exit
""")
        print("=" * 70)
        if update_choice == "1":
            # Get new title from user
            title_update = input("Please provide the new title:\n")
            # Update the database and roll back if something goes wrong
            try:
                cursor.execute('''UPDATE ebookstore SET Title = ? WHERE id = ?''',
                               (title_update, id_update))
                db.commit()
                print("Data has been updated.")
            except Exception as e:
                print("Could not update the data. Please try again")
                db.rollback()
        elif update_choice == '2':
            # Get new author from user
            author_update = input("Please provide the new author:\n")
            # Update the database and roll back if something goes wrong
            try:
                cursor.execute('''UPDATE ebookstore SET Author = ? WHERE id = ?''',
                               (author_update, id_update))
                db.commit()
                print("Data has been updated.")
            except Exception as e:
                print("Could not update the data. Please try again")
                db.rollback()
        
        # Update the quantity from user choice 
        elif update_choice == '3':
            # Get new quantity from user
            # Check if user enters a number
            qty_check = False
            while qty_check == False:
                try:
                    qty_update = int(input("Please provide the new quantity:\n"))
                    qty_check = True
                except ValueError:
                    print("Invalid input. Please try again.")
            # Update the database and roll back if something goes wrong
            try:
                cursor.execute('''UPDATE ebookstore SET Qty = ? WHERE id = ?''',
                               (qty_update, id_update))
                db.commit()
                print("Data has been updated.")
            except Exception as e:
                print("Could not update the data. Please try again")
                db.rollback()
                
        # Break out the loop when user want to exit
        elif update_choice == '0':
            break
        else:
            print("Invalid choice. Please try again")

def delete_book():
    # Get the the ID from the user that they want to delete
    # Validate user information for ID
    id_check = False
    while id_check == False:
        try:
            id_delete = int(input("Provide ID of book you want to delete:"))
            id_check = True
        except ValueError:
            print("Input provided is invalid. Please try again")

    # Delete the book the user has provided the ID for 
    cursor.execute('''DELETE FROM ebookstore WHERE id = ?''', (id_delete,))
    db.commit()
    print("Book as has been deleted from the database.")

def search_books():
    # Get the the ID from the user that they want to search
    # Validate user information for ID
    id_check = False
    while id_check == False:
        try:
            id_search = int(input("Provide ID of book you want to search:"))
            id_check = True
        except ValueError:
            print("Input provided is invalid. Please try again")

    # Search for the user selected book
    cursor.execute(''' SELECT * FROM ebookstore WHERE id = ?''', (id_search,))
    # save searched data to a variable
    books = cursor.fetchall()
    # Display all the books
    print("=" * 70)
    print("The Following book(s) were found:")
    for book in books:
        print(book)
    print("=" *70)

# Create/open database for the ebook data
db = sqlite3.connect('ebookstore_db')
# Get the cursor object
cursor = db.cursor()
# Create the table and check if it exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ebookstore(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
    ''')
# Commmit to the database
db.commit()

# Create list with books
books = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
         (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
         (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
         (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
         (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]
# Insert rows into the table
try:
    cursor.executemany('''INSERT INTO ebookstore(id, Title, Author, Qty) VALUES(?,?,?,?)''', books)

    db.commit()
# Catch the exception 
except Exception as e:
    print("Database already contains data. Rolling back default data registration.")
    # Roll back if something goes wrong
    db.rollback()

# Present user with options to use on the database
while True:
    action =(input('''
Welome to your E-bookstore database!
What would you like to do?
==================================================
1. Enter a book into the database.
2. Update information of an existing book.
3. Delete a book from the database.
4. Search for book(s)
0. Exit
==================================================
Please make your choice by giving the number of the option:'''))
    if action == '1':
        # Use function to enter a book into the database
        enter_book()
    elif action == '2':
        # Use function to update a book in the database
        update_book()
    elif action == '3':
        # Use function to delete a book into the database
        delete_book()
    elif action == '4':
        # Use function to search a book in the database
        search_books()
    elif action == '0':
        exit()
    else:
        print("Invalid choice. Please try again")
        
db.close()
