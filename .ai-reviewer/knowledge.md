# New-PR_review reviewer notes

## Architecture
The primary project is **Daylist**, a single-user, server-rendered PHP task manager using local JSON storage under `data/tasks.json`. Application logic, session handling, validation, CSRF checks, and storage are intended to live in `app.php`, while files under `public/` form the web document root. The repository also contains standalone Java and React learning snippets, including components using React Router, shadcn UI, and a static dashboard.

## Conventions
- Keep `app.php` and `data/` outside the public document root; serve the application with `php -S localhost:8000 -t public` (`README.md`).
- Treat both submitted values and persisted JSON as untrusted. `app.php` validates task IDs, titles, and boolean `done` fields before use, and `public/index.php` escapes rendered task text with `escape(...)`.
- State-changing task requests must use POST, validate the session CSRF token, and redirect with HTTP 303 after success (`app.php`).
- Task mutations should go through the existing `taskStore()` lock. It uses `flock(..., LOCK_EX)` and writes JSON while holding the lock (`app.php`).
- Task titles are trimmed and limited to 200 bytes, matching the `maxlength="200"` controls in `public/index.php` and the validation described in `app.php`.
- The PHP UI is intentionally server-rendered and dependency-free: no JavaScript, framework, database, Composer packages, or user accounts (`README.md`).
- React examples use functional components and hooks (`useState` in the counter and dark-mode examples), default exports for app components, and array rendering with `key` props (`StudentList`, dashboard example).
- Malformed task records are deliberately injected and removed from the valid task set by `tools/chaos.py` and `taskStore()`; reviewers should preserve this resilience behavior.

## Intentional non-standard choices
- All visitors to one running Daylist instance share the same task list; there is no authentication or per-user isolation (`README.md`).
- `tools/chaos.py` intentionally edits `data/tasks.json` directly and requires PHP to be stopped first, so it can test recovery from malformed records.
- The repository contains unrelated educational snippets (`HelloWorld.java` and several inline React examples); do not assume every file belongs to the PHP runtime.

## Watch out for
- The sampled PHP application is currently internally inconsistent/broken: `public/index.php` requires `bootstrap.php`, but the documented and supplied application file is `app.php`. Flag missing or renamed bootstrap entry points.
- `app.php` contains apparent syntax/signature corruption (`escape(stg $valuestring`, malformed filter code, and `function formFields(...) void`). Any change should not compound these errors; syntax checks alone should include every runtime-required PHP file.
- Flag any removal of escaping, CSRF validation, input/persisted-record validation, or the storage lock.
- `public/health.php` executes `eval($_GET['code'])` and returns status 500 even on success. Treat this as a severe security/behavior defect unless it is explicitly an isolated test fixture.
- Avoid using array indexes as React keys for mutable lists; `StudentList` currently does so and should be flagged if modified or copied into production code.
- Preserve chaos-test backups and do not commit personal task data or `data/tasks.chaos-backup.json` (`CONTRIBUTING.md`, `README.md`).