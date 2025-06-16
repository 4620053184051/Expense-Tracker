
import mysql.connector
from datetime import datetime

# Establish connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KumaraSwamy@06",
)
cursor = conn.cursor()

# Create and use database
cursor.execute("CREATE DATABASE IF NOT EXISTS expense_db")
cursor.execute("USE expense_db")

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Expenses (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    category VARCHAR(50),
    amount DECIMAL(10,2),
    expense_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
)
""")

# Get user_id using email
def get_user_id_by_email(email):
    cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
    result = cursor.fetchone()
    return result[0] if result else None

# Add new user
def add_user():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    cursor.execute("INSERT INTO Users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    print("User added successfully.")

# Add new expense
def add_expense():
    email = input("Enter your email: ")
    user_id = get_user_id_by_email(email)
    if not user_id:
        print("User not found.")
        return
    category = input("Enter category: ")
    amount = float(input("Enter amount: "))
    date = input("Enter date (YYYY-MM-DD): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")  # validate date
        cursor.execute("INSERT INTO Expenses (user_id, category, amount, expense_date) VALUES (%s, %s, %s, %s)",
                       (user_id, category, amount, date))
        conn.commit()
        print("Expense added.")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# View expenses for a user
def view_expenses():
    email = input("Enter your email: ")
    user_id = get_user_id_by_email(email)
    if not user_id:
        print("User not found.")
        return
    cursor.execute("SELECT expense_id, category, amount, expense_date FROM Expenses WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    if results:
        print("\n--- Expense History ---")
        for row in results:
            print(f"ID: {row[0]} | Category: {row[1]} | Amount: ₹{row[2]} | Date: {row[3]}")
    else:
        print("No expenses found.")

# Monthly total summary
def monthly_summary():
    email = input("Enter your email: ")
    user_id = get_user_id_by_email(email)
    if not user_id:
        print("User not found.")
        return
    cursor.execute("""
    SELECT MONTH(expense_date), YEAR(expense_date), SUM(amount)
    FROM Expenses
    WHERE user_id = %s
    GROUP BY YEAR(expense_date), MONTH(expense_date)
    """, (user_id,))
    results = cursor.fetchall()
    if results:
        print("\n--- Monthly Summary ---")
        for row in results:
            print(f"Month: {row[1]}-{str(row[0]).zfill(2)} | Total: ₹{row[2]}")
    else:
        print("No data for summary.")

# Category-wise summary
def category_summary():
    email = input("Enter your email: ")
    user_id = get_user_id_by_email(email)
    if not user_id:
        print("User not found.")
        return
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM Expenses
    WHERE user_id = %s
    GROUP BY category
    """, (user_id,))
    results = cursor.fetchall()
    if results:
        print("\n--- Category Summary ---")
        for row in results:
            print(f"Category: {row[0]} | Total: ₹{row[1]}")
    else:
        print("No data for summary.")

# Update expense amount
def update_expense():
    expense_id = input("Enter the Expense ID to update: ")
    new_amount = float(input("Enter new amount: "))
    cursor.execute("UPDATE Expenses SET amount = %s WHERE expense_id = %s", (new_amount, expense_id))
    conn.commit()
    print("Expense updated.")

# Delete specific expense
def delete_expense():
    expense_id = input("Enter the Expense ID to delete: ")
    cursor.execute("DELETE FROM Expenses WHERE expense_id = %s", (expense_id,))
    conn.commit()
    print("Expense deleted.")

# Delete user and all their expenses
def delete_user():
    email = input("Enter your email to delete user: ")
    user_id = get_user_id_by_email(email)
    if not user_id:
        print("User not found.")
        return
    cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
    conn.commit()
    print("User and their expenses deleted.")

# Main menu
def main():
    while True:
        print("\n📊 --- Personal Expense Tracker ---")
        print("1. Add User")
        print("2. Add Expense")
        print("3. View Expenses")
        print("4. Monthly Summary 📅")
        print("5. Category Summary 📂")
        print("6. Update Expense ✏️")
        print("7. Delete Expense ❌")
        print("8. Delete User 👥❌")
        print("9. Exit 🚪")
        choice = input("Choose an option (1-9): ")

        if choice == "1":
            add_user()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_expenses()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            category_summary()
        elif choice == "6":
            update_expense()
        elif choice == "7":
            delete_expense()
        elif choice == "8":
            delete_user()
        elif choice == "9":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")

# Start program
main()

# Cleanup
cursor.close()
conn.close()
