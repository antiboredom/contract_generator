# -*- coding: utf-8 -*-
import sys
import random
import regex
import re
from pattern.en import verbs, conjugate, PARTICIPLE, FUTURE, IMPERATIVE, SINGULAR, INFINITIVE, PRESENT
from pattern.en import tag, tokenize
from nltk.corpus import names

def wrap(text, width):
    return reduce(lambda line, word, width=width: '%s%s%s' %
                (line,
                    ' \n'[(len(line)-line.rfind('\n')-1
                        + len(word.split('\n',1)[0]
                            ) >= width)],
                        word),
                text.split(' ')
            )

the_artist = "The Artist"
phrases = ["shall", "must", "agrees to", "will", "is obliged to", "is required to", "hereby agrees to"]
section_prefixes = ["Within 30 days", "Within 6 days", "Within one year", "By no later than May 22nd,", "By no later than April 14th,", "In a timely fashion"]

names = [name for name in names.words('male.txt')] + [name for name in names.words('female.txt')]
name_ex = "|".join(names)
def name_replace(line):
    line = re.sub(r'(\b([Hh]e|[Ss]he)\b)|(Mr|Mrs|Ms)\. \w+', the_artist, line, flags=re.MULTILINE)
    line = re.sub(r'\b(' + name_ex + r')\b', the_artist, line, flags=re.MULTILINE)
    return line

content = ""
for line in sys.stdin:
    content += line + " "

for t in ["\n", "\r", "\t"]:
    content = content.replace(t, "")

content = name_replace(content)

pat = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
sents = tokenize(content)
sentences = []

for sent in sents:
    if the_artist not in sent or '"' in sent or "?" in sent or "!" in sent or "'" in sent:
        continue
    toPrint = False
    output = []
    i = 0
    prev_word=""
    for word, pos in tag(sent):
        if pos == "VBD" or pos=="VBZ":
            toPrint = True
            if  prev_word == "Artist":
                output += random.choice(phrases).split() + [conjugate(word, tense=INFINITIVE)]
            else:
                output += ["will", conjugate(word, tense=INFINITIVE)]
        else:
            output.append(word)

        i += 1
        prev_word = word

    if toPrint:
        try:
            sentences += ["The"] + output[output.index("Artist"):]
        except(ValueError):
            pass


detokenizer = regex.RegexDetokenizer()
text = detokenizer.detokenize(sentences)

i = 0
section = 1
output = ""

sentences = pat.findall(text)

while (i < len(sentences)):
    j = random.randint(3, 6)
    if (j > len(sentences) - 1):
        j = len(sentences) -1
    output += "SECTION " + str(section) + "\n"
    if (random.random() > .7):
        output += random.choice(section_prefixes) + " "
    output += " ".join(sentences[i:j+i])
    output += "\n\n\n"
    i = i + j
    section = section + 1

doc_width = 60
header =  "=" * doc_width + "\n"
header += "* CONTRACT *".center(doc_width, "*") + "\n"
header +=  "=" * doc_width + "\n\n\n\n"
header += "_____________________________, henceforth known as \"The Artist,\" agrees to the following:\n\n\n"

footer = "=" * doc_width + "\n\n\n"
footer += "Date:\t\t ________________________\n\n\n"
footer += "Name:\t\t ________________________\n\n\n"
footer += "Signature:\t ________________________\n\n\n"

output = header + output + footer

print wrap(output, doc_width)
