Git
===
- do not files proper to your computer to Git; use .gitignore files
- please do not push code that is used for debugging (especially NOT on master)
- do not push dead code (i.e. unused code in comments)
- name your branches following this convention: `words-separated-by-a-dash`, NOT `words_separated_by_underscores`
- do not copy-paste code. If you need code of some other branch, either create some small piece of code that can fake the behaviour (and do NOT upload that code in the end) or create your branch based on the one that contains what you need
- do your own commits (and do not add your College ID in brackets)
- be careful with whitespace characters (especially tabs); I saw some weird `CRLF` problems
- commit on your branch frequently enough to mark progress

Any language
===
- be consistent in terms of style everywhere! We want a code that is pleasasnt to the eye
- organize your files immediately! The skeleton of your work might be the first thing you want to do!
- **avoid writing everything manually, inventing weird ways, and coming up with black magic**: **see if a proper solution exists already, such as a library or a method in an already imported library** (especially in JS where there is a library even for checking if numbers are odd...). The most recent example is all the migration that had to be done from the original Vuex setup to the new one [that I did --- Oscar]
- document your code (this advice is less applicable to JS)
- comment your code

HTML/CSS
===
- do not use pixels (`px`) as a unit! It is not a good practice. Prefer: `em` or `rem` or even `vh`
- when using Vue Bootstrap, and using a component, do not add again the class of the element. For example, there is no need to add the class `form-group` to a `<b-form-group>` tag
- for colour variants in Vue Bootstrap, use `variant="dark"` instead of adding the classes manually

For JS
===
Style
---
- **stick to the conventions**! In JS, camelCase is predominant. Example: thisIsCamelCase
- remove colons (`;`): they are useless
- when writing anonymous functions (also called "arrow functions"), remove the curly braces (`{}`) if it only holds one line of code. For example, write: `.then(res => singleLine)` (and NOT `.then(res => { singleLine }`)
- when writing anonymous functions that have a single parameter, remove the parentheses (`()`) around the argument. For example, write: `argument => ...` (and NOT `(argument) => ...`)
- try to indent code properly (no proper definition of this, but just a bit of common sense - it should be fine, don't worry)
- use simple quotes (`' '`) instead of double quotes (`" "`)

Other
---
- for equality to special values, prefer `===` instead of `==`

For Python
===
Style
---
- stick to the Python naming convention of snake_case
- use simple quotes (`' '`) instead of double quotes (`" "`)

General
---
- again, use the **existing** methods! For example, do not write the status of the request manually, but rather use what Flask enables you to do; you could, for instance, return a tuple of 1. the response, 2. the code, in your route (*i.e.*, `return response, 200`) ONLY IF YOU NEED A PARTICULAR HTTP RESPONSE CODE
