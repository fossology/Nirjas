<?php
$plain = "// not a comment";
$nowdoc = <<<'TXT'
# not a comment inside a nowdoc
TXT;

# a hash-style comment
echo $plain; // trailing comment after code
