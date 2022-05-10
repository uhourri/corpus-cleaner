from tkinter import *
from tkinter import filedialog
import os
import sys
import re
from tkinter import messagebox
from langdetect import detect, DetectorFactory
from matplotlib import pyplot as plt
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.isri import ISRIStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import operator
import arabic_reshaper
from bidi.algorithm import get_display
from wordcloud import WordCloud

root = Tk()
root.title('Text Mining - TP08')
root.iconbitmap('C:/Users/UNES/Pictures/Camera Roll/logo.ico')
root.geometry("1080x600")

global open_status_name
open_status_name = False

global selected
selected = False

corpus = []
global directory

#####################

def read_lines(filename):
    try:
        myfile = open(filename, "r", encoding="utf-8")
    except:
        print("Can't open file ", filename)
        sys.exit()
    return myfile.readlines()

def tokenize(text):
    tokens = re.split("\W+", text)
    return tokens

def normalize(text):
    normalMap = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
                 'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
                 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
                 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                 'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
                 'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
                 'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
                 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
                 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
                 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
                 'Ñ': 'N', 'ñ': 'n',
                 'Ç': 'C', 'ç': 'c',
                 '§': 'S',  '³': '3', '²': '2', '¹': '1'}

    return text.translate(str.maketrans(normalMap))

def to_lower_case(text):
    return text.lower()

def remove_spaces(tokens):
    while '' in tokens:
        tokens.remove('')
    return tokens

def detect_lang(text):
    DetectorFactory.seed = 0
    return detect(text)

def remove_stop_words(values):
    if detect_lang(" ".join(values)) == "fr":
        lines = read_lines(
            'C:/Users/UNES/Documents/Projects/Python/Text Mining/TP08/stop_words/stop_words_french.txt')
    if detect_lang(" ".join(values)) == "ar":
        lines = read_lines(
            'C:/Users/UNES/Documents/Projects/Python/Text Mining/TP08/stop_words/stop_words_arabic.txt')

    for line in lines:
        word = line.split('\n')
        while word[0] in values:
            values.remove(word[0])
    return values

def remove_digits(values):
    new_items = [item for item in values if not item.isdigit()]
    return new_items

def stemmer(values):
    if detect_lang(" ".join(values)) == "fr":
        stemmer = FrenchStemmer()
    if detect_lang(" ".join(values)) == "ar":
        stemmer = ISRIStemmer()
    result = []
    for value in values:
        result.append(stemmer.stem(value))
    return result

def reverse_sort(values):
    result = {}
    for i in values:
        if i in result:
            result[i] += 1
        else:
            result[i] = 1
    result = dict(
        sorted(result.items(), key=operator.itemgetter(1), reverse=True))
    return result

def sort(values):
    result = {}
    for i in values:
        if i in result:
            result[i] += 1
        else:
            result[i] = 1
    result = dict(sorted(result.items(), key=operator.itemgetter(1)))
    return result

def to_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    converted = get_display(reshaped_text)
    return converted

def clean_extract(text):
    normalized = normalize(text)
    lower_case = to_lower_case(normalized)
    tokens = tokenize(lower_case)
    removed_stops = remove_stop_words(tokens)
    removed_spaces = remove_spaces(removed_stops)
    removed_digits = remove_digits(removed_spaces)
    stemmes = stemmer(removed_digits)
    return stemmes

def trace_word_cloud():
    data = my_text.get(1.0, END)
    data = arabic_reshaper.reshape(data)
    data = get_display(data)
    word_cloud = WordCloud(font_path='arial', background_color='white', collocations=False,
                           mode='RGB', width=2000, height=1000).generate(data)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()
    plt.close()

def trace_most_frequented():
    values = my_text.get(1.0, END).split(" ")
    tokens = reverse_sort(values)

    left = []
    left.extend(range(1, 21))

    tick_label = []
    height = []

    values = tokens.values()
    keys = tokens.keys()
    counter = 0
    for key, value in zip(keys, values):
        if(counter == 20):
            break
        tick_label.append(to_arabic(key))
        height.append(value)
        counter += 1

    plt.bar(left, height, tick_label=tick_label,
            width=0.2, color=['red', 'blue'])

    # Rotation of the bars names
    plt.xticks(rotation=90)

    plt.xlabel('mots')
    plt.ylabel('occurences')
    plt.subplots_adjust(bottom=0.19)
    plt.title('Les  20 mots plus frequents')

    plt.show()

