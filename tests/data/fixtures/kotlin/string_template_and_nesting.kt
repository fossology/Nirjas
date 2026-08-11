val count = 1
val templated = "// not a comment $count"
val raw = """/* not a comment */"""

/* outer /* nested block */ still outer */
fun main() { println(templated) } // trailing comment after code
