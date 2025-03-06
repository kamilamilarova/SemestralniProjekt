# Pygame Platformová Hra

Tento projekt je platformová hra vytvořená pomocí Pygame, ve které hráč sbírá mince, překonává překážky a vyhýbá se nepřátelům.

## Klíčové funkce
- Hráč se může pohybovat, skákat a interagovat s herním prostředím.
- Různé typy bloků včetně pevných a vodních.
- Systém sbírání mincí s animovaným efektem vznášení.
- Náhodné rozmístění mincí a generování platforem.
- Implementace nepřátel s pohybem a detekcí kolizí.
- Hladká kamera s posunem při pohybu hráče.

## Závislosti
Kod je psán v:
- Python 3.x
- Pygame

Instalace závislostí:
```
pip install pygame
```

## Struktura souborů
```
/your_project_directory
│── main.py          # Hlavní soubor hry
│── player.py        # Obsahuje třídu hráče
│── objects.py       # Obsahuje různé objekty včetně bloků a dveří
│── coins.py         # Obsahuje systém mincí
│── enemy.py         # Nepřátelé a jejich pohyb
│── settings.py      # Nastavení hry
│── windows.py       # Správa herního okna
│── assets/          # Obrázky a sprity
│── README.md
```


## Důležité poznámky
- Mince se vznášejí pomocí sinusové animace.
- Nepřátelé se pohybují mezi určenými hranicemi.
- Kamera sleduje hráče a posouvá herní svět.

## Možná vylepšení
- Přidání nových typů nepřátel.
- Implementace více úrovní s různými obtížnostmi.
- Vylepšení vizuálních efektů a zvukových efektů.

## Zdroje assetů a hudby
- 8 Bit Retro Game Music - Autor: Moodmode, Zdroj: https://pixabay.com
- Cartoon Buttons Pack - Autor: Prinbles, Zdroj: https://prinbles.itch.io/cartoon-buttons-pack-i
- Cat & Dog- free sprits, Zdroj: https://www.gameart2d.com/cat-and-dog-free-sprites.html
- Free platformer game tileset, Zdroj: https://www.gameart2d.com/free-platformer-game-tileset.html

Created By @Kamila Milarova
