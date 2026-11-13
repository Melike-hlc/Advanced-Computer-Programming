BEGIN;

INSERT OR IGNORE INTO Courses (course_code, course_name, credits) VALUES
('CS101', 'Introduction to Programming', 4),
('MATH201', 'Linear Algebra', 3),
('PHY101', 'General Physics I', 4),
('ENG101', 'Academic English', 2),
('HIST102', 'Modern History', 3);

INSERT OR IGNORE INTO Students (first_name, last_name, email, enrollment_year) VALUES
('Ali', 'Yılmaz', 'ali.yilmaz@example.com', 2026),
('Ayşe', 'Demir', 'ayse.demir@example.com', 2026),
('Mehmet', 'Kaya', 'mehmet.kaya@example.com', 2025),
('Fatma', 'Çelik', 'fatma.celik@example.com', 2026),
('Mustafa', 'Şahin', 'mustafa.sahin@example.com', 2024),
('Zeynep', 'Yıldız', 'zeynep.yildiz@example.com', 2026),
('Ahmet', 'Özkan', 'ahmet.ozkan@example.com', 2025),
('Elif', 'Aydın', 'elif.aydin@example.com', 2026),
('Burak', 'Öztürk', 'burak.ozturk@example.com', 2024),
('Merve', 'Arslan', 'merve.arslan@example.com', 2025);

DELETE FROM Enrollments;
DELETE FROM Sections;

INSERT INTO Sections (section_id, course_id, section_number, semester, instructor_name) VALUES
(1, (SELECT course_id FROM Courses WHERE course_code = 'CS101'), 1, '2026-Güz', 'Dr. Ahmet Yılmaz'),
(2, (SELECT course_id FROM Courses WHERE course_code = 'CS101'), 2, '2026-Güz', 'Dr. Ayşe Kılıç'),
(3, (SELECT course_id FROM Courses WHERE course_code = 'MATH201'), 1, '2026-Güz', 'Prof. Mehmet Demir'),
(4, (SELECT course_id FROM Courses WHERE course_code = 'PHY101'), 1, '2026-Güz', 'Dr. Ali Can'),
(5, (SELECT course_id FROM Courses WHERE course_code = 'PHY101'), 2, '2026-Güz', 'Doç. Dr. Elif Kara');

WITH desired_enrollments (email, section_id) AS (
	VALUES
        ('ali.yilmaz@example.com', 1),
        ('ayse.demir@example.com', 1),
        ('mehmet.kaya@example.com', 1),
        ('fatma.celik@example.com', 1),
        ('mustafa.sahin@example.com', 2),
        ('zeynep.yildiz@example.com', 2),
        ('ahmet.ozkan@example.com', 2),
        ('ali.yilmaz@example.com', 3),
        ('elif.aydin@example.com', 3),
        ('burak.ozturk@example.com', 3),
        ('merve.arslan@example.com', 3),
        ('ayse.demir@example.com', 4),
        ('mustafa.sahin@example.com', 4),
        ('elif.aydin@example.com', 4),
        ('mehmet.kaya@example.com', 5),
        ('zeynep.yildiz@example.com', 5),
        ('burak.ozturk@example.com', 5)
)
INSERT INTO Enrollments (student_id, section_id)
SELECT Students.student_id, Sections.section_id
FROM desired_enrollments
JOIN Students ON Students.email = desired_enrollments.email
JOIN Sections ON Sections.section_id = desired_enrollments.section_id;

COMMIT;