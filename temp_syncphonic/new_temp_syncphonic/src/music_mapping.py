def map_mood_to_music(mood):
    # Adjusted mapping example with file paths
    mood_to_music = {
        0: "C:\\Users\\sreec\\OneDrive\\Desktop\\Syncphonic\\Sad Song.mp3",
        1: "C:\\Users\\sreec\\OneDrive\\Desktop\\Syncphonic\\Neutral Song.mp3",
        2: "C:\\Users\\sreec\\OneDrive\\Desktop\\Syncphonic\\Happy Song.mp3",
    }
    return mood_to_music.get(mood, "C:\\Users\\sreec\\OneDrive\\Desktop\\Syncphonic\\Default Song.mp3")
