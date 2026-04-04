from connect import get_connection, close_connection

def call_search(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('search_contacts', (pattern,))
    results = cur.fetchall()
    cur.close()
    close_connection(conn)
    return results

def call_paginated(page, size):
    conn = get_connection()
    cur = conn.cursor()
    cur.callproc('get_contacts_paginated', (page, size))
    results = cur.fetchall()
    cur.close()
    close_connection(conn)
    return results

def call_upsert(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    close_connection(conn)

def call_bulk_insert(contacts):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s)", (contacts,))
    conn.commit()
    cur.close()
    close_connection(conn)

def call_delete(term):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact_by_term(%s)", (term,))
    conn.commit()
    cur.close()
    close_connection(conn)

def main():
    while True:
        print("PHONEBOOK")
        print("1. Search")
        print("2. Add 1 contact")
        print("3. Add more than 1 contact")
        print("4. Pagination")
        print("5. Delete")
        print("6. Exit")
        
        choice = input("Choose: ")
        
        if choice == "1":
            pattern = input("Pattern: ")
            for row in call_search(pattern):
                print(f"{row[0]}. {row[1]} - {row[2]}")
        
        elif choice == "2":
            call_upsert(input("Name: "), input("Phone: "))
            print("Done")
        
        elif choice == "3":
            contacts = []
            while True:
                name = input("Name (empty to stop): ")
                if not name:
                    break
                phone = input("Phone: ")
                contacts.append([name, phone])
            call_bulk_insert(contacts)
            print("Done")
        
        elif choice == "4":
            page = int(input("Page: "))
            size = int(input("Size: "))
            for row in call_paginated(page, size):
                print(f"{row[0]}. {row[1]} - {row[2]}")
        
        elif choice == "5":
            call_delete(input("Name or phone: "))
            print("Done")
        
        elif choice == "6":
            break

if __name__ == "__main__":
    main()