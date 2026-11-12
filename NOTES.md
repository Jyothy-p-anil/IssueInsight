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


- Step 35: Implemented automatic welcome emails using Django's
  send_mail() and Gmail SMTP.
  Verified successful customer registration and welcome
  email delivery to the registered Gmail inbox.
  Learned to handle email failures using try/except and logging.


        - Step 36 (Part 2): Created a form for admin-managed
        Employee and Support Staff account creation.
        Added email validation, department validation and
        initial password protection.

        - Step 36 (Part 3): Connected StaffAccountCreationForm
        to Django Admin. Customized the Add User screen to
        collect username, email, role and department without
        requiring an administrator-set password.


      - Step 36 (Part 4): Implemented secure initial password setup
        emails for admin-created Employee and Support Staff accounts.
        Reused Django password reset tokens and confirmation views.
        Verified email delivery and password setup.


  - Step 37: Implemented and tested employee account
  deactivation and reactivation using Django's is_active.
  Verified login restrictions and both email notifications.

  - Step 38: Improved login error handling by displaying
  a clear Bootstrap alert when authentication fails.
  Verified incorrect-password and successful-login behavior.

  - Step 39 (Part 1): Created a reusable role_required
  decorator to restrict access by user role.
  Added permission-error messages to the shared template.
  Actual role-specific page testing follows in Part 2.



  - Step 39 (Part 2): Created role-specific dashboard entry
  pages and protected them using role_required().
  Verified that unauthorized users cannot open restricted
  pages by entering their URLs directly.

  - Step 39 (Part 3): Connected role-specific dashboard
  links to the shared sidebar. Employees, Customers,
  Support Staff and Admins now see their respective
  dashboard navigation. Superusers see Admin Dashboard.
  - Fixed logout navigation so users return to the
  IssueInsight login page instead of Django Admin's
  default logged-out page.


  - Step 40 (Parts 1–3): Created the IssueInsight Admin
  User Management page.
  Displays employee, customer and support staff details,
  including role, department and account status.
  Added sidebar navigation and verified admin-only access.

  - Step 40 (Part 5): Added search and filtering to
  Admin User Management. Admin can filter by username,
  name, email, role, department and account status.
  Supports combined filters and clearing filters.

  - Step 40 (Part 6A): Moved staff password setup email
  logic into a reusable service function.
  Updated Django Admin to use the shared function.
  Prepared the email workflow for in-app account creation.


  - Step 40 (Part 6B): Implemented Admin account creation
  inside IssueInsight. Reused the existing staff creation
  form and password setup email service.
  Verified account creation, email delivery, login,
  validation and admin-only access.

  - Step 40 (Parts 7A–7D): Implemented editing Employee,
  Customer and Support Staff details inside IssueInsight.
  Added duplicate-email validation and role-based
  department handling. Verified the Edit User workflow.

  - Step 40 (Part 8A): Moved account activation and
  deactivation email notifications into a shared service.
  Verified that Django Admin still sends both emails.
  Prepared the service for IssueInsight User Management.

    - Step 40 (Parts 8B–8C): Completed in-app user
  activation and deactivation using protected POST
  actions and reusable email notifications.
  Verified account status changes, login restrictions,
  and both activation and deactivation emails.

    - Step 41: Implemented Employee complaint submission
  and My Tickets, including automatic department routing,
  validation, role protection and ticket listing.

    - Step 42: Implemented Customer complaint submission
  and My Tickets inside IssueInsight.
  Added active product selection, unlisted product entry,
  customer category validation, automatic department
  routing, submission confirmation and protected ticket
  lists. Tested valid and invalid complaint submissions.

    - Step 43: Created a reusable Ticket Details page
  for Employee and Customer complaints.
  Displays complete complaint information, product
  or floor details, department, assigned support staff,
  status and submission date.
  Added View Details buttons to both My Tickets pages.
  Enforced ticket ownership to prevent unauthorized access.



    - Step 44: Implemented Support Staff Department Queue,
  Assigned Tickets and Support Ticket Details.
  Restricted ticket access by support department.
  Added secure ticket claiming with conflict protection.
  Claiming assigns the staff member and moves the ticket
  to In Progress without recording a human acknowledgement.
  Verified department isolation and ticket ownership.

    - Step 45: Implemented Admin manual complaint routing.
  Added Pending Routing, complaint review and department
  assignment. Verified Employee and Customer complaints
  move to the correct Support Staff department queue.

  - Step 46: Implemented ticket conversations with public
  messages and private Support Staff notes.
  Verified Employee-to-Support communication, public
  replies and internal note visibility.
  First-response tracking and remaining security checks
  require final verification.

    - Step 47: Added automated role-based permission tests
  using Django TestCase.
  Verified Employee, Customer, Support Staff and Admin
  access restrictions, ticket privacy, department
  isolation, ticket claiming and anonymous access.
  All seven permission tests passed.

  - Module 3 Completion Review:
  Completed core role-based access and permission controls.
  Verified existing protected workflows.
  New features will receive additional permission tests
  during their respective module development.






  =================================================================
  ## Module 3 — Role Permission Matrix

