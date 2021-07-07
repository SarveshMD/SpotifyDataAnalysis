import sqlite3
from datetime import timedelta
from tabulate import tabulate

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()
songsArtistsConn = sqlite3.connect("../Databases/songsArtists.sqlite")
songsArtistsCursor = songsArtistsConn.cursor()

summary = {}
cursor.execute('''
CREATE TABLE IF NOT EXISTS songSummary (
    trackId INTEGER UNIQUE,
    totalMsPlayed INTEGER
    )
''')
cursor.execute('SELECT * FROM streamingHistory')
streamingHistory = cursor.fetchall()
for item in streamingHistory:
    endTime = item[0]
    trackId = item[1]
    artistId = item[2]
    msPlayed = item[3]
    if trackId not in summary.keys():
        summary[trackId] =  msPlayed
    else :
        summary[trackId] += msPlayed

for trackId, totalMsPlayed in summary.items():
    cursor.execute("INSERT OR IGNORE INTO songSummary (trackId, totalMsPlayed) VALUES (?, ?)", (trackId, totalMsPlayed))
connection.commit()

cursor.execute("SELECT * FROM songSummary ORDER BY totalMsPlayed DESC")
summaryFromTable = cursor.fetchall()

i = 0
table = list()
for trackId, totalMsPlayed in summaryFromTable:
    i += 1
    songsArtistsCursor.execute(f'SELECT trackName FROM Songs WHERE id IS {trackId}')
    trackName = songsArtistsCursor.fetchone()[0]
    convertedPlayed = str(timedelta(milliseconds=totalMsPlayed)).split(":")
    hours = int(convertedPlayed[0])
    minutes = int(convertedPlayed[1])
    seconds = float(convertedPlayed[2])
    table.append([i, trackName, hours, minutes, f"{seconds:.2f}"])
table = tabulate(table, headers=['S.No', 'Track Name', 'Hours', 'Minutes', 'Seconds'], tablefmt="pipe")
print()
print(table)