#!/bin/sh
path="a/b/c"
base="${path##*/}"        # strips a prefix; that hash is expansion syntax
printf '%s\n' "# not a comment"

cat <<'EOF'
# not a comment inside a quoted heredoc
EOF

echo "$base" # trailing comment after code
