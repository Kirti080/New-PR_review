# Daylist — a small PHP project

A complete, single-user task manager built with PHP and CSS. No JavaScript, framework, database, or Composer packages required.

## Features

- Add, edit, complete, reopen, and delete tasks.
- Filter all, active, or completed tasks and view task counts.
- Save tasks between visits in a local JSON file.
- Responsive layout, labeled controls, CSRF protection, escaped output, and locked storage updates.

## Run

Install PHP 8.0 or newer, then open a terminal in this project folder:

```sh
php -S localhost:8000 -t public
```

Visit http://localhost:8000. Stop the server with Ctrl+C.

On Windows with XAMPP, you can run:

```powershell
C:\xampp\php\php.exe -S localhost:8000 -t public
```

If using Apache instead, configure its document root to this project's `public` directory. Keep `app.php` and `data` outside the web document root. PHP needs permission to create/write `data/tasks.json`, which is created on first visit.

## Files

```text
app.php            Session, validation, task actions, and file storage
public/index.php   Server-rendered interface
public/style.css   Responsive styling
data/tasks.json    Automatically created task data
```

## Quick manual check

1. Add a task and refresh: it should remain saved.
2. Edit its title, complete it, and check the Completed filter.
3. Reopen it and check the In progress filter.
4. Choose Delete, then Confirm delete: it should disappear.
5. Try a title containing `<b>hello</b>`: it should display as plain text.

This is a local learning project without user accounts: all visitors to the same running instance share the task list. The PHP development server is for local use. Back up `data/tasks.json` to retain your tasks.

## Python chaos test

Requires Python 3.8+. Stop the PHP server while injecting or restoring so the
script and PHP cannot overwrite each other's writes. From the project folder:

```sh
python tools/chaos.py inject
```

This backs up the original task file and adds 10 malformed entries (scalars,
missing fields, and incorrect field types). Restart PHP and view each filter:
valid tasks and their counts should remain unchanged, with no rendering errors.
The validation in `app.php` should reject the injected entries. Python runs only
when you invoke this tool; it is not required for normal app use.

Stop PHP again and restore the original data:

```sh
python tools/chaos.py restore
```

Restoring replaces the task list with the backup, discarding edits made during
the test. Repeated injection is blocked until you restore. If no task file
existed before the test, restoring produces an empty task list.
