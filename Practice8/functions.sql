CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(
    contact_id INTEGER,
    contact_name VARCHAR,
    contact_phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%'
    ORDER BY name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(
    page_number INTEGER,
    page_size INTEGER
)
RETURNS TABLE(
    contact_id INTEGER,
    contact_name VARCHAR,
    contact_phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, phone
    FROM phonebook
    ORDER BY id
    LIMIT page_size
    OFFSET (page_number - 1) * page_size;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION is_valid_phone(phone TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    IF phone ~ '^[0-9]{1,}$' THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;