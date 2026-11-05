
# IssueInsight — UI Plan

## 1. Authentication
- Login
- Customer registration
- Forgot password / Reset password
- Admin-managed user accounts
- Welcome and deactivation email workflows

## 2. Employee Portal
- Dashboard
- Submit workplace complaint
- My tickets
- Ticket details and replies

## 3. Customer Portal
- Dashboard
- Submit software complaint
- My tickets
- Ticket details and replies

## 4. Support Staff
- Department ticket queue
- Assigned tickets
- Ticket details and messages
- Claim, resolve and reopen workflow
- Needs Triage queue
- Similar tickets and past resolved fixes
- Incident management

## 5. Admin
- User and account management
- Departments and categories
- Products
- Complaint search, filters and CSV export

## 6. Analytics
- Floor-wise problem radar
- Product-wise complaint analytics
- Complaint spike alerts

## Design Guidelines
- Django Templates + Bootstrap
- Responsive layout
- Reuse common components
- Server-side permission checks
- Separate public replies and private notes
```



## Common Layout and Navigation

Layout:
- Top bar: Application name, notifications, profile, logout
- Sidebar: Navigation based on the logged-in user's role
- Main area: Page-specific content
- Mobile: Collapsible sidebar

Employee and Customer Navigation:
- Dashboard
- Submit Complaint
- My Tickets
- Profile

Support Staff Navigation:
- Dashboard
- Department Queue
- My Assigned Tickets
- Needs Triage (authorized staff)
- Incidents
- Profile

Admin Navigation:
- Dashboard
- Ticket Search and Reports
- Users
- Departments
- Categories
- Products
- Analytics
- Profile

Technical Approach:
- Reusable Django base template
- Bootstrap for responsive layouts
- Role-based navigation
- Server-side permission checks
