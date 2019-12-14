# -*- encoding: utf-8 -*-

import os
import re

def Get_LC_TEXT(line):
	text = re.search('LC_TEXT\("(.*)"\)', line, re.IGNORECASE)
	if text:
		return text.group(1)

	return None

def Get_Translation(line):
	text = re.search('"(.*)";', line, re.IGNORECASE)
	if text:
		return text.group(1)

	return None

if __name__ == "__main__":
	curDir = os.getcwd() + "\\"

	duplicate_list = []
	default_translate_list = {}

	with open(curDir + "locale_string.txt", 'r', encoding="ISO8859") as translateFile:
		sentence = ""
		for (i, line) in enumerate(translateFile):
			if line:
				if (i % 3) == 0:
					sentence = Get_Translation(line)
				elif (i % 3) == 1:
					default_translate_list[sentence] = Get_Translation(line)
					sentence = ""

	srcDir = curDir + "game\src\\"
	for path, subdirectories, files in os.walk(srcDir):
		for file in files:

			with open(srcDir + file, 'r', encoding="ISO8859") as srcFile:

				file_content = ""
				for (i, line) in enumerate(srcFile):

					if "LC_TEXT" in line:
						lc_text = Get_LC_TEXT(line)
						if lc_text and lc_text in default_translate_list:
							line = line.replace(lc_text, default_translate_list[lc_text])
							# print(line) # Debug only
						else:
							print("WARNING: line not in locale_string: '%s'" % line)

						lc_text = Get_LC_TEXT(line)
						if not lc_text in duplicate_list:
							duplicate_list.append(lc_text)

					file_content += line

				new_file = open(curDir + "game_new\src\\" + file, "w", encoding="utf-8")
				new_file.write(file_content)
				new_file.close()

	newTranslation = open(curDir + "locale_string.new.txt", "w")
	newText = ""

	for line in duplicate_list:
		newText += "\"%s\";\n\"%s\";\n\n" % (line, line)

	newTranslation.write(newText)
	newTranslation.close()
