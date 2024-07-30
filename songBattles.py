import os
from datetime import datetime

songs_data = []
battles_data = []

def read_file():
    if not os.path.isfile("songs.csv"):
        print('no file "songs.csv" found!')
        return
    
    if not os.path.isfile("battles.csv"):
        print('no file "battles.csv" found!')
        return
    
    with open("songs.csv", "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split(";")
            song_info = {
                "Title": parts[0],
                "Album": parts[1],
                "Victories": int(parts[2]),
                "Defeats": int(parts[3]),
                "LosingSongs": parts[4:]
            }
            songs_data.append(song_info)

    with open("battles.csv", "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            parts = line.strip().split(";")
            battle_info = {
                "N": parts[0],
                "Song1": parts[1],
                "Song2": parts[2],
                "Album1": parts[3],
                "Album2": parts[4],
                "Votes1": int(parts[5]),
                "Votes2": int(parts[6]),
                "Date": parts[7]
            }
            battles_data.append(battle_info)

def Headline(text, qty, underlined="="):
    print()
    print(f"{text.center(qty)}\n{(underlined*qty)}")


# Songs functions
def list_songs():
    Headline("List of Songs", qty=76)
    if len(songs_data) == 0:
        print("No songs found!")
        return
    
    print(f"{'Nº':<3} | {'Song':<20} | {'Album':<20} | {'V':^3} | {'D':^3} | {'Losing Songs'}")
    print("="*76)

    for i, song in enumerate(songs_data):
        title = song["Title"]
        album = song["Album"]
        victories = song["Victories"]
        defeats = song["Defeats"]
        if len(song["LosingSongs"]) > 0:
            losing_songs = ", ".join(song["LosingSongs"])

        print(f"{i+1:02d}. | {title:<20} | {album:<20} | {victories:^3} | {defeats:^3} | {losing_songs}")

def add_song():
    Headline("Add Song", qty=76)
    title = input("Title: ")
    album = input("Album: ")

    song_info = {
        "Title": title,
        "Album": album,
        "Victories": 0,
        "Defeats": 0,
        "LosingSongs": ""
    }
    songs_data.append(song_info)

    with open("songs.csv", "a") as file:
        file.write(f"\n{title};{album};{0};{0};")

    print(f"🎉 Song '{title}' from album '{album}' added successfully!")


# Battles functions
def add_battle():
    Headline("Add Battle", qty=136)
    song1 = input("First Song: ")
    album1 = input("Album: ")
    song2 = input("Second Song: ")
    album2 = input("Album: ")
    votes1 = input("Votes for First song: ")
    votes2 = input("Votes for Second song: ")
    date = datetime.now().strftime("%d/%m/%Y")

    battle_info = {
        "N": len(battles_data) + 1,
        "Song1": song1,
        "Song2": song2,
        "Album1": album1,
        "Album2": album2,
        "Votes1": votes1,
        "Votes2": votes2,
        "Date": date
    }
    battles_data.append(battle_info)

    with open("battles.csv", "a") as file:
        file.write(f"\n{battle_info['N']};{song1};{song2};{album1};{album2};{votes1};{votes2};{date}")

    print(f"\n🎉 Battle between '{song1}' and '{song2}' added successfully!")

def list_battles():
    Headline("List of Battles", qty=136)
    if len(battles_data) == 0:
        print("No battles found!")
        return
    
    print(f"{'Nº':<3} | {'First Song'.center(50)} | {'X'.center(11)} | {'Second Song'.center(50)} | {'Date':<10}")
    print("="*136)

    for battle in battles_data:
        n = int(battle["N"])
        song1 = battle["Song1"]
        album1 = battle["Album1"]
        votes1 = battle["Votes1"]
        song2 = battle["Song2"]
        album2 = battle["Album2"]
        votes2 = battle["Votes2"]
        date = battle["Date"]

        first_song = f"{song1} - {album1}"
        second_song = f"{song2} - {album2}"

        print(f"{n:02d}. | {first_song.center(50)} | {votes1:^4} X {votes2:^4} | {second_song.center(50)} | {date:<10}")


# Main program
read_file()
while True:
    print()
    print("1. Listar músicas")
    print("2. Incluir música")
    print("3. Adicionar Batalha")
    print("4. Listar batalhas")
    # print("3. Pesquisar música")
    # print("4. Listar músicas por álbum")
    print("8. Sair")
    option = input("Opção: ")
    
    if option == "1":
        list_songs()
    elif option == "2":
        add_song()
    elif option == "3":
        add_battle()
    elif option == "4":
        list_battles()
    elif option == "8":
        break
    else:
        print("Opção inválida")

print("Fim do programa")

