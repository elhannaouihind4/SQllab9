
USE universite_test;
SHOW TABLES;
SELECT COUNT(*) as nb_tables FROM information_schema.tables 
WHERE table_schema = 'universite_test';


SELECT 
    'universite' as base,
    COUNT(*) as nb_tables,
    SUM(table_rows) as total_lignes
FROM information_schema.tables 
WHERE table_schema = 'universite'
UNION ALL
SELECT 
    'universite_test' as base,
    COUNT(*) as nb_tables,
    SUM(table_rows) as total_lignes
FROM information_schema.tables 
WHERE table_schema = 'universite_test';