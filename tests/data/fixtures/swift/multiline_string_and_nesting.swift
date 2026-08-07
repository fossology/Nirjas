let multiline = """
// not a comment inside a multiline string
"""

/* outer /* nested block */ still outer */
func main() { _ = multiline } // trailing comment after code
