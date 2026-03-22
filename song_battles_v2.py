import csv
import random
from collections import defaultdict, deque

SONGS_FILE = "songs_new.csv"
BATTLES_FILE = "battles_new.csv"


# --------------------
# Loaders
# --------------------
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


# --------------------
# Graph / Ranking
# --------------------
def build_graph(songs, battles):
    graph = defaultdict(set)
    indegree = {s: 0 for s in songs}

    for w, l in battles:
        if l not in graph[w]:
            graph[w].add(l)
            indegree[l] += 1

    return graph, indegree


def ranking(songs, battles):
    graph, indegree = build_graph(songs, battles)
    queue = deque([s for s in indegree if indegree[s] == 0])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for nxt in graph[current]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order

def ranking_by_wins(songs, battles):
    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    scores = []
    for song_id in songs:
        wins = len(reachable[song_id])  # diretas + indiretas
        scores.append((song_id, wins))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def show_ranking_by_wins():
    songs = load_songs()
    battles = load_battles()

    ranking = ranking_by_wins(songs, battles)

    print("\n🏆 RANKING POR VITÓRIAS (DIRETAS + INDIRETAS)\n")
    for pos, (song_id, wins) in enumerate(ranking, start=1):
        s = songs[song_id]
        print(f"{pos:02d}. {s['title']} ({wins} vitórias)")

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


def suggest_next_battle(songs, battles):
    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    possible_pairs = []

    for a in songs:
        for b in songs:
            if a >= b:
                continue  # evita pares repetidos (A,B) e (B,A)
            if b not in reachable[a] and a not in reachable[b]:
                possible_pairs.append((a, b))

    if not possible_pairs:
        return None

    return random.choice(possible_pairs)


# --------------------
# Menu
# --------------------
def show_ranking():
    songs = load_songs()
    battles = load_battles()
    rank = ranking(songs, battles)

    print("\n🏆 RANKING ATUAL\n")
    for i, song_id in enumerate(rank, start=1):
        s = songs[song_id]
        print(f"{i:02d}. {s['title']} ({s['album']})")


def show_suggestion():
    songs = load_songs()
    battles = load_battles()

    suggestion = suggest_next_battle(songs, battles)

    if not suggestion:
        print("✅ Todas as músicas já possuem relação direta ou indireta.")
        return

    a, b = suggestion
    print("\n🔥 PRÓXIMA BATALHA SUGERIDA 🔥")
    print(f"{songs[a]['title']}  VS  {songs[b]['title']}")


def add_battle():
    songs = load_songs()

    print("\nMúsicas:")
    for i, s in songs.items():
        print(f"{i} - {s['title']}")

    winner_title = input("Título da música vencedora: ")
    loser_title = input("Título da música perdedora: ")

    w = next((id for id, s in songs.items() if s['title'].lower() == winner_title.lower()), None)
    l = next((id for id, s in songs.items() if s['title'].lower() == loser_title.lower()), None)

    if w is None or l is None:
        print("❌ Um ou ambos os títulos não foram encontrados.")
        return

    if w == l:
        print("❌ Músicas iguais.")
        return

    save_battle(w, l)
    print(f"✅ Batalha registrada: 🏆 {songs[w]['title']} venceu {songs[l]['title']}")


def show_battle_history():
    songs = load_songs()
    battles = load_battles()

    if not battles:
        print("\n📜 Nenhuma batalha registrada até agora.")
        return

    print("\n📜 HISTÓRICO DE BATALHAS\n")
    for i, (winner_id, loser_id) in enumerate(battles, start=1):
        winner = songs[winner_id]['title']
        loser = songs[loser_id]['title']
        print(f"{i:02d}. 🏆 {winner} venceu {loser}")


# --------------------
# Song Analysis
# --------------------

def show_song_analysis():
    songs = load_songs()
    battles = load_battles()

    query = input("Digite o nome da música: ").strip().lower()

    target_id = next((id for id, s in songs.items() if s['title'].lower() == query), None)

    if target_id is None:
        print("❌ Música não encontrada.")
        return

    graph, _ = build_graph(songs, battles)
    reachable = build_reachability(graph, songs)

    # músicas ainda sem relação (direta ou indireta)
    missing = []
    for other_id in songs:
        if other_id == target_id:
            continue
        if other_id not in reachable[target_id] and target_id not in reachable[other_id]:
            missing.append(other_id)

    # ranking topológico
    topo_rank = ranking(songs, battles)
    topo_pos = topo_rank.index(target_id) + 1 if target_id in topo_rank else None

    # ranking por vitórias
    wins_rank = ranking_by_wins(songs, battles)
    wins_pos = next((i+1 for i, (sid, _) in enumerate(wins_rank) if sid == target_id), None)

    # histórico da música
    history = []
    for w, l in battles:
        if w == target_id:
            history.append(("WIN", songs[l]['title']))
        elif l == target_id:
            history.append(("LOSS", songs[w]['title']))

    print("\n📊 ANÁLISE DA MÚSICA\n")
    print(f"🎵 {songs[target_id]['title']} ({songs[target_id]['album']})\n")

    print(f"📍 Posição (ranking lógico): {topo_pos}")
    print(f"🏆 Posição (por vitórias): {wins_pos}\n")

    print(f"⚔️ Batalhas faltando: {len(missing)}")
    if missing:
        print("Ainda precisa enfrentar:")
        for m in missing[:20]:  # limite para não poluir
            print(f"- {songs[m]['title']}")
        if len(missing) > 20:
            print(f"... e mais {len(missing) - 20}")

    print("\n📜 Histórico de batalhas:\n")
    if not history:
        print("Nenhuma batalha ainda.")
    else:
        for i, (result, opponent) in enumerate(history, start=1):
            emoji = "🏆" if result == "WIN" else "❌"
            print(f"{i:02d}. {emoji} {result} contra {opponent}")




def main():
    while True:
        print("\n1 - Ranking")
        print("2 - Nova batalha")
        print("3 - Sugerir próxima batalha")
        print("4 - Ranking por vitórias")
        print("5 - Histórico de batalhas")
        print("6 - Análise de música")
        print("0 - Sair")

        op = input("> ")

        if op == "1":
            show_ranking()
        elif op == "2":
            add_battle()
        elif op == "3":
            show_suggestion()
        elif op == "4":
            show_ranking_by_wins()
        elif op == "5":
            show_battle_history()
        elif op == "6":
            show_song_analysis()
        elif op == "0":
            break


if __name__ == "__main__":
    main()