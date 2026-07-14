You are to create a language learning program that uses takes as input a special format for a list of words to learn (in some language) and serves questions to the user, resembling Duolingo.
The input lesson format is a json list of dictionaries with the following structure:
```json
[
    {
        "word": "the word in the target language.",
        "definition": "the definition of the word in the target language.",
        "synonym": "the synonym of the word in the target language, prefixed with =.",
        "translation": "the translation of the word in the native language.",
        "explanation": "the explanation of the word in the target language.",
        "alt1": "an alternate spelling of the word in the target language, if applicable.",
        "alt2": "an alternate spelling of the word in the target language, if applicable.",
        "alt3": "an alternate spelling of the word in the target language, if applicable.",
        "sentences": [
            {
                "exert": "An exert in the target language, with brackets next to every word where within the brackets is a rough translation of the previous word, for example: El [the] gato [cat] duerme [sleeps].",
                "translation": "The translation, ie: The cat sleeps."
            },
            ...
        ]
    },
    ...
]
```
The elements in each dict, asides from the sentence (which will be seperately handled) will be referred to as aspects of the word. The word is an aspect of itself. Any of the elements in the dict (the aspects) may be empty, asides from the word itself. In the extreme case, it is possible every single word in the list is missing a specific aspect (or multiple specific aspects). Also note that the list is ordered in the order the words should be taught. 

The ultimate goal is to teach the user everything in the given lesson; your app should have an entrypoint where the user can create lessons by uploading or pasting json, export their entire user data as a json (for backup), and import previous user data. They should also see a card for each lesson they have created and generic tracking statistics. The user can also delete lessons or reset their progress.

Clicking the lesson card takes the user to the lesson view, which shows detailed progress and history stats on that specific lesson, alongside a list of the words in the lesson. There are also three modes the user can choose to study under: daily review which yields 30 questions, lesson which yields 100 questions, and rush which is timed for 5 minutes with 3 lives. The user can also configure some basic properties for the lesson, such as whether to use SM2 or FSRS-5 for serving questions, and the max number of new words shown daily, and the required minimum mastery on existing words before new words are shown.

Now, when the user clicks a button to study, they are taken to the actual lesson view, where they are served questions. The algorithm does not serve questions, but instead formats, until 30 total questions are served. When a format is served, that format is used for multiple questions (the format manages its own questions); the session ends itself when the number of questions reaches the desired goal.

Each format predetermines what words it will pick for its questions, furthermore each format has different mastery prerequisties (each format has a set difficulty), it goes without saying that formats that do not have enough words with a given mastery cannot be served at all. Certain formats have further restrictions. Furthermore, formats scale their own difficulty based on mastery; the greater the mastery, the harder the format will try to be.

Here are all the formats:
Difficulty 0:
- Introduction: All never seen before words are placed into this format when seen for the first time, and never again. The word is shown with its translation and explanation if present, and the user should click "okay" and the question passes. For obvious reasons, this format only serves one card at a time.
Difficulty 1:
- Pick the Answer: Given the word or any of its alternate forms, the user is presented with N answer choices, where each answer choice is a random aspect of the word or another word, and they must pick the correct aspect that is correlated with the word. N increases with mastery, starting from 2.
- Spot the Lie: Given a set of N pairs, where one side of the pair is the word or one of its alternate forms, and the other side is a different aspect that is not the definition/explanation (since it wouldn't fit on screen), the user must pick the pair that is incorrect.
Difficulty 2:
- Match Pairs: Generic matching game: The word or any of its alts are chosen for the left column, and the other column is a single type of aspect, besides the definition/explanations. You must match each word with its aspect. Number of pairs to match increases with difficulty. This question is only served once, and affects mastery for all pairs.
- Word Scramble: A word or alt form is chosen, and any of its aspects including the explanation/definition are chosen. One is (either can work) presented, and the other one is to be filled. If the user must fill multiple words (seperated by spaces), then each word is an element, and remaining answer choices are randomly pulled. Otherwise, if the answer is a single word, the user must fill each character. The user is given the pieces to arrange into the correct answer, with some irrelevant pieces. Additionally, if the sentence/characters is too long, some will be prefilled as hints. As mastery increases, the number of irrelevant pieces does too, and the number of hints decreases. Note that there must be at least two characters for something to be fillable, make sure the answer isn't one character.
Difficulty 3:
- Fill the Gap: A word or alt form is chosen, and any of its aspects including the explanation/definition are chosen. One is (either can work) presented, and the other one is to be filled. Note that valid filling options must be typable on a standard qwerty keyboard, so no unicode. If the sequence is too long, most of it will be given as hints, the user should not be expected to type anything longer than maybe 1 word. The explanation/definition are not valid as possible answers, so the user should never have to type them. This mode does not adjust difficulty.
- Sentence Comprehension: A sentence is chosen and a set number of words are turned into underscores. Furthermore, all words with some mastery equal to the requirement to reach difficulty 3 have their bracket translations removed, while words with mastery below that have their bracket translations shown. The user must fill in all the blanks, with the number of blanks increasing (slightly) alongside the irrelevant answer choices with difficulty, similar to the word scramble problem.
- Sentence Translation: The translation of a sentence is shown, and a sentence is chosen, with all words with some mastery equal to the requirement to reach difficulty 3 have their bracket translations removed. Some words are randomly turned into blanks (more than in sentence comprehension), which must be filled by the user. Additional irrelevant words are also presented as answer choices for the blanks. As the difficulty increases, the number of blanks and irrelevant words increases.
Difficulty 4:
- Shell Game: This question is served multiple times, but the chosen shells are the same. That is, the game sets up once. N of the word, any of its alt forms, its synonym, or direct translation are chosen. They are shown briefly, placed into shells, and shuffled. The user is then randomly shown an aspect corresponding to a shell item, this can be any aspect including the same one in the shell, and the user must click the corresponding shell. The number of shells scales {4, 5, 6}.
- Card Game: As with the shell game, the question is served multiple times, but the chosen cards are the same. The user is given a set of N cards where each has a word, any of its alt forms, its synonym, or direct translation. The user can freely move them around. The cards are then hidden after some time. The user is then randomly shown an aspect corresponding to a card item, this can be any aspect including the same one in the card, and the user must click the corresponding card. The number of cards scales {4, 6, 9}.
- Marble Game: As with the card game, the question is served multiple times, but the chosen marbles are the same. The user is presented with N slots on the bottom in a row, each corresponding to a word, any of its alt forms, its synonym, or direct translation and a marble setup (which involves a bunch of pins which are circles). A cannon is on the top of the marble setup which has a fixed random angle, changed on each new question. Then, the words are hidden. A marble is shot from the cannon and falls into one of the slots. The user is given a list of options, they must pick the aspect corresponding to the slot. The slots are then shown briefly again (unlike the previous game formats) before another marble is shot. The number of slots scales {6, 9, 12}

The user can either pick SM-2 or FSRS-5 for the question yielding algorithm. N increases with mastery, starting from 2.

Of course, it goes without saying that in no format should the answer and question, or a pair of aspects be exactly the same, and there should not be multiple answer choices. This means you need to make sure not to accidentally resample aspects.

