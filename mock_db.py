import sqlite3

def init_mock_db():
    conn = sqlite3.connect("company.db")
    cur = conn.cursor()
    
    # جداول مطابقة لتصميم المشروع
    cur.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY,
        name TEXT,
        office_id INTEGER,
        budget REAL
    )""")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        job_title TEXT,
        department_id INTEGER,
        manager_id INTEGER,
        hire_date TEXT,
        office_id INTEGER,
        status TEXT
    )""")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS salaries (
        salary_id INTEGER PRIMARY KEY,
        employee_id INTEGER,
        annual_salary REAL,
        currency TEXT,
        effective_date TEXT
    )""")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY,
        name TEXT,
        client_id INTEGER,
        department_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        budget REAL,
        status TEXT
    )""")

    # بيانات تجريبية سريعة
    cur.executemany("INSERT OR IGNORE INTO departments VALUES (?, ?, ?, ?)", [
        (1, "Engineering", 10, 500000),
        (2, "Product", 10, 300000),
        (3, "HR", 20, 150000)
    ])
    
    cur.executemany("INSERT OR IGNORE INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        (101, "Mostafa", "Sharara", "mostafa@example.com", "AI Engineer", 1, None, "2023-01-15", 10, "active"),
        (102, "Ahmed", "Ali", "ahmed@example.com", "Product Manager", 2, None, "2022-03-01", 10, "active"),
        (103, "Sara", "Hassan", "sara@example.com", "HR Specialist", 3, None, "2024-05-10", 20, "active")
    ])

    cur.executemany("INSERT OR IGNORE INTO salaries VALUES (?, ?, ?, ?, ?)", [
        (1, 101, 120000, "USD", "2024-01-01"),
        (2, 102, 130000, "USD", "2024-01-01"),
        (3, 103, 75000, "USD", "2024-01-01")
    ])

    conn.commit()
    conn.close()
    print("Test company.db created successfully!")

if __name__ == "__main__":
    init_mock_db()