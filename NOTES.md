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


  - Step 8: Connected User to Department using ForeignKey.
  Learned one-to-many relationships and on_delete=SET_NULL.

  - Step 9: Created the Category model and connected it to
  Department using ForeignKey. Learned how categories
  support automatic complaint routing.


  - Step 10: Created the Product model to store software
  products. Learned BooleanField and how is_active
  helps deactivate products without deleting records.

  - Step 11: Created the Ticket model to store employee and
  customer complaints. Learned TextField, ForeignKey,
  status choices and auto_now_add. Added support for
  products not listed in the dropdown.


  - Step 12: Registered Department, Category, Product and Ticket
  in Django Admin. Learned how admin.site.register()
  makes database models manageable through Django's
  built-in administration interface.

  - Step 13: Created a Django superuser using createsuperuser.
  Learned that a superuser has full Django Admin permissions.
  The account is stored locally in SQLite.


  - Step 14: Started Django's development server using runserver.
  Logged into Django Admin with a superuser and verified
  that the registered models are accessible in the browser. 



  - Step 15: Registered the custom User model in Django Admin.
  Learned that role='admin' and is_superuser=True are separate.


  - Step 16: Added four support departments through Django Admin.
  Learned that models define tables, while Admin creates
  and manages actual database records.


  - Step 17: Added 12 complaint categories and mapped them
  to support departments. Learned that category records
  can define routing rules, while unrecognized categories
  can be reviewed manually.

        - Step 17.1: Customized CategoryAdmin using list_display,
        list_filter, search_fields and ordering to make
        complaint categories easier to manage.


- Step 18: Added three sample software products using Django Admin.
  Learned how Product records will support customer complaint
  submission and product-wise analytics.


  - Step 19: Created a test employee and sample complaint.
  Learned how Ticket uses ForeignKey relationships to
  connect Reporter, Category and Department records.


  - Step 20: Created a customer account and software complaint.
  Learned that one Ticket model supports both employee and
  customer complaints using the division field.


  - Step 21: Customized TicketAdmin to display reporter,
  division, category, department, status and creation time.
  Learned list_display, list_filter, search_fields and
  descending ordering in Django Admin.

  - Step 22: Created and tested a Django seed-data command.
  Learned BaseCommand, handle() and get_or_create().
  The initial database records can now be recreated automatically.


  Step 23: Planned the user-facing screens and navigation.
  Learned how role-based interfaces share reusable pages.


  - Step 24: Planned the shared layout and role-based navigation.
  Learned how a base template keeps common UI elements
  consistent across Django pages.



  - Step 25: Created a reusable base.html template using Bootstrap.
  Learned that Django template blocks allow multiple pages to
  share the same layout without repeating HTML.


- Step 26: Created the Django homepage using a view, URL
  routing, and template inheritance.
- Resolved TemplateDoesNotExist and verified the homepage
  using a fresh Django server process.

  - Step 27: Created a reusable CSS file for IssueInsight.
  Learned about Django static files, STATICFILES_DIRS,
  {% load static %}, and connecting CSS to templates.

  - Step 28: Created shared navigation with a top bar and sidebar.
  Learned Django template conditions, user roles, named URLs,
  and responsive Bootstrap columns.

  - Step 29: Tested Django's built-in authentication and sessions.
  Learned how Django identifies a logged-in user using
  a session cookie and the is_authenticated property.

  - Step 30: Created the IssueInsight login page using
  Django's built-in LoginView and AuthenticationForm.
  Learned POST requests, CSRF protection, login redirects,
  and how authentication creates user sessions.

  - Step 31: Implemented logout using Django's LogoutView.
  Learned how POST requests, CSRF protection, and
  session termination work during logout.

  - Step 32: Created CustomerRegistrationForm using Django's
  UserCreationForm. Learned form validation, Meta, clean_email(),
  and overriding save() to assign the customer role.

  - Step 33: Implemented and tested customer self-registration.
  Verified password validation, successful registration,
  customer role assignment and login.

  
- Step 34 (Part 1): Configured Django's Console Email Backend
  for local development.
  Learned how Django generates emails and displays them
  in the terminal without sending them to a real inbox.
  Tested email generation using send_mail().


          - Step 34 (Part 2): Created the Forgot Password request
          and confirmation pages using Django PasswordResetView.
          Learned about reset tokens, email-based password
          recovery, and generic confirmation messages.

          
        - Step 34 (Part 3): Completed the password reset workflow
          using Django's PasswordResetConfirmView and
          PasswordResetCompleteView.
          Learned how reset tokens are validated, how users set
          a new password, and how invalid or expired links are handled.
          Successfully tested password resetting and login.


          - Step 34 (Part 4): Configured Gmail SMTP with SSL on port 465.
          Stored credentials securely in local_secret.py.
          Resolved SMTP authentication errors and verified real email delivery.