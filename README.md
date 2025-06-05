## Requirements

You have been asked to design a system for handling events.
The frontend part was already developed.
You have to implement the database and the required APIs.

## Install and run

Create a new environment with virtualenv or conda. Activate it, then install the requirements using:
```shell
pip install -r requirements.txt
```

Run the application with:
```shell
fastapi dev
```

You can also run the `main.py` file as a script.

## Database
The system has a DB with 3 tables for storing events, users, and user registrations to events.
The latter is already implemented. You have to implement the ORM classes `User` and `Event` (NB: you must use exactly these names, otherwise it won't work!).

An event must be uniquely identified by its ID, which has to be automatically assigned by the system.
A user must be uniquely identified by their username, which will be set during the creation.

The code to initialize the DB and create the tables is already implemented.
Don't forget to import the classes associated with the tables in `data/db.py`, otherwise the net tables won't be created!

For the `date` attribute of the events table, you can use the datetime type:
```python
from datetime import datetime
```

## APIs
The system must provide the following APIs:
### /events
#### GET /events
Returns the list of existing events. Response format:
```json
[
  {
    "title": "string",
    "description": "string",
    "date": "2025-05-22T16:46:29.137Z",
    "location": "string",
    "id": 0
  }
]
```
#### POST /events
Creates a new event. Request format:
```json
{
  "title": "string",
  "description": "string",
  "date": "2025-05-22T16:55:14.958Z",
  "location": "string"
}
```
#### (optional) DELETE /events
Deletes all events.
#### GET /events/{id}
Returns the event with the given id. Response format:
```json
{
  "title": "string",
  "description": "string",
  "date": "2025-05-22T16:56:30.590Z",
  "location": "string",
  "id": 0
}
```
#### PUT /events/{id}
Updates an existing event. Request format:
```json
{
  "title": "string",
  "description": "string",
  "date": "2025-05-22T16:57:12.873Z",
  "location": "string"
}
```
#### (optional) DELETE /events/{id}
Deletes an existing event.
#### POST /events/{id}/register
Register a user to the given event. Request format:
```json
{
  "username": "string",
  "name": "string",
  "email": "string"
}
```
### /users
#### GET /users
Returns the list of existing users. Response format:
```json
[
  {
    "username": "string",
    "name": "string",
    "email": "string"
  }
]
```
#### POST /users
Creates a new user. Request format:
```json
{
  "username": "string",
  "name": "string",
  "email": "string"
}
```
#### (optional) DELETE /users
Deletes all users.
#### GET /users/{username}
Returns the user with the given username. Response format:
```json
{
  "username": "string",
  "name": "string",
  "email": "string"
}
```
#### (optional) DELETE /users/{username}
Deletes an existing user.
### /registrations
#### GET /registrations
Returns the list of existing registrations. Response format:
```json
[
  {
    "username": "string",
    "event_id": 0
  }
]
```
#### (optional) DELETE /registrations/?username={username}&event_id={event_id}
Deletes an existing registration.
