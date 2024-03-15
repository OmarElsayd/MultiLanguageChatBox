# Multi Language Chat Box


```
Multi-Language Chat Box (MLCB)
│
├── .github/
│   └── workflows/
│       └── github-ci.yml            - CI/CD workflow for GitHub Actions
│
├── backend/
│   ├── alembic/
│   │   ├── env.py                   - Alembic environment script
│   │   ├── README                  - Alembic README
│   │   ├── script.py.mako          - Alembic script generation template
│   │   └── versions/
│   │       ├── 098eec3c7abd_removingpasscode.py
│   │       └── 975af912aa7e_mlcbupdate.py
│   ├── src/
│   │   ├── mlcb_services/
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── chat.py
│   │   │   │   ├── login/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── login.py
│   │   │   │   ├── mlcb_session/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── mlcb_session.py
│   │   │   │   ├── register/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── register.py
│   │   │   │   └── util/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── email_service.py
│   │   │   │       ├── mlcb_translate.py
│   │   │   │       └── util.py
│   │   │   ├── config/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── get_creds.py
│   │   │   │   └── google_cloud_init.py
│   │   │   ├── db_engine/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── engine.py
│   │   │   │   └── session.py
│   │   │   ├── db_models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   └── models.py
│   │   │   ├── dependency/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── exception_handler.py
│   │   │   │   ├── role_checker.py
│   │   │   │   └── user_checker.py
│   │   │   ├── security_auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth_schema.py
│   │   │   │   └── jwt_auth.py
│   │   │   └── util/
│   │   │       ├── __init__.py
│   │   │       ├── constant.py
│   │   │       └── payloads.py
│   │   ├── main.py                  - Main application entry point
│   │   ├── requirements.txt         - Python package dependencies
│   │   └── setup.py
│   ├── Dockerfile                   - Docker configuration for backend
│   ├── alembic.ini                  - Alembic configuration file
│   └── entrypoint.sh                - Entry point script for Docker
│
├── frontend/
│   ├── mlcb/
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api_services/
│   │   │   │   │   ├── api.service.ts
│   │   │   │   │   ├── before-unload.service.ts
│   │   │   │   │   ├── note.service.ts
│   │   │   │   │   ├── speech.service.ts
│   │   │   │   │   └── web-socket.service.ts
│   │   │   │   ├── authGuard/
│   │   │   │   │   └── auth-guard.service.ts
│   │   │   │   ├── home/
│   │   │   │   │   ├── dialog/
│   │   │   │   │   │   ├── dialog.component.html
│   │   │   │   │   │   ├── dialog.component.scss
│   │   │   │   │   │   └── dialog.component.ts
│   │   │   │   │   ├── new-session/
│   │   │   │   │   │   ├── new-session.component.html
│   │   │   │   │   │   ├── new-session.component.scss
│   │   │   │   │   │   └── new-session.component.ts
│   │   │   │   │   ├── session-histroy/
│   │   │   │   │   │   ├── session-histroy.component.html
│   │   │   │   │   │   ├── session-histroy.component.scss
│   │   │   │   │   │   └── session-histroy.component.ts
│   │   │   │   │   ├── home.component.html
│   │   │   │   │   ├── home.component.scss
│   │   │   │   │   └── home.component.ts
│   │   │   │   ├── login/
│   │   │   │   │   ├── login.component.html
│   │   │   │   │   ├── login.component.scss
│   │   │   │   │   ├── login.component.spec.ts
│   │   │   │   │   └── login.component.ts
│   │   │   │   ├── sginup/
│   │   │   │   │   ├── sginup.component.html
│   │   │   │   │   ├── sginup.component.scss
│   │   │   │   │   └── sginup.component.ts
│   │   │   │   ├── app.component.html
│   │   │   │   ├── app.component.scss
│   │   │   │   ├── app.component.ts
│   │   │   │   ├── app.config.server.ts
│   │   │   │   ├── app.config.ts
│   │   │   │   ├── app.module.ts
│   │   │   │   └── app.routes.ts
│   │   │   ├── assets/
│   │   │   │   └── icons/
│   │   │   │       └── github.svg
│   │   │   ├── environments/
│   │   │   │   ├── environment.prod.ts
│   │   │   │   └── environment.ts
│   │   │   ├── favicon.ico
│   │   │   ├── index.html
│   │   │   ├── main.server.ts
│   │   │   ├── main.ts
│   │   │   └── styles.scss
│   │   ├── angular.json
│   │   ├── package.json
│   │   ├── server.ts
│   │   ├── tsconfig.app.json
│   │   ├── tsconfig.json
│   │   └── tsconfig.spec.json
│   └── Dockerfile                   - Docker configuration for frontend
│
├── nginx/
│   └── nginx.conf                   - Nginx configuration for frontend
│
├── local/
│   └── install_dependencies/
│       └── mlcb_backend_package.sh  - Script for backend dependencies installation
│
├── .dockerignore                    - Specifies files to ignore in Docker builds
├── .pylintrc                        - Pylint configuration file
├── docker-compose.yaml              - Docker Compose configuration for local development
├── LICENSE                          - The GNU General Public License
└── README.md                        - Project overview and documentation
```
