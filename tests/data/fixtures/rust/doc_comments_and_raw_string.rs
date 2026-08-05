//! Inner doc comment for the module.

/// Outer doc comment for the constant.
const RAW: &str = r#"// not a comment inside a raw string"#;

/* outer /* nested block */ still outer */
fn main() { let _ = RAW; } // trailing comment after code
