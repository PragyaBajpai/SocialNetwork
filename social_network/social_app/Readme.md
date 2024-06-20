# Django API Project

This Django-based project contains API for user authentication, user search, and friend request management. 

It includes the following functionalities:
- User Signup
- User Login
------ Below API Required authentication Token -------
- User Search by Email or Name
- Sending, Accepting, and Rejecting Friend Requests
- Listing Friends
- Listing Pending Friend Requests

#Setup

## Prerequisites
- Python 3.6+
- Django 3.0+
- Django REST Framework

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/django-api-project.git
    cd django-api-project
    ```

2. Build Docker - docker build --no-cache --tag social_network .
3. Run the server - docker run --publish 8002:8000 social_network

# API Endpoints

## User Signup
- **URL**: `social_app/signup/`
- **Method**: POST
- **Payload**:
    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword",
        "username": "yourusername",
        "first_name": "FirstName",
        "last_name": "LastName"
    }
    ```
- **Response**:
    ```json
    {
        "message": "User created successfully"
    }
    ```

### User Login
- **URL**: `social_app/login/`
- **Method**: POST
- **Payload**:
    ```json
    {
        "email": "user@example.com",
        "password": "yourpassword"
    }
    ```
- **Response**:
    ```json
    {
        "refresh": "your-refresh-token",
        "access": "your-access-token"
    }
    ```

## USE THE ABOVE GENERATED ACCESS TOKEN AS BEARER TOKEN FOR REST OF THE API'S

### User Search
- **URL**: `social_app/user-search/`
- **Method**: GET
- **Query Params**: `search=<keyword>`
- **Response**:
    ```json
    [
        {
            "id": 1,
            "username": "username",
            "email": "user@example.com",
            "first_name": "FirstName",
            "last_name": "LastName"
        },
        ...
    ]
    ```

### Send Friend Request
- **URL**: `social_app/friend-request/`
- **Method**: POST
- **Payload**:
    ```json
    {
        "to_user_id": "username"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "from_user": 2,
        "to_user": 3,
        "status": "pending",
        "from_user_full_name": "ab c",
        "to_user_full_name": "ab c",
        "from_user_name": "rocky",
        "to_user_name": "rani",
        "created_at": "2024-06-20T10:30:00Z",
        "updated_at": "2024-06-20T10:30:00Z"
    }
    ```

### Accept/Reject Friend Request
- **URL**: `social_app/friend-request/<request_id>/`
- **Method**: PATCH
- **Payload**:
    ```json
    {
        "action": "accept"  // or "reject"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "from_user": 2,
        "to_user": 3,
        "status": "accepted",
        "from_user_full_name": "ab c",
        "to_user_full_name": "ab c",
        "from_user_name": "rani",
        "to_user_name": "rocky",
        "created_at": "2024-06-20T10:30:00Z",
        "updated_at": "2024-06-20T10:30:00Z"
    }
    ```

### List Friends
- **URL**: `social_app/friend-request/?action=list_friends`
- **Method**: GET
- **Response**:
    ```json
    [
        {
            "id": 3,
            "username": "friendusername",
            "email": "friend@example.com",
            "first_name": "FriendFirstName",
            "last_name": "FriendLastName"
        },
        ...
    ]
    ```

### List Pending Friend Requests
- **URL**: `social_app/friend-request/?action=list_pending_requests`
- **Method**: GET
- **Response**:
    ```json
    [
        {
            "id": 1,
            "from_user": 2,
            "to_user": 3,
            "status": "pending",
            "created_at": "2024-06-20T10:30:00Z",
            "updated_at": "2024-06-20T10:30:00Z"
        },
        ...
    ]
    ```