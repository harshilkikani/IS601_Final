<!--
NOTE: requirements.txt installation is still failing. The agent must carefully review all terminal errors and requirements.txt issues, and must read through this outline and the project conversation to ensure all steps are on track. If a terminal or dependency issue occurs, the agent must fully analyze the error and resolve it as a senior-level Fortune 500 software engineer would, before proceeding. This is a strict requirement for all future steps.
-->
# User Management System Final Project: Completion Outline
# For each task you complete, you will make sure to comment it out on this file.

# NOTE: From this point forward, all steps that can be automated or run by the agent will be done automatically without asking the user to perform manual actions, unless absolutely necessary. This includes running tests, installing dependencies, and updating files.

## 1. Project Preparation & Setup

# - **Create a local `.env` file** with your MailTrap SMTP settings for email testing.
# (COMPLETED: .env template created. Fill in your MailTrap credentials.)
# - **Database & Alembic:**
#   - Be aware that running pytest deletes the user table but not the Alembic table. If Alembic gets out of sync, drop the Alembic table and run migrations:
#     - `docker compose exec fastapi alembic upgrade head`
#   - If you change the DB schema, delete the Alembic migration, Alembic table, and users table, then regenerate migration:
#     - `docker compose exec fastapi alembic revision --autogenerate -m 'initial migration'`
# (COMPLETED: .env file is configured. Review Alembic and DB instructions above as needed.)
# - **Run the project:**
#   - `docker compose up --build`
#   - Set up PGAdmin at `localhost:5050` (see docker compose for login details)
#   - View logs: `docker compose logs fastapi -f`
#   - Run tests: `docker compose exec fastapi pytest`
# (COMPLETED: Project started with Docker Compose. PGAdmin and logs available. Ready for next steps.)
# - **DockerHub Deployment:**
#   - Set up DockerHub deployment as in previous assignments.
#   - Enable issues in settings, create the production environment, and configure your DockerHub username/token.
#   - Add MailTrap to production environment variables if desired.
# (COMPLETED: Docker image built, tagged, and pushed to DockerHub as hk453/my-qr-app:latest)

---

## 2. Project Requirements & Process

- **Select a Feature:**  
# (SELECTED: User Profile Management - allow users to update profile fields, managers/admins can upgrade users to professional status.)
- **Quality Assurance (QA):**
# (COMPLETED: 5 QA issues created and linked in GitHub.)
- **Test Coverage:**
# (COMPLETED: 10 new tests for User Profile Management added to test_api/test_users_api.py.)
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
