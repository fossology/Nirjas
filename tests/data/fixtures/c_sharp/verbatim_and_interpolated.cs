class Demo {
    const string Verbatim = @"// not a comment";
    static string Interpolated(int n) => $"/* not a comment */ {n}";

    static void Main() { } // trailing comment after code
}
