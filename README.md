# feedback-app 

## App Requirements

### 1. Create User Model (models.py)
Developed User model for SQLAlchemy:
- username - a unique primary key that is no longer than 20 characters.
- password - a not-nullable column that is text
- email - a not-nullable column that is unique and no longer than 50 characters.
- first_name - a not-nullable column that is no longer than 30 characters.
- last_name - a not-nullable column that is no longer than 30 characters.
Added hashing BCrypt Functions for authentication

### 2. Make a Base Template
Add a base template with slots for the page title and content. Your other templates should use this. 


### 3. Make Routes For Users
Make routes for the following:
- GET / =  Redirect to /register.
- GET /register  =  Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name. Make sure you are using WTForms and that your password input hides the characters that the user is typing!
- POST /register  =  Process the registration form by adding a new user. Then redirect to /secret
- GET /login  =  Show a form that when submitted will login a user. This form should accept a username and a password. Make sure you are using WTForms and that your password input hides the characters that the user is typing!
- POST /login  =  Process the login form, ensuring the user is authenticated and going to /secret if so.
- GET /secret  =  Return the text “You made it!” (don’t worry, we’ll get rid of this soon)

### 4. Don’t let everyone go to /secret
Despite all of this wonderful password hashing that you have been doing, anyone can navigate to /secret and see the text “You made it!”. Let’s protect this route and make sure that only users who have logged in can access this route!

To do that, we’re going to make sure that when we log a user in (and after they register), we store just a little information in the session. When the user successfully registers or logs in, store the username in the session.

### 5. Log out users
Make routes for the following:

- GET /logout  = Clear any information from the session and redirect to /

### 6: Let’s change /secret to /users/<username>
Now that we have some logging in and and logging out working. Let’s add some authorization! When a user logs in, take them to the following route:

- GET /users/<username>  =  Display a template the shows information about that user (everything except for their password).  You should ensure that only logged in users can access this page.