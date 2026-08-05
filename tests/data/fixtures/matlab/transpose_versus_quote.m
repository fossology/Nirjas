A = [1 2 3];
B = A';                   % an apostrophe here is transpose, not a string
text = '% not a comment';

%{
A block comment delimited by %{ and %}
%}
disp(text); % trailing comment after code
