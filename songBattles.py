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

def update_file():
    with open("songs.csv", "w") as file:
        file.write("Title;Album;Victories;Defeats;LosingSongs")
        for song in songs_data:
            title = song["Title"]
            album = song["Album"]
            victories = song["Victories"]
            defeats = song["Defeats"]
            losing_songs = ";".join(song["LosingSongs"])
            file.write(f"\n{title};{album};{victories};{defeats};{losing_songs}")

    with open("battles.csv", "w") as file:
        file.write("N;Song1;Song2;Album1;Album2;Votes1;Votes2;Date")
        for battle in battles_data:
            n = battle["N"]
            song1 = battle["Song1"]
            song2 = battle["Song2"]
            album1 = battle["Album1"]
            album2 = battle["Album2"]
            votes1 = battle["Votes1"]
            votes2 = battle["Votes2"]
            date = battle["Date"]
            file.write(f"\n{n};{song1};{song2};{album1};{album2};{votes1};{votes2};{date}")

def Headline(text, qty, underlined="="):
    print()
    print(f"{text.center(qty)}\n{(underlined*qty)}")


# Songs functions
def list_songs():
    qty = 85
    Headline("List of Songs", qty)
    if len(songs_data) == 0:
        print("No songs found!")
        return
    
    print(f"{'Nº':<3} | {'Song':<29} | {'Album':<20} | {'V':^3} | {'D':^3} | {'Losing Songs'}")
    print("="*qty)

    for i, song in enumerate(songs_data):
        title = song["Title"]
        album = song["Album"]
        victories = song["Victories"]
        defeats = song["Defeats"]
        if len(song["LosingSongs"]) > 0:
            losing_songs = ", ".join(song["LosingSongs"])

        print(f"{i+1:02d}. | {title:<29} | {album:<20} | {victories:^3} | {defeats:^3} | {losing_songs}")
    print("="*qty)

def add_song():
    qty = 76
    Headline("Add Song", qty)
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
def find_song(title, album):
    for song in songs_data:
        if song["Title"].lower() == title.lower() and song["Album"].lower() == album.lower():
            return song
    print(f"Song '{title}' from album '{album}' not found!")

def update_song(song, album, is_winner):
    for s in songs_data:
        if s["Title"].lower() == song.lower() and s["Album"].lower() == album.lower():
            if is_winner:
                s["Victories"] += 1
            else:
                s["Defeats"] += 1
            return s

def find_losing_songs(song_title, album_title):
    losing_songs_set = set()

    for battle in battles_data:
        if battle["Song1"].lower() == song_title.lower() and battle["Album1"].lower() == album_title.lower() and int(battle["Votes1"]) > int(battle["Votes2"]):
            loser = (battle["Song2"], battle["Album2"])
            if loser not in losing_songs_set:
                losing_songs_set.add(loser)
                losing_songs_set.update(find_losing_songs(loser[0], loser[1]))
        elif battle["Song2"].lower() == song_title.lower() and battle["Album2"].lower() == album_title.lower() and int(battle["Votes2"]) > int(battle["Votes1"]):
            loser = (battle["Song1"], battle["Album1"])
            if loser not in losing_songs_set:
                losing_songs_set.add(loser)
                losing_songs_set.update(find_losing_songs(loser[0], loser[1]))

    return losing_songs_set

def update_losing_songs(winner_title, winner_album):
    losing_songs_set = find_losing_songs(winner_title, winner_album)

    for song in songs_data:
        if song["Title"].lower() == winner_title.lower() and song["Album"].lower() == winner_album.lower():
            song["LosingSongs"] = [losing_song for losing_song, _ in losing_songs_set]
            break

def update_all_losing_songs():
    for song in songs_data:
        update_losing_songs(song["Title"], song["Album"])

def add_battle():
    qty = 40
    Headline("Add Battle", qty)

    song1 = input("First Song: ")
    album1 = input("Album: ")
    if not find_song(song1, album1):
        return
    print("🆚".center(qty))
    song2 = input("Second Song: ")
    album2 = input("Album: ")
    if not find_song(song2, album2):
        return

    print()
    votes1 = input("Votes for First song: ")
    print("🥊".center(qty))
    votes2 = input("Votes for Second song: ")
    date = datetime.now().strftime("%d/%m/%Y")

    song1 = find_song(song1, album1)["Title"]
    song2 = find_song(song2, album2)["Title"]
    album1 = find_song(song1, album1)["Album"]
    album2 = find_song(song2, album2)["Album"]

    battle_info = {
        "N": len(battles_data) + 1,
        "Song1": song1,
        "Song2": song2,
        "Album1": album1,
        "Album2": album2,
        "Votes1": int(votes1),
        "Votes2": int(votes2),
        "Date": date
    }
    battles_data.append(battle_info)

    with open("battles.csv", "a") as file:
        file.write(f"\n{battle_info['N']};{song1};{song2};{album1};{album2};{votes1};{votes2};{date}")

    update_song(song1, album1, int(votes1) > int(votes2))
    update_song(song2, album2, int(votes2) > int(votes1))

    update_all_losing_songs()

    print(f"\n🎉 Battle between '{song1}' and '{song2}' added successfully!")

def list_battles():
    qty = 137
    Headline("History of Battles", qty)
    if len(battles_data) == 0:
        print("No battles found!")
        return
    
    print(f"{'Nº':<3} | {'Winner Song'.center(51)} | {'X'.center(11)} | {'Loser Song'.center(50)} | {'Date'.center(10)}")
    print("="*qty)

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

        if votes1 > votes2:
            first_song = f"🏆 {first_song}"
            print(f"{n:02d}. | {first_song.center(50)} | {votes1:^4} X {votes2:^4} | {second_song.center(50)} | {date:<10}")
        elif votes2 > votes1:
            second_song = f"🏆 {second_song}"
            print(f"{n:02d}. | {second_song.center(50)} | {votes2:^4} X {votes1:^4} | {first_song.center(50)} | {date:<10}")

    print("="*qty)

# Main program
read_file()
while True:
    print()
    print(" | Song Battles | ")
    print("1. List songs")
    print("2. Add new song")
    print("3. Add battle")
    print("4. List battles")
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
        update_file()
        break
    else:
        print("Invalid option!")

print("Program finished!")

