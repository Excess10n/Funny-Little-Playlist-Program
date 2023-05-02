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

print("sending ScoreSaber api request")
url = ("https://scoresaber.com/api/player/" + str(userID) + "/scores?limit=" + str(limit) + "&sort=top")
api = requests.get(url)
if str(api) == "<Response [200]>":
    print("api response: " + str(api) + " (good)")
else:
    print("api response: " + str(api))

print("creating JSON file for playlist")
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

playlist = {
    "playlistTitle": "Top Ranked",
    "playlistAuthor": None,
    "playlistDescription": None,
    "songs": songs
}

try:
    with open((directory + r"\Playlists\!Top Ranked Playlist.JSON"), "w") as file:
        json.dump(playlist, file)
        file.close()
    print("all processes finished successfully :)")
except:
    print("invalid directory")

input("[enter to close]")