| Action                              | Employee | Customer | Support | Admin |
|---------------------------------------------------------------------------------
| Submit own complaint                | Yes      | Yes      | No      | No    |
| View own complaints                 | Yes      | Yes      | No      | No    |
| Send public messages on own tickets | Yes      | Yes      | No      | No    |
| View department ticket queue        | No       | No       | Yes     | No    |
| Claim department tickets            | No       | No       | Yes     | No    |
| Reply to assigned tickets           | No       | No       | Yes     | No    |
| Write internal ticket notes         | No       | No       | Yes     | No    |
| Manage user accounts                | No       | No       | No      | Yes   |
| Route pending complaints            | No       | No       | No      | Yes   |

Rules:
- All protected pages require authentication.
- Employees and Customers can access only their own tickets.
- Support Staff are restricted to their assigned department.
- Only the assigned Support Staff member can reply or add notes.
- Internal notes are hidden from complaint reporters.
- Admin manages users and manually routes pending complaints.
- Django superusers have elevated access, subject to
  applicable object-level restrictions.


  ==============================================================================


    - Step 48: Completed the Module 3 permission review.
  Documented the four-role permission matrix.
  Corrected unauthorized redirects to role dashboards.
  Added tests for identity spoofing, cross-account edits,
  department routing, assigned-ticket permissions and
  internal message privacy.

  - Module 3 Completion Review:
  Verified role-based access for currently implemented
  workflows. Future features will receive permission
  tests as they are developed.


    - Step 49: Organized the existing IssueInsight
  development history by creating MODULE_INDEX.md.
  Mapped all 15 modules to their relevant files,
  functions, classes and Git commits.
  Recorded module completion statuses to support
  structured learning in the Module Understanding chat.
  Preserved the existing Git history and project structure.

