SELECT
    student_id,
    first_name,
    last_name,
    email,
    enrollment_year
FROM Students
ORDER BY student_id;

SELECT
    course_id,
    course_code,
    course_name,
    credits
FROM Courses
ORDER BY course_id;

SELECT
    section_id,
    course_code,
    course_name,
    section_number,
    semester,
    instructor_name
FROM Sections
JOIN Courses ON Courses.course_id = Sections.course_id
ORDER BY semester, course_code, section_number;

SELECT
    Enrollments.enrollment_id,
    Students.first_name,
    Students.last_name,
    Courses.course_code,
    Courses.course_name,
    Sections.section_number,
    Sections.semester,
    Enrollments.registration_date
FROM Enrollments
JOIN Students ON Students.student_id = Enrollments.student_id
JOIN Sections ON Sections.section_id = Enrollments.section_id
JOIN Courses ON Courses.course_id = Sections.course_id
ORDER BY Students.last_name, Students.first_name, Courses.course_code;