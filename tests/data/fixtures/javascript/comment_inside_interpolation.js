const value = `a ${/* a real comment inside an interpolation */ 1} b`;
const plain = "// not a comment";

function main() { return value; } // trailing comment after code
