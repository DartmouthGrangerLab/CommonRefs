# CommonRefs
Small Python script to match references from a set of papers and find which ones they have in common.

Currently it relies on the user to create a directory and fill it with plain text files. Those files represent the references cut and pasted from the papers to be checked for references in common. The script will output matches. You get at least two matches for each one reference in common. It's sort of primitive code, good part is the use of a fuzzy match on the references so they don't have to be same format.

I don't have time now to make it better, it gave me what I needed, more places to look for relevant papers -- all the papers citing those found to be used in common by the original set.

Fuzzy matching makes for a requirement of installing NLTK toolkit and the Treebank module (my thanks to Srvanna Reddy for making me able to appreciate the NLTK toolkit ;-))