def trace_fewest_frequented():
    values = my_text.get(1.0, END).split(" ")
    tokens = sort(values)

    left = []
    left.extend(range(1, 21))

    tick_label = []
    height = []

    values = tokens.values()
    keys = tokens.keys()
    counter = 0
    for key, value in zip(keys, values):
        if(counter == 20):
            break
        tick_label.append(to_arabic(key))
        height.append(value)
        counter += 1

    plt.bar(left, height, tick_label=tick_label,
            width=0.2, color=['red', 'blue'])

    # Rotation of the bars names
    plt.xticks(rotation=90)

    plt.xlabel('mots')
    plt.ylabel('occurences')
    plt.subplots_adjust(bottom=0.19)
    plt.title('Les 20 mots moins frequents')

    plt.show()

def trace_tfidf():
    tfidf = TfidfVectorizer()
    features = tfidf.fit_transform(corpus)
    print(pd.DataFrame(features.todense(), columns=tfidf.get_feature_names_out()))
    messagebox.showinfo("Message", "Voir le terminale !")

#####################


def read_file(filename):
    try:
        myfile = open(filename, "r", encoding="utf-8")
    except:
        print("Can't open file ", filename)
        sys.exit()
    return myfile.read().replace('\n', ' ')

def open_corpus():
    my_text.delete("1.0", END)
    global directory
    directory = filedialog.askdirectory(
        initialdir="C:/Users/UNES/Documents/Projects/Python/Text Mining/TP08", title="Open Folder")
    global corpus
    corpus.clear()
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            text = read_file(f)
            cleaned = clean_extract(text)
            corpus.append(" ".join(cleaned))

    my_text.insert(END, " ".join(corpus))
    return corpus

def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Users/UNES/Documents/Projects/Python/Text Mining/",
                                             title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        name = name.replace(
            "C:/Users/UNES/Documents/Projects/Python/Text Mining/", "")
        root.title(f'{name} - text Mining!')
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()

def save_file():
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()
        status_bar.config(text=f'Saved: {open_status_name}')
        name = open_status_name
        name = name.replace(
            "C:/Users/UNES/Documents/Projects/Python/Text Mining/", "")
        root.title(f'{name} - Text Mining!')
    else:
        save_as_file()

def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            selected = my_text.selection_get()
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)

def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)

def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)

def select_all(e):
    my_text.tag_add('sel', '1.0', 'end')

def clear_all():
    my_text.delete(1.0, END)

######################

toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

my_frame = Frame(root)
my_frame.pack(pady=5)

text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="grey",
               selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.pack()

text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open Corpus", command=open_corpus)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(
    False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Copy", command=lambda: copy_text(
    False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Paste",
                      command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=lambda: select_all(
    True), accelerator="(Ctrl+a)")
edit_menu.add_command(label="Clear", command=clear_all)

status_bar = Label(root, text='Ready', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)
root.bind('<Control-A>', select_all)
root.bind('<Control-a>', select_all)

cloud_button = Button(
    toolbar_frame, text="Nuage de mots", command=trace_word_cloud)
cloud_button.grid(row=0, column=1, padx=5, pady=5)

most_frequented_button = Button(
    toolbar_frame, text="20 mots les plus utilisés", command=trace_most_frequented)
most_frequented_button.grid(row=0, column=2, padx=5, pady=5)

fewest_frequented_button = Button(
    toolbar_frame, text="20 mots les moins utilisés", command=trace_fewest_frequented)
fewest_frequented_button.grid(row=0, column=3, padx=5, pady=5)

tfidf_button = Button(
    toolbar_frame, text="Matrice TF-IDF", command=trace_tfidf)
tfidf_button.grid(row=0, column=4, padx=5, pady=5)

root.mainloop()