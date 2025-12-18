
SHOW GLOBAL STATUS;


SHOW GLOBAL STATUS LIKE 'Uptime';
SHOW GLOBAL STATUS LIKE 'Threads_%';
SHOW GLOBAL STATUS LIKE 'Questions';

-- Variables système importantes
SHOW VARIABLES LIKE 'max_connections';
SHOW VARIABLES LIKE 'innodb_buffer_pool_size';