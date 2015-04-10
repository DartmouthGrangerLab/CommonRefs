#!/usr/bin/python
'''
Copyright (C) 2015 Brett Tofel, Dartmouth College

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

__author__ = 'bentito'
import os
import re
import string
import nltk.corpus
import warnings

warnings.simplefilter("ignore")

# Get default English stopwords and extend with punctuation
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation)
stopwords.append('')

# Create tokenizer
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()

def intersect(a, b):
     return list(set(a) & set(b))

def is_ci_token_stopword_match(a, b):
    """Check if a and b are matches."""
    tokens_a = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(a) \
                    if token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in tokenizer.tokenize(b) \
                    if token.lower().strip(string.punctuation) not in stopwords]

    intVal = len(intersect(tokens_a, tokens_b))

    # print "intersect",intVal #debug

    if (intVal > 10): # 10 is just min intersection to call it a match
        return True
    return False

path = r"/Users/bentito/Documents/video_object_detection_paper_citations"
data = {}
for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
        with open(dir_entry_path, 'r') as my_file:
            data[dir_entry] = my_file.read()

storeCites = {}
for paper in data:
    cites = data[paper]
    findCite = re.compile(r'(?s)\[\d+\](.*?)\[\d+\]')
    citations = list()
    while True:
        try:
            m = findCite.search(cites).group(1)
        except:
            break
        citations.append(m)
        newBegin = findCite.search(cites).end()
        cites=cites[newBegin-5:] # 5 is a quick hack to jump back before citation number
    if citations:
        # print paper,len(citations),citations
        storeCites[paper] = citations
    else:
        # print "other cite format"
        cites = data[paper]
        findCite = re.compile(r'(?s)\d+\.(.*?)\d+\.')
        while True:
            try:
                m = findCite.search(cites).group(1)
            except:
                break
            citations.append(m)
            newBegin = findCite.search(cites).end()
            cites=cites[newBegin-5:]
        if citations:
            # print paper,len(citations),citations
            storeCites[paper] = citations
        else:
            print "failed to decode cite format"

count = 0
for paper in storeCites:
    storeCopy = dict(storeCites)
    del storeCopy[paper]
    citations = storeCites[paper]
    # print len(citations)+1 #debug
    for cite in citations:
        for otherPaper in storeCopy:
            otherCitations = storeCopy[otherPaper]
            for otherCite in otherCitations:
                match = is_ci_token_stopword_match(cite, otherCite)
                if (match):
                    count = count + 1
                    print paper, "\n", ">>>>>>", cite, "\n*************** matches *****************\n"
                    print otherPaper, "\n", ">>>>>>", otherCite
                    print "--------------------------------------------------------------------------------"
                else:
                    pass
print count #debug

