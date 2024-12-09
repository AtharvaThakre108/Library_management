# Library_management
Library Management System API
Overview
The Library Management System API provides a backend service for managing library operations. It allows librarians to manage users and book borrow requests while enabling library users to request and view borrowing details.

Features
Librarian APIs
Create a New Library User
Add new users with an email and password, with an optional admin flag.

View All Book Borrow Requests
Retrieve all requests submitted by library users to borrow books.

Approve or Deny Borrow Requests
Approve or reject user requests for borrowing books based on availability.

View a User’s Book Borrow History
View the borrowing history of a specific user.

Library User APIs
Get List of Books
Retrieve a list of all books in the library.

Submit a Request to Borrow a Book
Request to borrow a book for specific dates, ensuring no overlap with other requests.

View Personal Borrow History
Access the borrowing history of the currently logged-in user.

Key Rules
Unique Book Borrowing

A book cannot be borrowed by more than one user during the same period.
Multiple copies of the same book are treated as unique items.
Authentication

Basic Authentication is used for securing all APIs.
Each user must provide valid credentials to access the API endpoints.
Edge Cases

Handle incomplete or invalid requests.
Ensure no overlapping borrow dates for the same book.
Reject requests for non-existent users or books.
