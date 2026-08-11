const slashes: RegExp = /\/\/ not a comment/;
const template: string = `/* not a comment */`;

function identity<T>(value: T): T { return value; } // trailing comment after code
