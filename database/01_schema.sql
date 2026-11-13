CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    enrollment_year INT
);

CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code VARCHAR(10) UNIQUE NOT NULL, -- Örn: CS101, MATH202
    course_name VARCHAR(100) NOT NULL,
    credits INT
);

CREATE TABLE Sections (
    section_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INT,
    section_number INT NOT NULL, -- Örn: 1, 2, 3 (Şube numarası)
    semester VARCHAR(20) NOT NULL, -- Örn: 2026-Güz
    instructor_name VARCHAR(100),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE,
    UNIQUE (course_id, section_number, semester) -- Aynı dönemde aynı dersin aynı şubesi açılamaz
);

CREATE TABLE Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    section_id INT,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES Sections(section_id) ON DELETE CASCADE,
    UNIQUE (student_id, section_id) -- Bir öğrenci aynı şubeye iki kez kaydolamaz
);