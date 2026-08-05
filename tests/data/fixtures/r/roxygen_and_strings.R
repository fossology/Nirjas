#' Roxygen documentation comment
#' @param x ignored
not_a_comment <- "# not a comment"

main <- function(x) {
  print(not_a_comment)  # trailing comment after code
}
