use strict;

my @list = (1, 2, 3);
my $last = $#list;        # the sigil above is array length, not comment syntax
my $text = "# not a comment";

=pod
A POD block, which is documentation rather than code.
=cut

print $text; # trailing comment after code
