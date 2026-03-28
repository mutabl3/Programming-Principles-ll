import csv
from connect import get_connection, close_connection

#show
def show_all(cur):
    cur.execute("SELECT id, name, phone FROM phonebook ORDER BY name")
    rows = cur.fetchall()
    
    if not rows:
        print("\nPhonebook is empty")
    else:
        print("\nAll contacts:")
        for row in rows:
            print(f"{row[0]}. {row[1]} - {row[2]}")

#add manual
def add_manual(cur, conn):
    print("\n--- Add new contact ---")
    name = input("Enter name: ").strip()
    phone = input("Enter phone: ").strip()
    
    if not name:
        print("Error: invalid name (cannot be empty)")
        return
    if not phone:
        print("Error: invalid phone number (cannot be empty)")
        return
    
    try:
        cur.execute(
            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print(f"Contact {name} added!")
    except:
        print("Error: phone number already exists")
    print()

#add csv
def add_from_csv(cur, conn):
    filename = input("Enter CSV filename: ")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            count = 0
            for row in reader:
                if len(row) >= 2 and row[0].strip() and row[1].strip():
                    name, phone = row[0].strip(), row[1].strip()
                    try:
                        cur.execute(
                            "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                            (name, phone)
                        )
                        count += 1
                    except:
                        print(f"Skipped: {name} - phone already exists")
            conn.commit()
            print(f"Added {count} contacts")
    except FileNotFoundError:
        print("File not found")
    print()

#search
def search(cur):
    print("\n--- Search contact ---")
    print("1. Search by name")
    print("2. Search by phone prefix")
    print("3. Search by full phone number")
    choice = input("Choose (1/2/3): ")
    
    if choice == "1":
        name = input("Enter name (or part of name): ")
        cur.execute(
            "SELECT name, phone FROM phonebook WHERE name ILIKE %s",
            (f"%{name}%",)
        )
        rows = cur.fetchall()
        if rows:
            print("\nResults:")
            for row in rows:
                print(f"{row[0]} - {row[1]}")
        else:
            print("Nothing found")
    
    elif choice == "2":
        prefix = input("Enter phone prefix (e.g., 7707): ")
        cur.execute(
            "SELECT name, phone FROM phonebook WHERE phone LIKE %s",
            (f"{prefix}%",)
        )
        rows = cur.fetchall()
        if rows:
            print("\nResults:")
            for row in rows:
                print(f"{row[0]} - {row[1]}")
        else:
            print("Nothing found")
    
    elif choice == "3":
        phone = input("Enter full phone number: ")
        cur.execute(
            "SELECT name, phone FROM phonebook WHERE phone = %s",
            (phone,)
        )
        row = cur.fetchone()
        if row:
            print(f"\nFound: {row[0]} - {row[1]}")
        else:
            print("Nothing found")
    else:
        print("Invalid choice")
    print()

#update
def update(cur, conn):
    print("\n--- Update contact ---")
    search_term = input("Enter name or phone to search: ")
    
    cur.execute(
        "SELECT id, name, phone FROM phonebook WHERE name ILIKE %s OR phone = %s",
        (f"%{search_term}%", search_term)
    )
    rows = cur.fetchall()
    
    if not rows:
        print("Contact not found")
        return
    
    print("\nFound contacts:")
    for row in rows:
        print(f"{row[0]}. {row[1]} - {row[2]}")
    
    try:
        contact_id = int(input("\nEnter contact ID to update: "))
        cur.execute("SELECT name, phone FROM phonebook WHERE id = %s", (contact_id,))
        current = cur.fetchone()
        
        if not current:
            print("Contact not found")
            return
        
        new_name = input(f"New name (current: {current[0]}), press Enter to keep: ").strip()
        new_phone = input(f"New phone (current: {current[1]}), press Enter to keep: ").strip()
        
        if new_name:
            cur.execute("UPDATE phonebook SET name = %s WHERE id = %s", (new_name, contact_id))
        if new_phone:
            cur.execute("UPDATE phonebook SET phone = %s WHERE id = %s", (new_phone, contact_id))
        
        conn.commit()
        print("Contact updated!")
    except ValueError:
        print("Invalid ID")
    except:
        print("Error")
    print()

#delete
def delete(cur, conn):
    print("\n--- Delete contact ---")
    print("1. Delete by name")
    print("2. Delete by phone number")
    print("3. Delete by selecting from list")
    choice = input("Choose (1/2/3): ")
    
    if choice == "1":
        name = input("Enter name to delete: ").strip()
        if not name:
            print("Name cannot be empty")
            return
        
        cur.execute("SELECT id, name, phone FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
        rows = cur.fetchall()
        
        if not rows:
            print("Nothing found")
            return
        
        print("\nContacts found:")
        for row in rows:
            print(f"{row[0]}. {row[1]} - {row[2]}")
        
        confirm = input("Delete all found? (yes/no): ").lower().strip()
        if confirm == 'yes':
            cur.execute("DELETE FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
            conn.commit()
            print("Deleted")
    
    elif choice == "2":
        phone = input("Enter phone number to delete: ").strip()
        if not phone:
            print("Phone number cannot be empty")
            return
        
        cur.execute("SELECT id, name, phone FROM phonebook WHERE phone = %s", (phone,))
        row = cur.fetchone()
        
        if row:
            print(f"\nFound: {row[1]} - {row[2]}")
            confirm = input("Delete? (yes/no): ").lower().strip()
            if confirm == 'yes':
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
                conn.commit()
                print("Deleted")
        else:
            print("Contact not found")
    
    elif choice == "3":
        show_all(cur)
        try:
            contact_id = int(input("Enter contact ID to delete: "))
            cur.execute("SELECT id, name, phone FROM phonebook WHERE id = %s", (contact_id,))
            row = cur.fetchone()
            if not row:
                print("Contact not found")
                return
            
            print(f"\nFound: {row[1]} - {row[2]}")
            confirm = input("Delete? (yes/no): ").lower().strip()
            if confirm == 'yes':
                cur.execute("DELETE FROM phonebook WHERE id = %s", (contact_id,))
                conn.commit()
                print("Deleted")
        except ValueError:
            print("Invalid ID")
        except:
            print("Error")
    else:
        print("Invalid choice")
    print()

def main():
    conn = get_connection()
    cur = conn.cursor()
    
    while True:
        print("Commands: add, update, search, delete, show, exit")
        
        command = input("Enter command: ").lower().strip()
        
        if command == "add":
            print("\n1. Add manually")
            print("2. Add from CSV")
            sub = input("Choose (1/2): ")
            if sub == "1":
                add_manual(cur, conn)
            elif sub == "2":
                add_from_csv(cur, conn)
            else:
                print("Invalid choice")
        
        elif command == "update":
            update(cur, conn)
        
        elif command == "search":
            search(cur)
        
        elif command == "delete":
            delete(cur, conn)
        
        elif command == "show":
            show_all(cur)
        
        elif command == "exit":
            print("Goodbye!")
            break
        
        else:
            print("Unknown command. Try: add, update, search, delete, show, exit")
    
    cur.close()
    close_connection(conn)

if __name__ == "__main__":
    main()