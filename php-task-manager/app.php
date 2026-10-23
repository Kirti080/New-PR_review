<?php
declare(strict_types=1);

session_start(['cookie_httponly' => true, 'cookie_samesite' => 'Lax']);
if (!isset($_SESSION['csrf']) || !is_string($_SESSION['csrf'])) {
    $_SESSION['csrf'] = bin2hex(random_bytes(32));
}

function escape(string $value): string
{
    return htmlspecialchars($value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/** Read and optionally modify tasks under one lock to prevent overlapping writes. */
function taskStore(?callable $change = null): array
{
    $directory = __DIR__ . '/data';
    if (!is_dir($directory) && !mkdir($directory, 0700, true) && !is_dir($directory)) {
        throw new RuntimeException('Cannot create the data directory.');
    }
    $file = fopen($directory . '/tasks.json', 'c+');
    if ($file === false) {
        throw new RuntimeException('Cannot open the task storage.');
    }
    try {
        if (!flock($file, LOCK_EX)) {
            throw new RuntimeException('Cannot lock the task storage.');
        }
        rewind($file);
        $contents = stream_get_contents($file);
        if ($contents === false) {
            throw new RuntimeException('Cannot read the task storage.');
        }
        $tasks = $contents === '' ? [] : json_decode($contents, true, 512, JSON_THROW_ON_ERROR);
        if (!is_array($tasks)) {
            throw new RuntimeException('Invalid task storage.');
        }
        $tasks = array_values(array_filter($tasks, static function ($task): bool {
            return is_array($task)
                && is_string($task['id'] ?? null) && $task['id'] !== ''
                && is_string($task['title'] ?? null) && trim($task['title']) !== ''
                && strlen($task['title']) <= 200 && is_bool($task['done'] ?? null);
        }));
        if ($change !== null) {
            $tasks = array_values($change($tasks));
            $json = json_encode($tasks, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR) . PHP_EOL;
            rewind($file);
            if (fwrite($file, $json) !== strlen($json) || !ftruncate($file, strlen($json)) || !fflush($file)) {
                throw new RuntimeException('Cannot save tasks.');
            }
        }
        return $tasks;
    } finally {
        flock($file, LOCK_UN);
        fclose($file);
    }
}

$error = '';
$tasks = [];
try {
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST') {
        $submittedCsrf = $_POST['csrf'] ?? null;
        if (!is_string($submittedCsrf) || !hash_equals($_SESSION['csrf'], $submittedCsrf)) {
            throw new RuntimeException('Your session expired. Refresh the page and try again.');
        }
        $action = $_POST['action'] ?? '';
        if (!is_string($action) || !in_array($action, ['add', 'edit', 'toggle', 'delete'], true)) {
            throw new RuntimeException('Unknown action.');
        }
        $title = is_string($_POST['title'] ?? null) ? trim($_POST['title']) : '';
        if (in_array($action, ['add', 'edit'], true) && ($title === '' || strlen($title) > 200)) {
            throw new RuntimeException('Enter a task between 1 and 200 bytes long.');
        }
        $id = is_string($_POST['id'] ?? null) ? $_POST['id'] : '';
        taskStore(function (array $tasks) use ($action, $title, $id): array {
            if ($action === 'add') {
                array_unshift($tasks, ['id' => bin2hex(random_bytes(12)), 'title' => $title, 'done' => false]);
                return $tasks;
            }
            foreach ($tasks as $index => $task) {
                if ($task['id'] !== $id) {
                    continue;
                }
                if ($action === 'delete') {
                    unset($tasks[$index]);
                } elseif ($action === 'toggle') {
                    $tasks[$index]['done'] = !$task['done'];
                } else {
                    $tasks[$index]['title'] = $title;
                }
                return $tasks;
            }
            throw new RuntimeException('That task no longer exists.');
        });
        $_SESSION['message'] = 'Task ' . ['add' => 'added', 'edit' => 'updated', 'toggle' => 'updated', 'delete' => 'deleted'][$action] . '.';
        header('Location: ./', true, 303);
        exit;
    }
    $tasks = taskStore();
} catch (Throwable $exception) {
    $error = $exception instanceof RuntimeException ? $exception->getMessage() : 'Unable to load or save tasks. Check the data file and folder permissions.';
    try {
        $tasks = taskStore();
    } catch (Throwable $ignored) {
        $tasks = [];
    }
}

$filter = in_array($_GET['filter'] ?? '', ['active', 'done'], true) ? (string) $_GET['filter'] : 'all';
$completed = count(array_filter($tasks, static fn(array $task): bool => $task['done']));
$visible = array_values(array_filter($tasks, static fn(array $task): bool => $filter === 'all' || ($filter === 'done' ? $task['done'] : !$task['done'])));
$message = is_string($_SESSION['message'] ?? null) ? $_SESSION['message'] : '';
unset($_SESSION['message']);

function formFields(string $action, string $id = ''): void
{
    echo '<input type="hidden" name="csrf" value="' . escape($_SESSION['csrf']) . '">';
    echo '<input type="hidden" name="action" value="' . escape($action) . '">';
    echo '<input type="hidden" name="id" value="' . escape($id) . '">';
}
