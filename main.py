import requests
import json

diff_dic = {1: "Easy", 3: "Normal", 5: "Hard", 7: "Expert", 9: "ExpertPlus"}

def input_id():
    loop = True
    while loop:
        try:
            userID = int(input("enter your ScoreSaberID -> "))
            loop = False
        except:
            print("invalid ScoreSaberID (make sure it's just the numbers at the end of the url)")
    return userID

def save_data(userID, directory):
    data = {"userID": userID, "directory": directory}
    with open("UserData.JSON", "w") as file:
        json.dump(data, file)
        file.close()
    print("user data saved")

print("loading user data")
try:
    file = open("UserData.JSON", "r")
    file.close()
except:
    print("creating new user data file (UserData.JSON)")
    userID = input_id()
    directory = input("enter your Beat Saber directory -> ")
    save_data(userID, directory)

with open("UserData.JSON", "r") as file:
    save = False
    data = json.load(file)
    if data["userID"] == None:
        userID = input_id()
        save = True
    else:
        userID = data["userID"]
    if data["directory"] == None:
        directory = input("enter your Beat Saber directory -> ")
        save = True
    else:
        directory = data["directory"]
    file.close()

if save:
    save_data(userID, directory)

loop = True
while loop:
    try:
        limit = int(input("enter number of maps in playlist (max 100)(enter 0 to change user data) -> "))
        loop = False
    except:
        print("enter an integer")
    if limit <= 0:
        userID = input_id()
        directory = input("enter your Beat Saber directory -> ")
        save_data(userID, directory)
        loop = True

songs = []
max_page = ((limit - 1) // 100) + 2
failed = False
for page in range(1, max_page):
    if page < max_page:
        req_limit = 100
    else:
        req_limit = limit - (max_page * 100)
    print("sending ScoreSaber api request " + str(page))
    url = ("https://scoresaber.com/api/player/" + str(userID) + "/scores?limit=" + str(req_limit) + "&sort=top&page=" + str(page))
    api = requests.get(url)
    if str(api) == "<Response [200]>":
        print("api response: " + str(api) + " (good)")
    else:
        print("api response: " + str(api) + " (bad)")

    try:
        print("getting JSON data for playlist")
        dic = json.loads(api.content)
        arr = dic["playerScores"]
        songs = []
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
        print(" - I fucked up")
        print(" - api just not found :(")
        failed = True
        break

if not failed:
    playlist = {
        "playlistTitle": "Top Ranked",
        "playlistAuthor": None,
        "playlistDescription": None,
        "songs": songs
    }

    print("Creating bplist file in playlist folder of directory")
    try:
        with open((directory + r"\Playlists\!Top Ranked Playlist.bplist"), "w") as file:
            json.dump(playlist, file)
            file.close()
        print("all processes finished successfully :)")
    except:
        print("FAILED")
        print("possible problems:")
        print(" - invalid directory")
        print(" - your beat saber directory is very scuffed (doesn't have a playlist folder)")

input("[enter to close]")
