import psycopg2
import json
import os
from connect import get_connection

def run_query(sql, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        if fetch:
            result = cur.fetchall()
        else:
            conn.commit()
            result = None
    finally:
        cur.close()
        conn.close()
    return result

def list_contacts():
    page, size = 1, 5
    while True:
        rows = run_query("SELECT * FROM get_contacts_paginated(%s, %s)", (page, size), fetch=True)
        if not rows:
            print("\nNo contacts")
            break
        print(f"\n--- Page {page} ---")
        for r in rows:
            print(f"ID: {r[0]}, Name: {r[1]}, Phone: {r[2]}")
        cmd = input("\n[n]ext [p]rev [q]uit: ").lower()
        if cmd == 'n':
            page += 1
        elif cmd == 'p' and page > 1:
            page -= 1
        elif cmd == 'q':
            break

def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email (optional): ") or None
    birthday = input("Birthday (YYYY-MM-DD, optional): ") or None
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO phonebook (name, phone, email, birthday)
            VALUES (%s, %s, %s, %s)
        """, (name, phone, email, birthday))
        conn.commit()
        print("Contact added")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")
    try:
        run_query("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        print("Phone added")
    except Exception as e:
        print(f"Error: {e}")

def move_group():
    name = input("Contact name: ")
    group = input("Group name: ")
    try:
        run_query("CALL move_to_group(%s, %s)", (name, group))
        print("Contact moved")
    except Exception as e:
        print(f"Error: {e}")

def delete_contact():
    term = input("Enter name or phone to delete: ")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact_by_term(%s)", (term,))
        conn.commit()
        print("Contact deleted (if existed)")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()

def search():
    q = input("Search (name/email/phone): ")
    rows = run_query("SELECT * FROM search_contacts_full(%s)", (q,), fetch=True)
    if not rows:
        print("Not found")
    else:
        print("\n--- Results ---")
        for r in rows:
            print(f"ID: {r[0]}, Name: {r[1]}, Phones: {r[2]}, Email: {r[3]}, Group: {r[4]}")

def filter_group():
    group = input("Group name: ")
    rows = run_query("""
        SELECT pb.id, pb.name, pb.email 
        FROM phonebook pb
        JOIN groups g ON pb.group_id = g.id
        WHERE g.name = %s
    """, (group,), fetch=True)
    if not rows:
        print(f"No contacts in {group}")
    else:
        print(f"\n--- {group} ---")
        for r in rows:
            print(f"ID: {r[0]}, Name: {r[1]}, Email: {r[2]}")

def export_json():
    fname = input("JSON filename: ")
    rows = run_query("""
        SELECT pb.id, pb.name, pb.email, pb.birthday, 
               COALESCE(g.name, 'None') as grp,
               STRING_AGG(DISTINCT ph.phone || ':' || ph.type, ', ') as phones
        FROM phonebook pb
        LEFT JOIN groups g ON pb.group_id = g.id
        LEFT JOIN phones ph ON pb.id = ph.contact_id
        GROUP BY pb.id, g.name
    """, fetch=True)
    contacts = [{
        "id": r[0], "name": r[1], "email": r[2],
        "birthday": str(r[3]) if r[3] else None,
        "group": r[4], "phones": r[5].split(', ') if r[5] else []
    } for r in rows]
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(contacts)} contacts")

def import_json():
    fname = input("JSON filename: ")
    if not os.path.exists(fname):
        print("File not found")
        return
    with open(fname, 'r', encoding='utf-8') as f:
        contacts = json.load(f)
    conn = get_connection()
    cur = conn.cursor()
    for c in contacts:
        cur.execute("SELECT id FROM phonebook WHERE name = %s", (c['name'],))
        existing = cur.fetchone()
        if existing:
            choice = input(f"{c['name']} exists. [s]kip / [o]verwrite: ").lower()
            if choice == 's':
                continue
            elif choice == 'o':
                cur.execute("DELETE FROM phonebook WHERE id = %s", (existing[0],))
        cur.execute("INSERT INTO phonebook (name, email, birthday) VALUES (%s, %s, %s) RETURNING id",
                    (c['name'], c['email'], c['birthday']))
        cid = cur.fetchone()[0]
        for p in c['phones']:
            if ':' in p:
                phone, typ = p.rsplit(':', 1)
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                            (cid, phone.strip(), typ.strip()))
        if c['group'] and c['group'] != 'None':
            cur.execute("SELECT id FROM groups WHERE name = %s", (c['group'],))
            gid = cur.fetchone()
            if gid:
                cur.execute("UPDATE phonebook SET group_id = %s WHERE id = %s", (gid[0], cid))
            else:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (c['group'],))
                cur.execute("UPDATE phonebook SET group_id = %s WHERE id = %s", (cur.fetchone()[0], cid))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Imported {len(contacts)} contacts")

def import_csv():
    fname = input("CSV filename: ")
    if not os.path.exists(fname):
        print("File not found")
        return
    conn = get_connection()
    cur = conn.cursor()
    with open(fname, 'r', encoding='utf-8') as f:
        for line in f.readlines()[1:]:
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue
            name, phone = parts[0], parts[1]
            email = parts[2] if len(parts) > 2 and parts[2] else None
            birthday = parts[3] if len(parts) > 3 and parts[3] else None
            group = parts[4] if len(parts) > 4 and parts[4] else None
            try:
                cur.execute("INSERT INTO phonebook (name, phone, email, birthday) VALUES (%s, %s, %s, %s) RETURNING id",
                            (name, phone, email, birthday))
                cid = cur.fetchone()[0]
                if group:
                    cur.execute("SELECT id FROM groups WHERE name = %s", (group,))
                    gid = cur.fetchone()
                    if gid:
                        cur.execute("UPDATE phonebook SET group_id = %s WHERE id = %s", (gid[0], cid))
            except:
                pass
    conn.commit()
    cur.close()
    conn.close()
    print("CSV import done")

def main():
    menu = {
        '1': ("View all contacts (paginated)", list_contacts),
        '2': ("Add new contact", add_contact),
        '3': ("Add phone to contact", add_phone),
        '4': ("Move contact to group", move_group),
        '5': ("Search contacts", search),
        '6': ("Filter by group", filter_group),
        '7': ("Delete contact", delete_contact),
        '8': ("Export to JSON", export_json),
        '9': ("Import from JSON", import_json),
        '10': ("Import from CSV", import_csv),
    }
    while True:
        print("\n" + "=" * 40)
        print("PHONEBOOK EXTENDED")
        print("=" * 40)
        for k, (desc, _) in menu.items():
            print(f"{k}. {desc}")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == '0':
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()