import csv
import random
from collections import defaultdict

SONGS_FILE = "songs_new.csv"
BATTLES_FILE = "battles_new.csv"


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃          LOADERS         ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def load_songs():
    songs = {}
    with open(SONGS_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs[int(row["id"])] = {
                "title": row["title"],
                "album": row["album"]
            }
    return songs

def load_battles():
    battles = []
    with open(BATTLES_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            battles.append((int(row["winner_id"]), int(row["loser_id"])))
    return battles

def save_battle(winner, loser):
    with open(BATTLES_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([winner, loser])

def Headline(text, qty, underlined="-"):
    print()
    print(f"{text.center(qty)}\n{f'+{(underlined*qty)}+'}")

def return_to_menu(zero):
    if zero == "0":
        print("\n↩️  Retorned to main menu.")
        return True
    return False

# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃        Management        ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def add_song():
    qty = 50
    Headline("Add New Song", qty)
    
    reader = []
    file_exists = False

    try:
        with open(SONGS_FILE, newline="", encoding="utf-8") as f:
            file_exists = True
            reader = list(csv.DictReader(f))
            if reader:
                last_id = max(int(row["id"]) for row in reader)
            else:
                last_id = 0
    except FileNotFoundError:
        file_exists = False
        last_id = 0

    title = input("| Song Title: ").strip()
    if return_to_menu(title):
        return
    
    album = input("| Album Name: ").strip()
    if return_to_menu(album):
        return

    if not title or not album:
        print("|\n| ❌ Error: Song Title and Album name are required.")
        return

    normalized_title = title.lower()
    if any(row["title"].strip().lower() == normalized_title for row in reader):
        print(f"|\n| ❌ Error: The song '{title}' already exists. (Try using a different Title.)")
        return

    new_id = last_id + 1

    with open(SONGS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["id", "title", "album"])
        writer.writerow([new_id, title, album])

    print(f"|\n| ✅ {new_id:02d}º Song added: {title} - {album}")

def add_battle():
    qty = 50
    Headline("Add New Battle", qty)

    songs = load_songs()
    battles = load_battles()
    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    print(f"| 🥊 {len(load_battles())}º '{songs[battles[-1][0]]['title']}'  WON  '{songs[battles[-1][1]]['title']}'" if battles else "| No battles added yet.")
    print("|")

    winner = input("| 🏆 Winner Song Title: ").strip()
    if return_to_menu(winner):
        return
    
    loser = input("| 🥊 Loser Song Title: ").strip()
    if return_to_menu(loser):
        return

    if not winner or not loser:
        print("|\n| ❌ Error: Winner and loser song titles are required.")
        return

    w = next((id for id, s in songs.items() if s['title'].lower() == winner.lower()), None)
    l = next((id for id, s in songs.items() if s['title'].lower() == loser.lower()), None)

    if w is None or l is None:
        print("|\n| ❌ Error: One or both song titles not found. Please check the spelling and try again.")
        return
    
    if w == l:
        print("|\n| ❌ Error: The winner and loser songs cannot be the same.")
        return

    # Check if a direct or indirect relationship already exists.
    if l in reachable[w] or w in reachable[l]:
        print("|\n| ❌ Error: A direct or indirect relationship already exists between these songs. Please check the battle history and try again.")

        # Looking for a way to show historical evidence.
        def find_path(start, end, graph):
            stack = [(start, [start])]
            visited = set()

            while stack:
                current, path = stack.pop()
                if current == end:
                    return path
                for nxt in graph[current]:
                    if nxt not in visited:
                        visited.add(nxt)
                        stack.append((nxt, path + [nxt]))
            return None

        path = find_path(w, l, graph)
        if not path:
            path = find_path(l, w, graph)

        if path:
            print("|\n| 📜 Relationship found:")
            for i in range(len(path) - 1):
                a = songs[path[i]]['title']
                b = songs[path[i+1]]['title']
                print(f"| {i+1}. 🏆 {a}  WON  {b}")

            return
        
        else:
            print("|\n| ⚠️ Indirect relationship detected, but it was not possible to reconstruct the path.")
        return
    
    save_battle(w, l)
    battle_number = len(battles) + 1

    print(f"|\n| ✅ {battle_number:02d}º Battle added: 🏆 '{songs[w]['title']}' WON '{songs[l]['title']}'.")

def build_reachability(graph, songs):
    reachable = {s: set() for s in songs}

    for start in songs:
        stack = [start]
        visited = set()

        while stack:
            current = stack.pop()
            for nxt in graph[current]:
                if nxt not in visited:
                    visited.add(nxt)
                    reachable[start].add(nxt)
                    stack.append(nxt)

    return reachable

def suggest_next_battles(songs, battles, limit=5):
    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    possible_pairs = []

    for a in songs:
        for b in songs:
            if a >= b:
                continue
            if b not in reachable[a] and a not in reachable[b]:
                possible_pairs.append((a, b))

    if not possible_pairs:
        return []

    return random.sample(possible_pairs, k=min(limit, len(possible_pairs)))

def show_suggestion():
    qty = 50
    songs = load_songs()
    battles = load_battles()

    suggestions = suggest_next_battles(songs, battles)

    if not suggestions:
        Headline("🎉 THE BATTLE IS OVER! 🎉", qty)
        print("All possible battles have been completed. Check the Ranking to see the final results!")
        return

    Headline("Suggest Battles", qty)
    for i, (a, b) in enumerate(suggestions, start=1):
        print(f"{i:02d}. {songs[a]['title']}  VS  {songs[b]['title']}")


# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃   Ranking and Analysis   ┃
# ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
def build_graph(songs, battles):
    graph = defaultdict(set)
    indegree = {s: 0 for s in songs}

    for w, l in battles:
        if l not in graph[w]:
            graph[w].add(l)
            indegree[l] += 1

    return graph, indegree

def show_song_analysis():
    qty = 50
    Headline("Info Song", qty)

    songs = load_songs()
    battles = load_battles()

    query = input("| Type the name of the song: ").strip().lower()

    target_id = next((id for id, s in songs.items() if s['title'].lower() == query), None)

    if target_id is None:
        print("|\n| ❌ Song not found. Please check the spelling and try again.")
        return

    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    missing = []
    for other_id in songs:
        if other_id == target_id:
            continue
        if other_id not in reachable[target_id] and target_id not in reachable[other_id]:
            missing.append(other_id)

    wins_rank = ranking(songs, battles)
    wins_pos = next((i+1 for i, (sid, _) in enumerate(wins_rank) if sid == target_id), None)

    history = []
    for w, l in battles:
        if w == target_id:
            history.append(("WIN ", songs[l]['title']))
        elif l == target_id:
            history.append(("LOSS", songs[w]['title']))

    Headline(f"🎵 {songs[target_id]['title'].upper()} from {songs[target_id]['album'].upper()}", qty)

    print(f"| 🏆 Ranking: {wins_pos}º")
    print(f"|\n| ⚔️  Missing Battles: {len(missing)}")

    if missing:
        for i, m in enumerate(missing[:20]):  # Show only 20 to not pollute
            print(f"| {i+1:02d}. {songs[m]['title']}")
        if len(missing) > 20:
            print(f"| ... and {len(missing) - 20} more.")
    else:
        print("|\n| None, this song has battled against all others!")

    print("|\n| 📜 Battle History:")
    if not history:
        print("|\n| No battles recorded yet.")
    else:
        for i, (result, opponent) in enumerate(history, start=1):
            emoji = "🏆" if result == "WIN " else "❌"
            print(f"| {i:02d}. {emoji} {songs[target_id]['title']}  vs  {opponent}")

def ranking(songs, battles):
    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    scores = []
    for song_id in songs:
        wins = len(reachable[song_id])
        scores.append((song_id, wins))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def show_ranking():
    qty = 63
    Headline("🏆 RANKING 🏆", qty)
    songs = load_songs()
    battles = load_battles()

    if not songs:
        print("|\n| 📜 No songs registered yet.")
        return

    if not battles:
        print("|\n| 📜 No battles registered yet.")
        return

    rank = ranking(songs, battles)

    print(f"{'| Nº':<3} | {'Song':<29} | {'Album':<17} | {'Wins':^4} |")
    print(f'{f"+{("-"*4)}+{("-"*31)}+{("-"*19)}+{("-"*6)}+"}')

    for i, (song_id, wins) in enumerate(rank, start=1):
        s = songs[song_id]
        print(f"|{i:03d}.| {s['title']:<29} | {s['album']:<17} | {wins:^4} |")

    print(f'{f"+{("-"*4)}+{("-"*31)}+{("-"*19)}+{("-"*6)}+"}')

def show_battle_history():
    qty = 78
    Headline("Battle History", qty)

    songs = load_songs()
    battles = load_battles()

    if not battles:
        print("|\n| 📜 No battles registered yet.")
        return

    print(f"{'| Nº':<3} | {'Winner Song'.center(31)} | {'X'.center(3)} | {'Loser Song'.center(31)} |")
    print(f'{f"+{("-"*4)}+{("-"*33)}+{("-"*5)}+{("-"*33)}+"}')

    for i, (winner_id, loser_id) in enumerate(battles, start=1):
        winner = songs[winner_id]['title']
        loser = songs[loser_id]['title']
        print(f"|{i:03d}.|🏆 {winner:<29} | {'X':^3} | {loser:>29} 🥊|")

    print(f'{f"+{("-"*4)}+{("-"*33)}+{("-"*5)}+{("-"*33)}+"}')

def show_participating_songs():
    qty = 50
    Headline("Participating Songs", qty)
    songs = load_songs()
    battles = load_battles()

    participating_ids = set()
    for winner_id, loser_id in battles:
        participating_ids.add(winner_id)
        participating_ids.add(loser_id)

    if not participating_ids:
        print("| 📀 No music has participated in battles yet.")
        return

    songs_by_album = defaultdict(list)
    for song_id in sorted(participating_ids):
        song = songs.get(song_id)
        if song is None:
            continue
        songs_by_album[song["album"]].append(song["title"])

    print(f"| {("📀 Participating Songs by Album").center(qty-3)} |")
    print("+" + "-"*qty + "+")
    
    for album in sorted(songs_by_album):
        print(f"| {f'{album.upper()} ({len(songs_by_album[album])})'.center(qty-2)} |")
        print("+" + "-"*qty + "+")
        for i, title in enumerate(sorted(songs_by_album[album], key=str.lower), start=1):
            print(f"| {f'{i:02d}. {title}':<{qty-2}} |")
        print("+" + "-"*qty + "+")



def main():
    while True:
        print("\n+---------------------------+")
        print("|      Song Battles v2      |")
        print("+---------------------------+")
        print("| 1. Add New Song           |")
        print("| 2. Add New Battle         |")
        print("| 3. Info Song              |")
        print("| 4. Suggest Battles        |")
        print("| 5. Ranking                |")
        print("| 6. Battle History         |")
        print("| 7. Participating Songs    |")
        print("| 0. Leave                  |")
        print("+---------------------------+")
        print(f'type "0" to return to menu'.center(27))
        print(f"{f'+{("-"*27)}+'}")

        option = input("\nChoose an option: ").strip()

        if option == "1":
            add_song()
        elif option == "2":
            add_battle()
        elif option == "3":
            show_song_analysis()
        elif option == "4":
            show_suggestion()
        elif option == "5":
            show_ranking()
        elif option == "6":
            show_battle_history()
        elif option == "7":
            show_participating_songs()
        elif option == "0":
            break

main()
