<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
http_response_code(500);

echo json_encode(['status' => 'ok', 'app' => 'Daylist']);
