# Backend API Usage Guide

This document describes how the Django backend API can be used by the frontend.

---

## Base URL

When running via Docker Compose:

- **Base URL:** `http://localhost:8000/`
- All auth/account endpoints are under: `http://localhost:8000/api/accounts/`

---

## Authentication Overview

The backend uses **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.

- After **registration** or **login**, the backend returns a pair of tokens:
  - `access`: short-lived token used in the `Authorization` header.
  - `refresh`: longer-lived token used to obtain a new access token.

- For **authenticated endpoints**, the frontend must send:

  ```http
  Authorization: Bearer <access_token>
  ```

---

## Endpoints Summary

All paths below are relative to `http://localhost:8000/api/accounts/`.

- **POST** `/register/` – Register a new user and receive JWT tokens.
- **POST** `/login/` – Log in with username and password, receive JWT tokens.
- **GET** `/availability/` – Check if username and/or email are available.
- **GET** `/me/` – Get the currently logged-in user profile (requires JWT).
- **POST** `/token/refresh/` – Refresh the access token using a refresh token.
- **GET** `/subjects/` – List all `Subject` records.
- **GET** `/courses/subject/<subject_id>/` – List courses for a given subject.
- **GET** `/courses/<course_id>/` – Get details of a specific course.

---

## 1. Register – `POST /register/`

Register a new user and get JWT tokens.

- **URL:** `POST http://localhost:8000/api/accounts/register/`
- **Body (JSON):**

  ```json
  {
    "user_name": "alice",
    "email": "alice@example.com",
    "password": "StrongPass123!",
    "License": "optional license string"
  }
  ```

- **Response (201):**

  ```json
  {
    "user": {
      "userID": "<uuid>",
      "user_name": "alice",
      "email": "alice@example.com",
      "License": "optional license string",
      "profile": {
        "score": 0,
        "rank": 99999,
        "login_streak_days": 0,
        "last_login_date": null
      }
    },
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
  ```

---

## 2. Login – `POST /login/`

Log in an existing user and get JWT tokens.

- **URL:** `POST http://localhost:8000/api/accounts/login/`
- **Body (JSON):**

  ```json
  {
    "user_name": "alice",
    "password": "StrongPass123!"
  }
  ```

- **Response (200):**

  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "user": {
      "userID": "<uuid>",
      "user_name": "alice",
      "email": "alice@example.com",
      "License": "optional license string",
      "profile": {
        "score": 0,
        "rank": 99999,
        "login_streak_days": 1,
        "last_login_date": "2025-01-01"
      }
    }
  }
  ```

- **Error (401):**

  ```json
  { "error": "Invalid credentials" }
  ```

---

## 3. Check Availability – `GET /availability/`

Check if a username and/or email are already used.

- **URL examples:**
  - `GET /availability/?user_name=alice`
  - `GET /availability/?email=alice@example.com`
  - `GET /availability/?user_name=alice&email=alice@example.com`

- **Response (200):**

  ```json
  {
    "user_name_available": false,
    "email_available": true
  }
  ```

- **Error (400) if no query params:**

  ```json
  { "detail": "Provide at least one of user_name or email query params." }
  ```

---

## 4. Current User – `GET /me/`

Get the currently authenticated user’s data.

- **URL:** `GET http://localhost:8000/api/accounts/me/`
- **Headers:**

  ```http
  Authorization: Bearer <access_token>
  ```

- **Response (200):** same `user` structure as in login/registration.

---

## 5. Refresh Token – `POST /token/refresh/`

Get a new access token using a refresh token.

- **URL:** `POST http://localhost:8000/api/accounts/token/refresh/`
- **Body (JSON):**

  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```

- **Response (200):**

  ```json
  {
    "access": "<new_access_token>"
  }
  ```

---

## 6. List Subjects – `GET /subjects/`

Returns all `Subject` records.

- **URL:** `GET http://localhost:8000/api/accounts/subjects/`

- **Response (200):**

  ```json
  [
    {
      "SubjectID": 1,
      "SubjectName": "Git",
      "SubjectDescription": "Version control system"
    },
    {
      "SubjectID": 2,
      "SubjectName": "Python",
      "SubjectDescription": "Programming language"
    }
  ]
  ```

---

## 7. List Courses by Subject – `GET /courses/subject/<subject_id>/`

Returns all courses belonging to a specific subject. Only course ID and title are returned (for listing).

- **URL pattern:**

  ```
  GET /courses/subject/<subject_id>/
  ```

  Example:

  ```
  GET http://localhost:8000/api/accounts/courses/subject/1/
  ```

- **Response (200):**

  ```json
  [
    {
      "CourseID": 1,
      "CourseTitle": "Intro to Git"
    },
    {
      "CourseID": 2,
      "CourseTitle": "Advanced Git"
    }
  ]
  ```

- If there are no courses for that subject, the API returns an empty array `[]`.

---

## 8. Get Course Detail – `GET /courses/<course_id>/`

Returns the full information about a single course.

- **URL pattern:**

  ```
  GET /courses/<course_id>/
  ```

  Example:

  ```
  GET http://localhost:8000/api/accounts/courses/1/
  ```

- **Response (200):**

  ```json
  {
    "CourseID": 1,
    "SubjectID": 1,
    "CourseTitle": "Intro to Git",
    "CourseDescription": "Learn Git basics.",
    "CourseDifficulty": 1
  }
  ```

- **Error (404) if course does not exist:**

  ```json
  { "detail": "Course not found." }
  ```

---

## 9. Notes for Frontend Implementation

- All JSON bodies should be sent with header:

  ```http
  Content-Type: application/json
  ```

- For authenticated endpoints like `/me/`, always include:

  ```http
  Authorization: Bearer <access_token>
  ```

- Tokens are obtained from the `/register/` or `/login/` responses.
- Error responses generally follow the pattern:

  ```json
  { "detail": "..." }
  ```

or

  ```json
  { "error": "..." }
  ```

The frontend should handle both success and error responses appropriately.

---

## 10. List Questions by Course – `GET /questions/course/<course_id>/`

Returns a list of question IDs that belong to a given course.

- **URL pattern:**

  ```
  GET /questions/course/<course_id>/
  ```

  Example:

  ```
  GET http://localhost:8000/api/accounts/questions/course/1/
  ```

- **Response (200):**

  ```json
  [1, 2, 3]
  ```

  This means questions with IDs 1, 2 and 3 all belong to course with ID 1.

---

## 11. Get Question Detail – `GET /questions/<question_id>/`

Returns the question and its options, but **does not** expose which option is correct.

- **URL pattern:**

  ```
  GET /questions/<question_id>/
  ```

  Example:

  ```
  GET http://localhost:8000/api/accounts/questions/1/
  ```

- **Response (200):**

  ```json
  {
    "QuestionID": 1,
    "CourseID": 2,
    "QuestionDescription": "What does Git do?",
    "options": [
      {
        "OptionID": 10,
        "OptionText": "Version control system"
      },
      {
        "OptionID": 11,
        "OptionText": "Text editor"
      },
      {
        "OptionID": 12,
        "OptionText": "Operating system"
      },
      {
        "OptionID": 13,
        "OptionText": "Web browser"
      }
    ]
  }
  ```

  Note: the backend does **not** include `CorrectOption` in this response so the frontend cannot see which answer is correct.

- **Error (404) if question does not exist:**

  ```json
  { "detail": "Question not found." }
  ```

