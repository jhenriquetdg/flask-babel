# 

import os
import re
import sys

from shutil import copyfile

from googletrans import Translator

translator = Translator()
translation_dir = "/home/zetdg/Devasoft/devablog/app/translations"

lang_dir = sys.argv
# lang_dir = os.listdir(translation_dir)

if len(lang_dir) == 1:
    lang_dir = os.listdir(translation_dir)
else:
    lang_dir = lang_dir[1:]


for f, lang_acronyms in enumerate(lang_dir):
    message_file = os.path.join(translation_dir, lang_acronyms, 'LC_MESSAGES/messages.po')

    print(str(f) + ' of ' + str(len(lang_dir)), lang_acronyms, message_file)

    if not os.path.isfile(message_file):
        print("\tFile {} doesn't exist".format(message_file))
        continue

    mfile = open(message_file, "r")

    id_source = []
    id_translate = []
    translated_lines = []

    all_lines = mfile.readlines()
    mfile.close()
    translated_lines = all_lines

    for l, line in enumerate(all_lines):
        split_line = line.split(" ")
        if split_line[0] == 'msgid':
            id_source.append(l)
        if split_line[0] == 'msgstr':
            id_translate.append(l)

    cont = 0
    for s, t in zip(id_source, id_translate):
        cont = cont + 1
        source_text = re.findall('(\".+?\")', all_lines[s])
        translate_text = re.findall('(\".+?\")', all_lines[t])

        if not len(translate_text) == 0:
            continue

        if len(source_text):
            print(str(cont) + ' of ' + str(len(id_translate)))
            source_text = source_text[0]
            source_text = source_text[1:-1]

            Splitted = re.split("(\%\(.+?\)s)", source_text)
            # TagName = re.findall("(\%\(.+?\)s)", source_text)
            Dummy = re.sub("(\%\(.+?\)s)", "_@@_", source_text)

            Translated = translator.translate(Dummy, dest=lang_acronyms)
            Translated = Translated.text

            SplittedTranslation = re.split("(_\s*@@\s*_)", Translated)

            translated_text = []
            for c, chunk in enumerate(Splitted):
                if c % 2:
                    translated_text.append(Splitted[c])
                else:
                    translated_text.append(SplittedTranslation[c])

            translated_text = ''.join(translated_text)
            translated_lines[t] = 'msgstr "' + translated_text + '"\n'

            # print(source_text, '->', translated_lines[t], end='')
            print('\t' + source_text, '->', translated_text)

    copyfile(message_file, message_file + '.bkp')
    os.remove(message_file)

    mfile = open(message_file, "w")
    for line in translated_lines:
        mfile.write("%s" % line)

    mfile.close()
