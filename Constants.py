import random

import requests

WORD_LIST = [
    {"word": "Apfel", "hint": "Süß"},
    {"word": "Banane", "hint": "Form"},
    {"word": "Kirsche", "hint": "Doppelt"},
    {"word": "Delfin", "hint": "Freundlich"},
    {"word": "Känguru", "hint": "Sprung"},
    {"word": "Schmetterling", "hint": "Leicht"},
    {"word": "Regenschirm", "hint": "Schutz"},
    {"word": "Taschenlampe", "hint": "Kreis"},
    {"word": "Kühlschrank", "hint": "Weiß"},
    {"word": "Fernseher", "hint": "Flach"},
    {"word": "Kopfhörer", "hint": "Laut"},
    {"word": "Schlüssel", "hint": "Drehung"},
    {"word": "Brille", "hint": "Rahmen"},
    {"word": "Uhr", "hint": "Kreis"},
    {"word": "Gitarre", "hint": "Holz"},
    {"word": "Flasche", "hint": "Hals"},
    {"word": "Buch", "hint": "Schwer"},
    {"word": "Stift", "hint": "Spitze"},
    {"word": "Ball", "hint": "Luft"},
    {"word": "Schuh", "hint": "Paar"},
    {"word": "Hut", "hint": "Rand"},
    {"word": "Schal", "hint": "Länge"},
    {"word": "Tasse", "hint": "Henkel"},
    {"word": "Löffel", "hint": "Hohl"},
    {"word": "Gabel", "hint": "Spitzen"},
    {"word": "Messer", "hint": "Scharf"},
    {"word": "Teller", "hint": "Rund"},
    {"word": "Lampe", "hint": "Strahlt"},
    {"word": "Bett", "hint": "Weich"},
    {"word": "Stuhl", "hint": "Beine"},
    {"word": "Tisch", "hint": "Platte"},
    {"word": "Tür", "hint": "Klinke"},
    {"word": "Fenster", "hint": "Quadrat"},
    {"word": "Teppich", "hint": "Flauschig"},
    {"word": "Kissen", "hint": "Ecke"},
    {"word": "Decke", "hint": "Schwer"},
    {"word": "Spiegel", "hint": "Glatt"},
    {"word": "Bürste", "hint": "Borsten"},
    {"word": "Seife", "hint": "Rutschig"},
    {"word": "Handy", "hint": "Flach"},
    {"word": "Computer", "hint": "Laut"},
    {"word": "Tastatur", "hint": "Klick"},
    {"word": "Maus", "hint": "Schnur"},
    {"word": "Drucker", "hint": "Geräusch"},
    {"word": "Kamera", "hint": "Auge"},
    {"word": "Geld", "hint": "Papier"},
    {"word": "Regen", "hint": "Linien"},
    {"word": "Schnee", "hint": "Weich"},
    {"word": "Sonne", "hint": "Gelb"},
    {"word": "Wolke", "hint": "Formlos"},
    {"word": "Stern", "hint": "Punkte"},
    {"word": "Mond", "hint": "Phase"},
    {"word": "Blitz", "hint": "Zackig"},
    {"word": "Donner", "hint": "Bass"},
    {"word": "Wind", "hint": "Unsichtbar"},
    {"word": "Feuer", "hint": "Orange"},
    {"word": "Wasser", "hint": "Blau"},
    {"word": "Erde", "hint": "Braun"},
    {"word": "Berg", "hint": "Spitze"},
    {"word": "Tal", "hint": "Senke"},
    {"word": "Fluss", "hint": "Schlängelnd"},
    {"word": "See", "hint": "Spiegelnd"},
    {"word": "Meer", "hint": "Weit"},
    {"word": "Strand", "hint": "Körnig"},
    {"word": "Wald", "hint": "Dunkel"},
    {"word": "Wiese", "hint": "Grün"},
    {"word": "Blume", "hint": "Duft"},
    {"word": "Baum", "hint": "Schatten"},
    {"word": "Strauch", "hint": "Dicht"}, #Extendable
]

CUSTOM_WORD_LIST = [

]

class Constants:

    def __init__(self):
        self.word_list = WORD_LIST
        self.realWord = None
        self.hintWord = None
        self.previous_words = []

    def get_random_word(self):
        """Select a random word that hasn't been used recently"""
        available_words = [w for w in self.word_list if w["word"] not in self.previous_words]

        if not available_words:
            self.previous_words = []
            available_words = self.word_list

        selected = random.choice(available_words)
        self.real_word = selected["word"]
        self.hint_word = selected["hint"]

        self.previous_words.append(self.real_word)
        if len(self.previous_words) > 10:
            self.previous_words.pop(0)

        return selected

    def chance_word(self, chance):
        chance = max(1, min(10, chance))
        custom_probability = chance / 10



        valid_custom_words = [word for word in CUSTOM_WORD_LIST if word["word"]]




        if random.random() < custom_probability and valid_custom_words:
            return random.choice(valid_custom_words)
        else:
            return random.choice(WORD_LIST)

    def get_word_by_difficulty(self, difficulty):
        difficulty_map = {
            'easy': [w for w in self.word_list if len(w["word"]) <= 5],
            'medium': [w for w in self.word_list if 5 < len(w["word"]) <= 8],
            'hard': [w for w in self.word_list if len(w["word"]) > 8]
        }
        return random.choice(difficulty_map.get(difficulty, self.word_list))

    def add_custom_word(self, word, hint):
        """Add new word to the list"""
        new_entry = {"word": word, "hint": hint}
        self.word_list.append(new_entry)
        return new_entry
