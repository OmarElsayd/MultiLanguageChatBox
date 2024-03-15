# Multi Language Chat Box

## Overview
The Multi-Language Chat Box (MLCB) is a comprehensive application designed to facilitate real-time communication across various languages, leveraging modern web technologies and machine learning for translation and interaction.

## Project Structure
```
Multi-Language Chat Box (MLCB)
│
├── .github/               - Contains GitHub Actions CI/CD configurations
│ └── workflows/           - Workflow definitions for GitHub Actions
│ └── github-ci.yml        - Defines the CI/CD pipeline for automated testing and deployment
│
├── .idea/                   - Configuration files for JetBrains IDEs like PyCharm
│ ├── .gitignore             - Specifies intentionally untracked files to ignore
│ ├── inspectionProfiles/    - Inspection profiles for code analysis
│ │ └── profiles_settings.xml       - Settings for code inspection profiles
│ ├── misc.xml                      - Miscellaneous IDE-specific settings
│ ├── modules.xml                   - Project modules information for the IDE
│ ├── MultiLanguageChatBox-master.iml - Project file for IDE, specifying project structure
│ └── workspace.xml                   - IDE workspace settings, including editor preferences
│
├── backend/             - Backend part of the project, containing all server-side code
│ ├── alembic/           - Alembic migration scripts for database versioning
│ │ ├── env.py           - Alembic environment configuration for running migrations
│ │ ├── README           - Documentation on how to use Alembic for migrations
│ │ ├── script.py.mako   - Mako template for generating Alembic migration files
│ │ └── versions/         - Contains individual migration scripts
│ │ ├── 098eec3c7abd_removingpasscode.py - Specific migration for removing a passcode field
│ │ └── 975af912aa7e_mlcbupdate.py       - Migration script for an update in MLCB
│ ├── src/                             - Source code of the backend application
│ │ ├── mlcb_services/                  - Core backend services and logic
│ │ │ ├── init.py                       - Initializes the mlcb_services package
│ │ │ ├── api/                          - API endpoints for the backend
│ │ │ │ ├── init.py                     - Initializes the API sub-package
│ │ │ │ ├── chat/                       - Chat-related API functionalities
│ │ │ │ │ ├── init.py                   - Initializes the chat sub-module
│ │ │ │ │ └── chat.py                   - Implements chat functionality
│ │ │ │ ├── login/                       - Login API functionalities
│ │ │ │ │ ├── init.py                    - Initializes the login sub-module
│ │ │ │ │ └── login.py                   - Handles user login
│ │ │ │ ├── mlcb_session/                - Session management APIs
│ │ │ │ │ ├── init.py                    - Initializes the session sub-module
│ │ │ │ │ └── mlcb_session.py            - Manages user sessions
│ │ │ │ ├── register/                    - Registration API
│ │ │ │ │ ├── init.py                    - Initializes the register sub-module
│ │ │ │ │ └── register.py                - Handles user registration
│ │ │ │ └── util/                        - Utility functions for APIs
│ │ │ │ ├── init.py                      - Initializes the utility sub-module
│ │ │ │ ├── email_service.py             - Email service functions
│ │ │ │ ├── mlcb_translate.py            - Translation services for MLCB
│ │ │ │ └── util.py                      - General utility functions
│ │ │ ├── config/                        - Configuration settings for the backend
│ │ │ │ ├── init.py                      - Initializes the config sub-package
│ │ │ │ ├── get_creds.py                 - Retrieves credentials for services
│ │ │ │ └── google_cloud_init.py         - Initialization for Google Cloud services
│ │ │ ├── db_engine/                     - Database engine configurations and session management
│ │ │ │ ├── init.py                      - Initializes the db_engine sub-package
│ │ │ │ ├── engine.py                    - Setup for the SQLAlchemy engine
│ │ │ │ └── session.py                    - Database session management
│ │ │ ├── db_models/                     - ORM models defining the database schema
│ │ │ │ ├── init.py                      - Initializes the db_models sub-package
│ │ │ │ ├── base.py                      - Base class for all ORM models
│ │ │ │ └── models.py                    - Defines specific database models
│ │ │ ├── dependency/                    - Dependency injection and utility classes
│ │ │ │ ├── init.py                      - Initializes the dependency sub-package
│ │ │ │ ├── exception_handler.py - Custom exception handling for the backend
│ │ │ │ ├── role_checker.py - Checks user roles for access control
│ │ │ │ └── user_checker.py - Verifies user information and permissions
│ │ │ ├── security_auth/ - Authentication and authorization mechanisms
│ │ │ │ ├── init.py - Initializes the security_auth sub-package
│ │ │ │ ├── auth_schema.py - Schemas for authentication data
│ │ │ │ └── jwt_auth.py - JWT authentication handling
│ │ │ └── util/ - Additional utility functions
│ │ │ ├── init.py - Initializes the util sub-package
│ │ │ ├── constant.py - Constants used across the backend
│ │ │ └── payloads.py - Defines data payloads for API communication
│ │ ├── main.py - Main entry point for the backend application
│ │ ├── requirements.txt - Lists all Python package dependencies
│ │ └── setup.py - Setup script for the backend application
│ ├── Dockerfile - Docker configuration for building the backend service
│ ├── alembic.ini - Configuration file for Alembic migrations
│ └── entrypoint.sh - Script that runs when the Docker container starts
│
├── frontend/ - Frontend part of the project, containing client-side code
│ ├── mlcb/ - Angular project for the frontend
│ │ ├── src/ - Source files for the Angular application
│ │ │ ├── app/ - Angular components, services, and modules
│ │ │ │ ├── api_services/ - Services for API interaction
│ │ │ │ │ ├── api.service.ts - Service for API calls
│ │ │ │ │ ├── before-unload.service.ts - Handles events before unloading the page
│ │ │ │ │ ├── note.service.ts - Service for managing notes
│ │ │ │ │ ├── speech.service.ts - Service for speech operations
│ │ │ │ │ └── web-socket.service.ts - WebSocket service for real-time communication
│ │ │ │ ├── authGuard/ - Authentication guards for route protection
│ │ │ │ │ └── auth-guard.service.ts - Service for guarding routes based on authentication
│ │ │ │ ├── home/ - Home module with related components
│ │ │ │ │ ├── dialog/ - Dialog components for chat interactions
│ │ │ │ │ │ ├── dialog.component.html - Markup for the dialog component
│ │ │ │ │ │ ├── dialog.component.scss - Styles for the dialog component
│ │ │ │ │ │ └── dialog.component.ts - Logic for the dialog component
│ │ │ │ │ ├── new-session/ - Components for creating new chat sessions
│ │ │ │ │ │ ├── new-session.component.html - Markup for new session creation
│ │ │ │ │ │ ├── new-session.component.scss - Styles for the new session component
│ │ │ │ │ │ └── new-session.component.ts - Logic for new session creation
│ │ │ │ │ ├── session-histroy/ - Components for displaying session history
│ │ │ │ │ │ ├── session-histroy.component.html - Markup for session history
│ │ │ │ │ │ ├── session-histroy.component.scss - Styles for session history
│ │ │ │ │ │ └── session-histroy.component.ts - Logic for session history management
│ │ │ │ │ ├── home.component.html - Markup for the home component
│ │ │ │ │ ├── home.component.scss - Styles for the home component
│ │ │ │ │ └── home.component.ts - Logic for the home component
│ │ │ │ ├── login/ - Login components and services
│ │ │ │ │ ├── login.component.html - Markup for the login component
│ │ │ │ │ ├── login.component.scss - Styles for the login component
│ │ │ │ │ ├── login.component.spec.ts - Test specifications for the login component
│ │ │ │ │ └── login.component.ts - Logic for the login component
│ │ │ │ ├── signup/ - Signup components and services
│ │ │ │ │ ├── signup.component.html - Markup for the signup component
│ │ │ │ │ ├── signup.component.scss - Styles for the signup component
│ │ │ │ │ └── signup.component.ts - Logic for the signup component
│ │ │ │ ├── app.component.html - Root component markup for the Angular app
│ │ │ │ ├── app.component.scss - Root component styles for the Angular app
│ │ │ │ ├── app.component.ts - Root component logic for the Angular app
│ │ │ │ ├── app.config.server.ts - Server-specific configuration for the Angular app
│ │ │ │ ├── app.config.ts - Client-specific configuration for the Angular app
│ │ │ │ ├── app.module.ts - Root module for the Angular app
│ │ │ │ └── app.routes.ts - Routing definitions for the Angular app
│ │ │ ├── assets/ - Static assets like images, icons, and styles
│ │ │ │ └── icons/ - Icon files used throughout the frontend
│ │ │ │ └── github.svg - GitHub icon used in the frontend
│ │ │ ├── environments/ - Environment-specific configurations for Angular
│ │ │ │ ├── environment.prod.ts - Production environment settings
│ │ │ │ └── environment.ts - Development environment settings
│ │ │ ├── favicon.ico - Favicon for the web application
│ │ │ ├── index.html - Entry HTML file for the Angular application
│ │ │ ├── main.server.ts - Entry point for Angular Universal (server-side rendering)
│ │ │ ├── main.ts - Main entry point for the Angular client-side application
│ │ │ └── styles.scss - Global styles for the Angular application
│ │ ├── angular.json - Angular CLI configuration file
│ │ ├── package.json - NPM package dependencies for the frontend
│ │ ├── server.ts - Server-side rendering setup for Angular Universal
│ │ ├── tsconfig.app.json - TypeScript configuration for the Angular app
│ │ ├── tsconfig.json - Root TypeScript configuration for the Angular project
│ │ └── tsconfig.spec.json - TypeScript configuration for Angular tests
│ └── Dockerfile - Docker configuration for building the frontend service
│
├── nginx/ - Nginx web server configuration for serving the frontend
│ └── nginx.conf - Main configuration file for Nginx
│
├── local/ - Contains scripts for local development and setup
│ └── install_dependencies/ - Scripts to install dependencies for the project
│ └── mlcb_backend_package.sh - Shell script to install backend dependencies
│
├── .dockerignore - Specifies patterns to ignore in Docker build context
├── .pylintrc - Configuration file for Python linting with Pylint
├── docker-compose.yaml - Defines and configures multi-container Docker applications
├── LICENSE - License file specifying the usage rights
└── README.md - Documentation of the project, describing its purpose and setup
```
