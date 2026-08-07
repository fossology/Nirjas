SELECT '-- not a comment' AS first_column;
SELECT 'text /* not a comment */' AS second_column;

-- a genuine line comment
SELECT 1; -- trailing comment after code
