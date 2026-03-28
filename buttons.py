import random

import discord

class ReadButton(discord.ui.View):
    def __init__(self, timeout=120):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Read", style=discord.ButtonStyle.secondary)
    async def read(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.message.delete()
        except discord.HTTPException:
            await interaction.response.send_message("Could not delete the message.", ephemeral=True)



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
    {"word": "Strauch", "hint": "Dicht"},
]

CUSTOM_WORD_LIST = [
    {"word": "Abi darf ich mitkommen", "hint": "EmirMono"},
    {"word": "Dildo", "hint": "stecken"},
    {"word": "Smart", "hint": "Kompakt"},
    {"word": "Zev", "hint": "Campus"},
    {"word": "StreichBruder", "hint": "Japan"},
    {"word": "", "hint": ""},
    {"word": "", "hint": ""},
]


