# feedback-app 

## App Requirements

### Create User Model (models.py)
Developed User model for SQLAlchemy:
- username - a unique primary key that is no longer than 20 characters.
- password - a not-nullable column that is text
- email - a not-nullable column that is unique and no longer than 50 characters.
- first_name - a not-nullable column that is no longer than 30 characters.
- last_name - a not-nullable column that is no longer than 30 characters.

### Make a Base Template
Add a base template with slots for the page title and content. Your other templates should use this. 
