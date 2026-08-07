#include <stdio.h>

const char *plain = "// not a comment";
// this comment continues onto the next line with a backslash \
   and this line is still inside that comment
int main(void) { return 0; } // trailing comment after code
