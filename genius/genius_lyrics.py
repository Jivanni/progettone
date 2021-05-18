import re
import csv
import os
import lyricsgenius


UNIQUE_SONG_PATH = "unique_songs_v2.csv"
DOWNLOAD_DIR = "lyrics"
curr_row = 0

GENIUS_TOKEN = "kkAcDUBp0WMs-dHSKsmGZweB9xLdDBFmXy7NWaWFGBzC0w3HJDMJhNUhihFJns4n"

genius = lyricsgenius.Genius(GENIUS_TOKEN, remove_section_headers=True)

try:
    with open("state.txt", "r", encoding="utf-8") as state:
        curr_row = int(state.readlines()[0])
except FileNotFoundError:
    with open("state.txt", "w", encoding="utf-8") as state:
        state.write("0")

print(f"Resuming from row {curr_row}")

def unpack_artist_list(str_repr):
    output = []
    try:
        output.extend(eval(str_repr))
    except:
        output.append(str_repr)
    finally:
        return output


def get_lyrics(song_name, artist_name, clean_filename):
    """
    This function retrieves the songs' lyrics from genius using song_name and artist_name and write them on a txt
    """
    song_lyrics = genius.search_song(song_name, artist_name, get_full_info=True)
    if song_lyrics:
        path = os.path.join(DOWNLOAD_DIR, clean_filename)
        with open(path, "w", encoding="utf-8") as file_hand:
            file_hand.write(song_lyrics.lyrics)
        return True
    return False


with open(UNIQUE_SONG_PATH, 'r', encoding="utf-8") as input_handle:
    my_reader = csv.reader(input_handle, delimiter=";")
    for i in range(curr_row):
        next(my_reader, None)

    total_saved = 0
    total_not_found = 0
    list_not_found = []
    """
    We search each song on genius using a combination of the columns "original_song_name" and "song_name"
    for the song_name; and the columns "original_artists_name" and "artist_names" for artist_name. 
    In this way we maximize our chances to find the songs lyrics on genius
    """
    for id, original_song_name, original_artists_name, song_name, artists_names in my_reader:

        artists_names = unpack_artist_list(artists_names)
        clean_filename = re.sub(r"[><:\"?*|\\/]", "", f"{song_name}_{artists_names[0]}.txt")

        lyric = get_lyrics(song_name, artists_names[0], clean_filename)

        if not lyric:
            total_not_found += 1
            list_not_found.append(song_name + "_" + artists_names[0])
            print("Total songs not found: ", total_not_found)
            continue

        total_saved += 1
        print("Total songs saved: ", total_saved)


    print("Finished!")
    print("The total songs saved are: ", total_saved)
    print("The total songs not found are: ", total_not_found)
    print("This is the list of the missing songs: ", list_not_found)


with open("list_total_lyrics_not_found.txt", "w", encoding="utf-8") as file1:
    file1.write(list_not_found)









