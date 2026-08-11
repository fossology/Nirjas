#include <string>

const std::string raw = R"(// not a comment inside a raw string)";
const std::string plain = "/* not a comment */";
/* outer /* C has no nesting, so this closes here */
int main() { return 0; } // trailing comment after code
