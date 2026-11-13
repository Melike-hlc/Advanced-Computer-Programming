import sqlite3
from contextlib import closing
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI(title="Öğrenci Kayıt Sistemi API")

DB_NAME = Path(__file__).resolve().parent / "database" / "student.db"
STATIC_DIR = Path(__file__).resolve().parent / "static"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def read_index():
    return FileResponse(STATIC_DIR / "index.html")

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    enrollment_year: int

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

@app.get("/students/")
def get_students():
    with closing(get_db_connection()) as conn:
        students = conn.execute(
            "SELECT * FROM Students ORDER BY student_id"
        ).fetchall()
    return [dict(student) for student in students]


@app.get("/enrollments/")
def get_enrollments():
    with closing(get_db_connection()) as conn:
        enrollments = conn.execute(
            """
            SELECT
                Enrollments.enrollment_id,
                Sections.section_id,
                Students.student_id,
                Students.first_name,
                Students.last_name,
                Courses.course_code,
                Courses.course_name,
                Sections.section_number,
                Sections.semester,
                Sections.instructor_name
            FROM Enrollments
            JOIN Students ON Students.student_id = Enrollments.student_id
            JOIN Sections ON Sections.section_id = Enrollments.section_id
            JOIN Courses ON Courses.course_id = Sections.course_id
            ORDER BY Students.last_name, Students.first_name, Courses.course_code
            """
        ).fetchall()
    return [dict(enrollment) for enrollment in enrollments]


@app.post("/students/")
def create_student(student: StudentCreate):
    with closing(get_db_connection()) as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO Students (first_name, last_name, email, enrollment_year)
                VALUES (?, ?, ?, ?)
                """,
                (
                    student.first_name,
                    student.last_name,
                    student.email,
                    student.enrollment_year,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError as error:
            raise HTTPException(
                status_code=400,
                detail="Bu email adresi zaten kayıtlı.",
            ) from error

        new_student = conn.execute(
            "SELECT * FROM Students WHERE student_id = ?", (cursor.lastrowid,)
        ).fetchone()

    return {"message": "Öğrenci başarıyla eklendi.", "student": dict(new_student)}


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    with closing(get_db_connection()) as conn:
        try:
            cursor = conn.execute(
                """
                UPDATE Students
                SET first_name = ?, last_name = ?, email = ?, enrollment_year = ?
                WHERE student_id = ?
                """,
                (
                    student.first_name,
                    student.last_name,
                    student.email,
                    student.enrollment_year,
                    student_id,
                ),
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Öğrenci bulunamadı.")
            conn.commit()
        except sqlite3.IntegrityError as error:
            raise HTTPException(
                status_code=400,
                detail="Bu email adresi zaten kayıtlı.",
            ) from error

        updated_student = conn.execute(
            "SELECT * FROM Students WHERE student_id = ?", (student_id,)
        ).fetchone()

    return {"message": "Öğrenci bilgileri güncellendi.", "student": dict(updated_student)}


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with closing(get_db_connection()) as conn:
        cursor = conn.execute(
            "DELETE FROM Students WHERE student_id = ?", (student_id,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Öğrenci bulunamadı.")

    return {"message": f"{student_id} ID'li öğrenci başarıyla silindi."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)