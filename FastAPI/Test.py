import sqlite3
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Öğrenci Kayıt Sistemi API")

DB_NAME = Path(__file__).resolve().parent / "database" / "student.db"

# Gelen veriyi doğrulamak için Pydantic modeli
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    enrollment_year: int

# Veritabanı bağlantısı için yardımcı fonksiyon
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

# 1. Tüm öğrencileri listele (GET)
@app.get("/students/")
def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    conn.close()
    return [dict(student) for student in students]

# 2. Yeni öğrenci ekle (POST)
@app.post("/students/")
def create_student(student: StudentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Students (first_name, last_name, email, enrollment_year)
            VALUES (?, ?, ?, ?)
        ''', (student.first_name, student.last_name, student.email, student.enrollment_year))
        conn.commit()
        new_id = cursor.lastrowid # Yeni eklenen öğrencinin ID'sini al
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="Bu email adresi zaten kayıtlı.")
    
    conn.close()
    return {"message": "Öğrenci eklendi", "student_id": new_id, "data": student}

# 3. Öğrenci sil (DELETE)
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı.")
        
    return {"message": f"{student_id} ID'li öğrenci başarıyla silindi."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)