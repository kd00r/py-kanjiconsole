# Missing Column header:
# Core-index,Vocab-KO-Index,Sent-KO-Index,New-Opt-Voc-Index,Opt-Voc-Index,Opt-Sen-Index,jlpt ,Vocab-expression,Vocab-kana,Vocab-meaning,Vocab-sound-local,Vocab-pos,Sentence-expression,Sentence-kana,Sentence-meaning,Sentence-sound-local,Sentence-image-local,Vocab-furigana,Sentence-furigana,Sentence-Cloze

import csv
from os import stat
import random
from Levenshtein import distance as levenshtein_distance # for a little kind error tolerance!

#path_kana = "japan\Optimized Kore - Sheet1.csv" # OLD
path_kana = "japan/Optimized_Kore_shortanswers_col9.csv"
path_stats = "japan/stats.csv"
first_hundred = []
first_hundred_stats = [0] * 99
global data
data = [0] * 99
current_entry = 0
global exit_now
exit_now = False

# open stat file and fill data list
with open(path_stats, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        counter = 0
        for row in reader:
            data[counter] = int(row['stats'])
            counter += 1

def save_progress(path_stats, data):
    with open(path_stats, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['stats']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({'stats': str(row)})

# open kana sheet and write first hundred entries to first_hundred list
with open(path_kana, newline='', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in reader:
        if int(row[5]) < 100:
            first_hundred.append(row)

def fetch_pair(kana_list, count, mode):
    eng = kana_list[count][9].lower()

    if mode == "hiragana":
        jap = kana_list[count][8]
    elif mode == "kanji":
        jap = kana_list[count][7]
    return eng, jap

def fetch_all(kana_list, count):
    return kana_list[count]

def review(kana_list, count, mode):
    eng, jap = fetch_pair(kana_list, count, mode)
    answer = input(jap + "? ")
    if answer == eng:
        print("Yayy!")
        return True
    elif answer != eng:
        print("Sorry, the correct translation is: " + eng)
        return False

def review_quiz(kana_list, count, mode): # fix me pls
    eng, jap = fetch_pair(kana_list, count, mode)
    answer = input(jap + "? ")
    data = fetch_all(kana_list, random.randrange(0, 99))

def review_helper(kana_list, count, mode):
    global exit_now
    eng, jap = fetch_pair(kana_list, count, mode)
    answer = input(jap + "? ").lower()
    distance = levenshtein_distance(answer, eng)
    if answer == "@QUIT" or answer == "@EXIT" or answer == "@quit" or answer == "@exit":
        exit_now = True
        return False, count # subtract one from stats.csv for an extra reminder next time
    elif distance < 2:
        print("Yayy! True with distance: " + str(distance)) # this is wayy to kind, fixme!
        return True, count
    elif distance > 2:
        print("Sorry, the correct translation is: " + eng + " With distance: " + str(distance))
        return False, count

def fetch_difficult_words(data, reverse):
    if reverse:
        return data.index(max(data))
    else:
        return data.index(min(data))

def difficult_words(kana_list, datas):
    diff_index = fetch_difficult_words(datas, False)
    #print(kana_list[diff])
    return diff_index

def main(kana_list):
    global current_entry
    global first_hundred_stats
    diff_index = difficult_words(first_hundred, data)

    # Temporary solution to setting the kana mode:
    correct, count = review_helper(kana_list, diff_index, "hiragana")
    #correct, count = review_helper(kana_list, diff_index, "kanji")


    #correct, count = review_helper(kana_list, current_entry, "hiragana")
    if correct:
        data[count] += 1
    if not correct:
        data[count] -= 1
    current_entry += 1


while not exit_now:
    main(first_hundred)
    save_progress(path_stats, data)

save_progress(path_stats, data) # to catch the last save after exit_now turns True