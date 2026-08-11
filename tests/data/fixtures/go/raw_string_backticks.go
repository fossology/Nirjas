package main

const raw = `// not a comment inside a raw string`
const plain = "/* not a comment */"

func main() { _ = raw } // trailing comment after code
