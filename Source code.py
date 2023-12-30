import requests
import json

def menu(exist):
    loop = True
    while loop:
        print("---------------------------------------")
        print("Excess10n's funny little playlist program")
        print("---------------------------------------")
        print("\t- 1: Get maps for snipes")
        print("\t- 2: Get top plays")
        print("\t- 3: Set user data")
        print("\t- 4: Snipe Bela")
        print("\t- 5: Quit")
        if (not exist):
            print("User data hasn't been set, please select 2")
        x = input("Select -> ")
        print()
        if x == "1":
            snipe()
        elif x == "2":
            top_ranked()
        elif x == "3":
            set_data()
        elif x == "4":
            bela()
        elif x == "5":
            loop = False

def set_data():
    global userData
    print("--- Set user data ---")
    print()
    if userData["userID"] == None:
        print("Your ScoreSaber ID: [NOT SET]")
    else:
        print("Your ScoreSaber ID: " + str(userData["userID"]))

    if userData["directory"] == None:
        print("Your Beat Saber directory: [NOT SET]")
    else:
        print("Your Beat Saber directory: " + str(userData["directory"]))
    print()
    loop = True
    while loop:
        x = input("Input ID or name (leave empty to not change) -> ")
        if x == "":
            loop = False
        else:
            try:
                x = int(x)
                userData["userID"] = x
                print("Set user id to: " + str(x))
                loop = False
            except:
                player = player_search(x)
                if player != None:
                    userData["userID"] = player["id"]
                    print("Set user id to: " + str(player["id"]))
                    loop = False
    x = input("Input Beat Saber directory (leave empty to not change) -> ")
    if x != "":
        userData["directory"] = x
        print("Set directory to: " + x)
    print()
        
def snipe():
    print("--- Get maps for snipes ---")
    print()
    exist = userData["userID"] != None
    loop = True
    id1 = 0
    while loop:
        if exist:
            x = input("Input ID or name of the sniper (leave empty to use your own ID) -> ")
        else:
            x = input("Input ID or name of the sniper -> ")
        if x == "":
            id1 = userData["userID"]
            loop = False
        else:
            try:
                x = int(x)
                id1 = x
                print("Set sniper id to: " + str(x))
                loop = False
            except:
                player = player_search(x)
                if player != None:
                    id1 = player["id"]
                    print("Set sniper id to: " + str(player["id"]))
                    loop = False
    print()
    loop = True
    id2 = 0
    while loop:
        x = input("Input ID or name of the target -> ")
        if x != "":
            try:
                x = int(x)
                id2 = x
                print("Set target id to: " + str(x))
                loop = False
            except:
                player = player_search(x)
                if player != None:
                    id2 = player["id"]
                    print("Set target id to: " + str(player["id"]))
                    loop = False
    print()
    x = input("Include maps that you don't have scores on? (y/n) -> ").lower()
    if x == "y":
        x = True
    else:
        x = False
    songs = get_maps(id1, id2, x)
    print()
    print("Found " + str(len(songs)) + " maps")
    x = input("Display maps? (y/n) -> ").lower()
    if x == "y":
        for song in songs:
            print()
            print("name: " + song["name"])
            print("diff: " + song["difficulties"][0]["name"])
    if userData["directory"] != None:
        print()
        x = input("Would you like to create a playlist in your beat saber directory (y/n) -> ").lower()
        if x == "y":
            name = input("Enter a name for the playlist (this will also be the file name) -> ")
            make_playlist(songs, name)
    print()
    print("Done!")
    print()

def bela():
    print("--- Bela snipe time ---")
    print()
    if userData["userID"] == None or userData["directory"] == None:
        print("Please set the user data from the menu first")
    elif userData["userID"] == belaID:
        for i in range(100):
            print("HI BELA :)")
    else:
        x = input("Include maps that you don't have scores on? (y/n) -> ").lower()
        if x == "y":
            x = True
        else:
            x = False
        songs = get_maps(userData["userID"], belaID, x)
        print()
        print("Found " + str(len(songs)) + " maps")
        x = input("Display maps? (y/n) -> ").lower()
        if x == "y":
            for song in songs:
                print()
                print("name: " + song["name"])
                print("diff: " + song["difficulties"][0]["name"])
        make_playlist(songs, "Bela snipe time")
        print()
        print("Bela snipe time playlist created!")
        print()

