Here is a word bank:
{{word_bank}}

You are in charge of creating a dataset for someone learning the language {{target_language}}, noting that their native language is {{native_language}}. This dataset will be passed into an educational app that teaches them the language (think Duolingo). The above word bank contains all the words you should use to create the dataset, however it is not in the correct format.

Your output format is a csv file (where the order of the rows is the order the words should be learned in, and make sure you have the csv header row), with the following columns:
word in most commonly seen form in {{target_language}} | short definition in {{target_language}} | close synonym in {{target_language}} (prefixed with =) | direct translation to {{native_language}} | basic 1-2 sentence explanatory definition of the word and how to use it in {{native_language}} | Alternate form 1 | Alternate form 2 | Alternate form 3 

The alternate forms are optional; they represent different spellings of the same word, for example, a romanization or a different script. For languages where this is not appropriate, you may exclude it. Additionally, if no reasonable synonym exists (or if no reasonable definition in the same language exists, ie: for basic grammatical particles), you may leave the column with a blank string.

You do not need to call any tools or run any code.

Write your response in markdown, outputting a single code block for the csv, ie:
```csv
word | definition | synonym | translation | explanation | alt1 | alt2 | alt3
... row 1 ...
... row 2 ...
... row N ...
```