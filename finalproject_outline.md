# User Management System Final Project: Completion Outline

## 1. Project Preparation & Setup

- **Create a local `.env` file** with your MailTrap SMTP settings for email testing.
- **Database & Alembic:**
  - Be aware that running pytest deletes the user table but not the Alembic table. If Alembic gets out of sync, drop the Alembic table and run migrations:
    - `docker compose exec fastapi alembic upgrade head`
  - If you change the DB schema, delete the Alembic migration, Alembic table, and users table, then regenerate migration:
    - `docker compose exec fastapi alembic revision --autogenerate -m 'initial migration'`
- **Run the project:**
  - `docker compose up --build`
  - Set up PGAdmin at `localhost:5050` (see docker compose for login details)
  - View logs: `docker compose logs fastapi -f`
  - Run tests: `docker compose exec fastapi pytest`
- **DockerHub Deployment:**
  - Set up DockerHub deployment as in previous assignments.
  - Enable issues in settings, create the production environment, and configure your DockerHub username/token.
  - Add MailTrap to production environment variables if desired.

---

## 2. Project Requirements & Process

- **Select a Feature:**  
  - Choose one feature from `features.md` to implement (see section 3 below for options).
- **Quality Assurance (QA):**
  - Test major functionalities related to your feature.
  - Identify at least 5 issues/bugs, create detailed GitHub issues for each.
- **Test Coverage:**
  - Review existing tests, identify gaps.
  - Add 10 new tests covering edge cases, error scenarios, and important functionalities related to your feature (e.g., registration, login, authorization, DB interactions).
- **Feature Implementation:**
  - Implement your chosen feature, following project coding practices and architecture.
  - Write appropriate tests for your feature.
  - Document the feature: usage, configuration, migrations.
- **Documentation:**
  - Include links to closed issues for the 5 QA issues, 10 new tests, and your feature.
  - Include a link to your DockerHub repository.
- **Commit History:**
  - Maintain a consistent commit history (minimum 10 commits).
  - Use issues, commits, and a professional development process.
- **Deployability:**
  - Ensure the project deploys to DockerHub and passes all automated tests on GitHub Actions.
  - The main branch must always be deployable.

---

## 3. Feature Options (Choose One)

**(Summarized, see `features.md` for full details and requirements)**

1. **Profile Picture Upload with Minio**
   - API for uploading profile pictures, store in Minio, update user profile with picture URL.

2. **Event-Driven Email Notifications (Celery + Kafka)**
   - Refactor email notifications to use Celery tasks and Kafka for event processing.

3. **User Search and Filtering**
   - Add search/filtering to user management (by username, email, role, etc.).

4. **RBAC Enhancements**
   - Allow admins to change user roles dynamically, log changes.

5. **Event Management (BREAD)**
   - Full event management system (Browse, Read, Edit, Add, Delete) for managers/admins.

6. **Localization Support**
   - Add multi-language support and allow users to switch languages.

7. **User Retention Analytics**
   - Track/analyze user engagement, retention, and conversion rates.

8. **QR Code Generation User Invites with Minio**
   - Invite users via email with QR codes, track invites, store QR codes in Minio.

9. **User Profile Management**
   - Allow users to update profile fields, managers/admins can upgrade users to professional status.

10. **Admin Console Application**
    - CLI for admin tasks: drop tables, change roles, upload CSVs for user creation.

---

## 4. Best Practices & Methodology

- Follow the 12-Factor App methodology (see about.md for details).
- Adhere to coding standards and conventions.
- Write clear documentation for all new features and changes.
- Implement error handling, data validation, and security.
- Conduct thorough testing (unit and integration).
- Seek feedback and iterate as needed.

---

## 5. Submission Checklist

- [ ] `.env` file created and configured.
- [ ] Project runs locally and via Docker.
- [ ] Feature selected and fully implemented.
- [ ] At least 5 QA issues created and closed (with links).
- [ ] At least 10 new tests added and closed (with links).
- [ ] Feature documented (usage, config, migrations).
- [ ] Project deployed to DockerHub (link included).
- [ ] Commit history shows consistent, professional development.
- [ ] All tests pass on GitHub Actions.
- [ ] Main branch is always deployable.

---

*Use this file to track and check off each requirement as you complete your project.*
