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

For example, if you were requested to do japanese, you might output something like
```
word | definition | synonym | translation | explanation | alt1 | alt2 | alt3
私 | 自分自身を指す言葉 | =僕 | I / me | A general, polite word for "I" or "me" used by anyone. It is the most common first-person pronoun taught to beginners. | わたし | watashi | 
が |  |  | subject marker | A grammatical particle used to mark the grammatical subject of a sentence. It highlights new information or the noun immediately preceding it. | ga |  | 
水 | 冷たい飲み物、無色透明の液体 | =お冷 | water | Refers specifically to cold or room-temperature drinking water. Note that hot water has a completely different word in Japanese ("oyu"). | みず | mizu | 
食べる | 食物を口に入れて飲み込むこと | =食う | to eat | A basic verb meaning to consume food. This is a standard "ru-verb" (Ichidan verb) used in everyday polite and casual conversation. | たべる | taberu | 
美味しい | 味がいいこと | =うまい | delicious / tasty | An i-adjective used to describe food or drinks that taste very good. | おいしい | oishii |
...
```
Though obviously, your requested language might not be japanese.