from django.db import migrations


FORWARD_SQL = """
CREATE TABLE IF NOT EXISTS uploaded_financial_data (
    id BIGSERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL,
    month VARCHAR(20) NOT NULL,
    year INTEGER NOT NULL,
    item VARCHAR(255) NOT NULL,
    revenue NUMERIC(14, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION manage_department(
    p_operation TEXT,
    p_dept_id BIGINT,
    p_dept_name TEXT,
    p_user_id INTEGER
)
RETURNS TABLE(message TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF UPPER(COALESCE(p_operation, '')) = 'CREATE' THEN
        INSERT INTO departments_department (name, is_active)
        VALUES (p_dept_name, TRUE);
        RETURN QUERY SELECT 'CREATE successful'::TEXT;

    ELSIF UPPER(COALESCE(p_operation, '')) = 'UPDATE' THEN
        UPDATE departments_department
        SET name = p_dept_name
        WHERE id = p_dept_id;
        RETURN QUERY SELECT 'UPDATE successful'::TEXT;

    ELSIF UPPER(COALESCE(p_operation, '')) = 'DEACTIVATE' THEN
        UPDATE departments_department
        SET is_active = FALSE
        WHERE id = p_dept_id;
        RETURN QUERY SELECT 'DEACTIVATE successful'::TEXT;

    ELSIF UPPER(COALESCE(p_operation, '')) = 'ACTIVATE' THEN
        UPDATE departments_department
        SET is_active = TRUE
        WHERE id = p_dept_id;
        RETURN QUERY SELECT 'ACTIVATE successful'::TEXT;

    ELSE
        RETURN QUERY SELECT 'Unknown operation'::TEXT;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_uploaded_data(
    p_department VARCHAR,
    p_month VARCHAR,
    p_year INTEGER,
    p_item VARCHAR,
    p_revenue NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO uploaded_financial_data (department, month, year, item, revenue)
    VALUES (p_department, p_month, p_year, p_item, p_revenue);
END;
$$;

CREATE OR REPLACE FUNCTION fetch_uploaded_data(
    p_department TEXT,
    p_month TEXT,
    p_year INTEGER
)
RETURNS TABLE (
    department VARCHAR,
    item VARCHAR,
    revenue NUMERIC,
    month VARCHAR,
    year INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.department, u.item, u.revenue, u.month, u.year
    FROM uploaded_financial_data AS u
    WHERE (p_department = 'all_departments' OR u.department = p_department)
      AND (p_month = 'all_months' OR u.month = p_month)
      AND (p_year = -1 OR u.year = p_year)
    ORDER BY u.year DESC, u.month, u.department, u.item;
END;
$$;

CREATE OR REPLACE VIEW uploaded_data AS
SELECT department, item, revenue, month, year
FROM uploaded_financial_data;
"""


REVERSE_SQL = """
DROP VIEW IF EXISTS uploaded_data;
DROP FUNCTION IF EXISTS fetch_uploaded_data(TEXT, TEXT, INTEGER);
DROP PROCEDURE IF EXISTS insert_uploaded_data(VARCHAR, VARCHAR, INTEGER, VARCHAR, NUMERIC);
DROP FUNCTION IF EXISTS manage_department(TEXT, BIGINT, TEXT, INTEGER);
DROP TABLE IF EXISTS uploaded_financial_data;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("departments", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(FORWARD_SQL, REVERSE_SQL),
    ]
