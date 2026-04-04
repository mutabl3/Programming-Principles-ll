CREATE OR REPLACE PROCEDURE insert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE phonebook SET name = p_name WHERE phone = p_phone;
    
    IF NOT FOUND THEN
        INSERT INTO phonebook (name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    contacts_data TEXT[][]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    contact_name VARCHAR;
    contact_phone VARCHAR;
    invalid_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(contacts_data, 1) LOOP
        contact_name := contacts_data[i][1];
        contact_phone := contacts_data[i][2];
        
        IF NOT is_valid_phone(contact_phone) THEN
            invalid_data := invalid_data || format('Invalid phone: %s (%s); ', contact_name, contact_phone);
            CONTINUE;
        END IF;
        
        BEGIN
            INSERT INTO phonebook (name, phone) VALUES (contact_name, contact_phone);
        EXCEPTION 
            WHEN unique_violation THEN
                invalid_data := invalid_data || format('Duplicate phone: %s (%s); ', contact_name, contact_phone);
        END;
    END LOOP;
    
    IF invalid_data <> '' THEN
        RAISE NOTICE 'Errors: %', invalid_data;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by_term(
    search_term VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM phonebook WHERE name = search_term OR phone = search_term;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    IF deleted_count = 0 THEN
        RAISE NOTICE 'Contact not found: %', search_term;
    ELSE
        RAISE NOTICE 'Deleted % contact(s)', deleted_count;
    END IF;
END;
$$;