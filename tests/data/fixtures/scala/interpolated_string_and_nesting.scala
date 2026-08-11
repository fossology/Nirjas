object Demo {
  val count = 1
  val interpolated = s"// not a comment $count"

  /* outer /* nested block */ still outer */
  def main(args: Array[String]): Unit = println(interpolated) // trailing comment after code
}
