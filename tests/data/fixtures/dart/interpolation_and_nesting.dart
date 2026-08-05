const count = 1;
const plain = "// not a comment";

/* outer /* nested block */ still outer */
void main() { print(plain); } // trailing comment after code