------------------------------------------------------------------

    - Step 50 (Module 4): Implemented Admin-only
  Department Management with department listing,
  creation, duplicate-name validation and role protection.
  Added four automated tests and verified the interface.
  Department editing and safe deletion remain pending.


    - Step 51 (Module 4): Implemented Admin-only
  department editing and safe deletion.
  Added duplicate-name validation during editing,
  deletion confirmation and dependency checks.
  Departments linked to Support Staff, categories
  or tickets cannot be deleted.
  Disabled department deletion through Django Admin.
  Added five automated tests and verified the workflows.

  - Step 52 (Module 4): Implemented Admin-only
  Category Management with category listing,
  creation, division selection and department mapping.
  Added duplicate-category validation within each
  division and preserved manual routing for Other.
  Applied the same form validation in Django Admin.
  Added seven automated tests and verified the page.
  Category editing and safe deletion remain pending.


    - Step 53 (Module 4): Implemented Admin-only
  category editing and safe deletion.
  Added protection for categories used by existing
  tickets, prevented complaint-type changes for
  referenced categories and protected Other.
  Disabled category deletion through Django Admin.
  Added seven automated tests and verified workflows.


    - Step 54 (Module 4): Implemented Admin-only
  Software Product Management with product listing,
  creation, active-status display and duplicate-name
  validation. Reused the existing Product model.
  Verified that new active products are available
  during Customer complaint submission.
  Added five automated tests and verified the UI.
  Product editing and activation/deactivation
  remain pending.


    - Step 55 (Module 4): Implemented Admin-only
  software product editing and activation/deactivation.
  Added protection against duplicate names during editing.
  Inactive products are excluded from new Customer
  Complaint forms while historical ticket references
  remain preserved. Disabled product deletion through
  Django Admin. Added seven automated tests and
  verified the workflows.


    - Step 56 (Module 4): Completed the Module 4
  integration and regression review.
  Verified Department, Category and Software Product
  management, role protection, dependency checks,
  manual routing rules and product activation.
  Confirmed all 47 automated tests passed.
  Verified no new database migrations were required.
  Updated MODULE_INDEX.md with implemented functions,
  files and Git history.

  - Module 4 Completion Review:
  Core Master Data Management is complete.
  Admin complaint visibility remains planned
  for Module 8, with search and filtering
  coordinated with Module 13.


    - Step 57 (Module 5): Completed Employee Complaint
  Submission review. Verified role protection,
  required-field validation, category restrictions,
  server-controlled ticket fields, automatic
  department routing and manual routing for Other.
  Corrected Employee My Tickets HTML structure.
  Added ten automated tests and verified
  the browser workflow.

  - Module 5 Completion Review:
  Employee Complaint Submission is complete
  for its current approved scope.
  Shared workplace issue verification remains
  scheduled for Module 10.
  Future ticket lifecycle features remain
  in their designated modules.

    - Step 58 (Module 5): Addressed Employee Complaint
  Submission checklist gaps. Added floor/location
  validation, category suggestion integration preparation,
  invalid/unmapped category handling tests, and
  shared-facilities and personal-device routing tests.
  Added eight automated tests.
  Final checklist verification pending Step 59.


    - Step 59 (Module 5): Completed the final
  Employee Complaint Submission checklist audit.
  Verified all 16 requirements (71–86) against
  implemented code and automated tests.
  Confirmed floor validation, category integration
  preparation, secure submission, automatic/manual
  routing and workplace complaint scenarios.
  Completed the final 65-test regression review.

  - Module 5 Final Completion:
  All approved Module 5 requirements are complete.
  Shared issue verification remains in Module 10,
  and AI classification remains in Module 11.

    - Step 60 (Module 6): Reviewed Customer complaint
  form, product selection, category restrictions and
  required-field validation. Reused the category
  suggestion candidate provider, corrected Customer
  My Tickets table structure and added nine tests.
  Remaining Module 6 security and edge-case checks
  were pending.

  - Step 61 (Module 6): Verified Customer submission
  security, server-controlled fields, invalid and inactive
  products, invalid and unmapped categories, Admin manual
  routing, ticket confirmation, and Customer privacy.
  Added ten automated tests.
  Final Module 6 checklist audit remains pending.

  - Step 62 (Module 6): Completed the final Customer
  Complaint Submission checklist audit.
  Verified all 16 requirements (87–102).
  Confirmed product selection, validation, reporter
  security, category restrictions, automatic/manual
  routing, ticket references and Customer privacy.
  All 84 regression tests passed.

  - Module 6 Final Completion:
  All approved Module 6 requirements are complete.
  AI category classification remains in Module 11.
  Later ticket lifecycle functionality remains
  in its designated modules.

    - Step 63 (Module 7): Reviewed reporter complaint
  detail pages and corrected HTML nesting.
  Verified Employee workplace information,
  Customer product details, assignment display,
  public conversation privacy, reporter access
  restrictions and reply availability.
  Added six automated tests.
  Module 7 remains in progress.

    - Step 64 (Module 7): Added basic status filtering
  to Employee and Customer My Tickets pages.
  Preserved reporter privacy and existing status
  values. Improved filtered empty states and
  responsive filter controls. Added seven tests.
  Module 7 final checklist review remains pending.


    - Step 65 (Module 7): Completed the remaining
  My Tickets and Complaint Details requirements.
  Added reporter ticket search by title/reference,
  submission date filtering, combined search/status/
  date filters, and latest-update tracking.
  Added an updated_at field and database migration.
  Improved the shared filter UI, responsive layouts,
  long-text handling, and available ticket history.
  Added eleven automated tests.

  - Step 66 (Module 7): Completed the final Module 7
  checklist audit. Verified all 17 requirements
  (103–119), including reporter privacy, ticket
  information, search, filters, timestamps, available
  history, empty states, and mobile usability.
  All 108 regression tests passed.

  - Module 7 Final Completion:
  All 17 approved Module 7 checklist requirements
  are complete.
  Ticket status-change history, resolution confirmation,
  closing, reopening and escalation remain in their
  designated later modules.


    - Step 71 (Module 8): Added the Admin All Complaints
  overview for Employee and Customer complaints.
  Displayed reporter, source, category, department,
  assignment, status and submission date.
  Preserved Pending Routing and existing Support Staff
  workflows. Added seven security and visibility tests.
  Module 8 remains in progress.


    - Step 72 (Module 8): Verified existing Support
  Staff department queues, assigned-ticket lists,
  complaint details and safe ticket claiming.
  Tested department isolation, role restrictions,
  POST-only claiming, status transitions from
  Submitted to In Progress, and prevention of
  duplicate claims. Added twelve automated tests.
  Module 8 remains in progress.


    - Step 73 (Module 8): Verified existing Admin
  manual routing for Employee and Customer complaints.
  Tested Pending Routing eligibility, valid department
  assignment, Support Staff queue visibility, invalid
  department submissions, unauthorized access, forged
  ticket fields and prevention of repeated routing.
  Confirmed that routing preserves the complaint status
  and does not automatically assign Support Staff.
  Added thirteen automated tests.
  Module 8 remains in progress.

    - Step 74 (Module 8): Reviewed the approved
  five-status complaint lifecycle without introducing
  new statuses or automatic transitions.
  Verified that the first public Support Staff reply
  records the first human acknowledgement.
  Confirmed that internal notes, reporter replies,
  blank messages and unauthorized replies do not
  record acknowledgement. Verified that later replies
  preserve the original first-response timestamp.
  Added nine automated tests.

  - Module 8 lifecycle decisions retained:
  Resolution must include a summary and history.
  Reporter confirmation and reopening are required.
  The precise 72-hour unconfirmed-resolution behavior
  must be verified before implementing automation.
  No complex SLA engine or specialist escalation system
  is included. Module 8 remains in progress.


  - Step 75 (Module 8): Implemented Support Staff
  complaint resolution using the existing Resolved
  status. Added mandatory resolution_summary and
  resolved_at fields to the Ticket model, together
  with a database migration.

  Added TicketResolutionForm, resolve_support_ticket
  view, POST-only resolution URL and resolution
  controls on the Support Staff ticket detail page.

  Restricted resolution to the assigned Support Staff
  member in the correct department for In Progress
  tickets. Prevented blank summaries, unauthorized
  resolution and repeated resolution attempts.

  Added resolution details to the reporter's ticket
  page. Added seven automated resolution tests.
  Corrected reporter template rendering after a
  failed visibility test.

  Reporter confirmation, reopening and the precise
  72-hour unconfirmed-resolution rule remain pending.
  Module 8 remains in progress.


  - Step 76A (Module 8): Added the reporter resolution
  confirmation view. The original Employee or Customer
  reporter can confirm a Resolved complaint, changing
  its status to Closed. The view uses POST-only access,
  ownership checks and conditional database updates.
  URL integration, interface and automated tests
  remain pending.


  - Step 76B (Module 8): Registered the reporter
  resolution confirmation URL. The endpoint connects
  to confirm_ticket_resolution and accepts POST
  requests through its view-level protection.
  Reporter interface and functional tests remain pending.


  - Step 76C (Module 8): Added a reporter-facing
  resolution confirmation form to the ticket detail
  page. The form appears for Resolved tickets and
  submits a CSRF-protected POST request to the
  confirmation endpoint. Verified that confirming
  resolution closes the ticket and removes the
  confirmation button. Resolution history visibility
  requires follow-up verification.


  - Step 76D (Module 8): Added seven automated tests
  for reporter resolution confirmation. Verified
  Employee and Customer confirmation, ticket ownership,
  Support Staff restrictions, POST-only access,
  prevention of unresolved-ticket confirmation and
  repeated confirmation protection.
  Full regression testing remains pending.



  - Step 76E (Module 8): Completed reporter resolution
  confirmation. Verified that Employee and Customer
  reporters can close their own Resolved tickets.
  Preserved the resolution summary after closure.
  Verified ownership protection, POST-only access,
  valid status transitions and duplicate confirmation
  prevention. Step 76 completed.
  Reporter reopening and unconfirmed-resolution
  handling remain pending.


  - Step 77B (Module 8): Added the reporter reopening
  view. Only the original Employee or Customer reporter
  can reopen a Resolved ticket using a valid reason.
  Reopening changes the status to Reopened, clears the
  assignment and records the reason as a public ticket
  message. URL, interface and automated tests remain
  pending.



  - Step 77C (Module 8): Registered the reporter
  reopening URL at /tickets/<ticket_id>/reopen/.
  The route connects to reopen_ticket, which accepts
  POST requests only. Reporter interface and
  automated tests remain pending.


  - Step 77E (Module 8): Added ten automated tests
  for reporter ticket reopening. Verified Employee
  and Customer access, ownership restrictions,
  POST-only access, mandatory reopening reasons,
  Resolved-only transitions, public reason recording,
  preservation of resolution history and prevention
  of duplicate reopening. Full regression testing
  remains pending.


  - Step 77F (Module 8): Completed reporter ticket
  reopening. Verified that Employee and Customer
  reporters can reopen their own Resolved tickets
  with a mandatory reason. Reopening clears the
  previous assignment, records the reason publicly
  and preserves the resolution summary and timestamp.
  Verified access restrictions, valid transitions,
  duplicate prevention and regression tests.
  Step 77 completed.
  Unconfirmed-resolution handling remains pending.