def top_ranked():
    print("--- Get top plays ---")
    print("This is an old program I made for creating a playlist of top plays that I decided to include here")
    if userData["userID"] == None or userData["directory"] == None:
        print("Please set the user data from the menu first")
    else:
        loop = True
        while loop:
            try:
                limit = int(input("enter number of maps in playlist -> "))
                loop = False
            except:
                print("enter an integer")
        songs = []
        max_page = ((limit - 1) // 100) + 2
        failed = False
        for page in range(1, max_page):
            if page < max_page - 1:
                req_limit = 100
            else:
                req_limit = limit - ((max_page - 2) * 100)
            print("sending ScoreSaber api request " + str(page))
            url = ("https://scoresaber.com/api/player/" + str(userData["userID"]) + "/scores?limit=" + str(req_limit) + "&sort=top&page=" + str(page))
            api = requests.get(url)
            if str(api) == "<Response [200]>":
                print("api response: " + str(api) + " (good)")
            else:
                print("api response: " + str(api) + " (bad)")

            try:
                print("getting JSON data for playlist")
                dic = json.loads(api.content)
                arr = dic["playerScores"]
                for i in arr:
                    leaderboard = i["leaderboard"]
                    hash = leaderboard["songHash"]
                    diff = diff_dic[leaderboard["difficulty"]["difficulty"]]
                    songs.append({
                        "hash": hash,
                        "difficulties": [
                            {
                                "characteristic": "Standard",
                                "name": diff
                            }
                        ]
                    })
            except:
                print("FAILED")
                print("possible problems:")
                print(" - incorrect ScoreSaberID")
                print(" - You asked for more maps than you have ranked plays")
                print(" - api just not found :(")
                failed = True
                break

        if not failed:
            print("creating playlist of " + str(len(songs)) + " maps")
            playlist = {
                "playlistTitle": "Top Ranked",
                "playlistAuthor": None,
                "playlistDescription": None,
                "songs": songs
            }

            print("creating bplist file in playlist folder of directory")
            try:
                with open((userData["directory"] + "\\Playlists\\!Top Ranked Playlist.bplist"), "w") as file:
                    json.dump(playlist, file)
                    file.close()
                print("all processes finished successfully :)")
            except:
                print("FAILED")
                print("possible problems:")
                print(" - invalid directory")
                print(" - your beat saber directory is very scuffed (doesn't have a playlist folder)")
    

def player_search(name):
    print("Searching for: " + name)
    api = requests.get("https://scoresaber.com/api/players?search=" + name)
    dic = json.loads(api.content)
    players = dic["players"]
    print("Search result:")
    if len(players) != 1:
        for i in range(len(players)):
            print("\t- " + str(i+1) + ": " + players[i]["name"] + " (" + str(players[i]["rank"]) + ")")
        while True:
            try:
                x = int(input("Select (0 for back) -> ")) - 1
                if x >= 0:
                    player = {
                        "name": players[x]["name"],
                        "id": players[x]["id"],
                        "rank": players[x]["rank"]
                    }
                    return player
                elif x == -1:
                    return None
            except:
                pass
    else:
        print("\t- " + players[0]["name"] + " (" + str(players[0]["rank"]) + ")")
        while(True):
            x = input("Is this correct (y/n) -> ").lower()
            if x == "y":
                player = {
                    "name": players[0]["name"],
                    "id": players[0]["id"],
                    "rank": players[0]["rank"]
                }
                return player
            elif x == "n":
                return None
            

def get_total(id):
    api = requests.get("https://scoresaber.com/api/player/" + id + "/full")
    dic = json.loads(api.content)
    return dic["scoreStats"]["rankedPlayCount"]

def get_scores(id):
    songs = []
    total = get_total(id)
    max_page = ((total - 1) // 100) + 2
    for page in range(1, max_page):
        if page < max_page - 1:
            req_limit = 100
        else:
            req_limit = total - ((max_page - 2) * 100)
        url = ("https://scoresaber.com/api/player/" + id + "/scores?limit=" + str(req_limit) + "&sort=top&page=" + str(page))
        api = requests.get(url)
        print("request: " + str(page))
        try:
            dic = json.loads(api.content)
        except:
            print("Invalid ID")
            return None
        arr = dic["playerScores"]
        for i in arr:
            score = i["score"]["baseScore"]
            leaderboard = i["leaderboard"]
            hash = leaderboard["songHash"]
            name = leaderboard["songName"]
            diff = diff_dic[leaderboard["difficulty"]["difficulty"]]
            songs.append({
                "score": score,
                "hash": hash,
                "name": name,
                "difficulties": [
                    {
                        "characteristic": "Standard",
                        "name": diff
                    }
                ]
            })
    return songs

def get_maps(id1, id2, include):
    songs = []
    print()
    print("Sending ScoreSaber api requests...")
    scores1 = get_scores(str(id2))
    scores2 = get_scores(str(id1))
    if scores1 == None or scores2 == None:
        return None
    for score1 in scores1:
        exist = False
        for score2 in scores2:
            if (score1["hash"] == score2["hash"]) and (score1["difficulties"][0]["name"] == score2["difficulties"][0]["name"]):
                exist = True
                if score1["score"] > score2["score"]:
                    songs.append(score1)
        if not exist and include:
            songs.append(score1)
    return songs

def make_playlist(songs, name):
    arr = []
    for song in songs:
        arr.append({
            "hash": song["hash"],
            "difficulties": song["difficulties"]
        })
    playlist = {
            "playlistTitle": name,
            "playlistAuthor": None,
            "playlistDescription": None,
            "songs": arr
    }

    with open((userData["directory"] + "\\Playlists\\" + name + ".bplist"), "w") as file:
        json.dump(playlist, file)
        file.close()

diff_dic = {1: "Easy", 3: "Normal", 5: "Hard", 7: "Expert", 9: "ExpertPlus"}
belaID = 76561199003743737
try:
    file = open("UserData.JSON", "r")
    userData = json.load(file)
    file.close()
    if userData["userID"] == None or userData["directory"] == None:
        exist = False
    else:
        exist = True
except:
    userData = {"userID": None, "directory": None}
    exist = False

menu(exist)

file = open("UserData.JSON", "w")
json.dump(userData, file)
file.close()
