Here is a list of words in {{target_language}}:
{{words}}

Here is a word bank:
{{word_bank}}

You are in charge of creating a dataset for someone learning the language {{target_language}}, noting that their native language is {{native_language}}. This dataset will be passed into an educational app that teaches them the language (think Duolingo). For each word in the word bank, create a natural sounding and interesting exert of up to 3 sentences that uses the word (and other words), with the remaining words in the exert from the word list if possible. This means that you will have the same number of exerts as words in the word bank.

Your output format is a csv file (where the order of the rows is the order the words should be learned in, and make sure you have the csv header row), with the following columns:
exert in {{target_language}} | {{native_language}} translation

The exert must follow a special format. After every word in {{target_language}}, wrap within square brackets a reasonably appropriate one word translation (for that specific sentence) to {{native_language}}. This way, even if the user does not understand the words in the sentence, they will be able to know the meaning of those words by reading the translations as a form of hint. Every single word should be followed by its translation in this manner. The translation of the exert should be written normally.

You do not need to call any tools or run any code.

Write your response in markdown, outputting a single code block for the csv, ie:
```csv
exert | translation
... row 1 ...
... row 2 ...
... row N ...
```

For example, if you were requested to do spanish, you might output something like
```
exert | translation
El[The] fantasma[ghost] viejo[old] lee[reads] un[a] libro[book]. | The old ghost reads a book.
La[The] biblioteca[library] está[is] oscura[dark]. Nosotros[We] leemos[read] en[in] silencio[silence]. | The library is dark. We read in silence.
Tú[You] no[not] debes[must] susurrar[whisper] aquí[here]. El[The] bibliotecario[librarian] está[is] enojado[angry]. Él[He] tiene[has] orejas[ears] grandes[big]. | You must not whisper here. The librarian is angry. He has big ears.
```
Though obviously, your requested language might not be spanish.