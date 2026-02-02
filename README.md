# result-viewing

Project Description

The Online Result Viewing System is a secure web-based application developed using Python Flask that allows educational institutions to manage and publish student examination results efficiently. The system enables teachers to upload results directly from Google Sheets, while students can view their results online by entering their enrollment details.

The project eliminates manual result distribution, reduces errors, and provides a centralized, user-friendly platform for result management and viewing.

🎯 Objectives

To provide a digital platform for publishing and viewing student results

To allow teachers to upload and update results securely

To enable students to view results instantly using enrollment details

To maintain results in a structured database for quick access

System Features
Teacher Module

Secure teacher access using a teacher verification code

Upload results via Google Sheets URL

Automatic subject detection from the sheet

Update or overwrite previous results for a semester and department

Data stored securely in SQLite database

Student Module

Students can view results by entering:

Enrollment number

Department

Semester

Displays subject-wise marks

Shows student details such as name, exam name, and academic year

Technologies Used

Backend: Python, Flask

Database: SQLite

API Integration: Google Sheets API (gspread)

Frontend: HTML, CSS

Security: Environment variables (.env) for sensitive data

Authentication: Teacher code validation

Security Features

Sensitive data (teacher code, credentials) stored in environment variables

Teacher-only access to result upload functionality

Backend-only data processing to prevent unauthorized access

No exposure of API keys or credentials in frontend code

Database Design

The system stores results in a structured table containing:

Enrollment number

Student name

Department

Semester

Subject

Marks

Exam name

Academic year

This design allows efficient querying and accurate result retrieval.

Advantages

Paperless and time-saving result management

Easy result updates without manual data entry

Scalable for multiple departments and semesters

Simple and intuitive user interface

Future Enhancements

Student login system with authentication

Grade and percentage calculation

PDF result download option

Admin dashboard for monitoring results

Deployment on cloud platforms

Conclusion

The Online Result Viewing System provides a reliable, secure, and efficient solution for managing academic results. By integrating Google Sheets with a Flask backend, the system simplifies result handling while ensuring accuracy, security, and accessibility for both teachers and students
