# IssueInsight Development Notes

- Step 1: Created the project workspace and
  initialized Git to track code changes.
- Step 2: Created a Python virtual environment to isolate project dependencies and configured Git to ignore local files.

- Step 3: Installed Django and created the project configuration.
  Learned that manage.py runs Django commands and config/ stores project settings.


- Step 4: Created and registered the tickets Django app.
  A project is the complete website; an app handles a specific
  part of its functionality.


  - Step 5: Created the accounts app and a custom User model
  using AbstractUser. Added Employee, Customer, Support Staff,
  and Admin roles. Configured AUTH_USER_MODEL so Django uses
  our custom model for authentication.


  - Step 6: Created and applied Django migrations.
  makemigrations generates database change instructions.
  migrate applies them to SQLite.


  - Step 7: Created the Department model.
  Learned how models.Model, CharField, unique=True
  and __str__ work. Created its SQLite table using migrations.

  - GitHub Setup Step 3: Moved Django's SECRET_KEY into a
  Git-ignored local file to keep it out of the repository.