-- Phone adding procedure
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook WHERE name = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;

-- Phone moving procedure
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM phonebook WHERE name = p_contact_name;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;
    
    UPDATE phonebook SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;

-- Advanced search function
CREATE OR REPLACE FUNCTION search_contacts_full(p_query TEXT)
RETURNS TABLE(
    contact_id INTEGER,
    contact_name VARCHAR,
    phones_text TEXT,
    contact_email VARCHAR,
    group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        pb.id,
        pb.name,
        STRING_AGG(DISTINCT ph.phone || ' (' || ph.type || ')', ', ') AS phones_text,
        pb.email,
        g.name AS group_name
    FROM phonebook pb
    LEFT JOIN phones ph ON pb.id = ph.contact_id
    LEFT JOIN groups g ON pb.group_id = g.id
    WHERE
        pb.name ILIKE '%' || p_query || '%' OR
        pb.email ILIKE '%' || p_query || '%' OR
        ph.phone ILIKE '%' || p_query || '%'
    GROUP BY pb.id, g.name;
END;
$$;