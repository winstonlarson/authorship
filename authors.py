# find all authors and last authors on PubMed Microbiome papers

import pandas as pd
import re

papertype = ['microbiomeold'] #['microbiome', 'comp', 'qiime', 'host']

for paper in papertype:

    filename = paper + '_papers.txt'
    paperfile = open(filename)
    paperread = paperfile.read()

    papers = paperread.replace('\n\n\n', '\t').replace('\n', ' ').replace('\t', '\n')
    papers = papers.split('\n')

    paperauthors = []
    for row in papers:
        authorlist = re.findall(':.*?\.', row)
        authorlist = authorlist[0]
        authorlist = authorlist.replace(': ', '')
        authorlist = authorlist.replace('.', '')
        paperauthors.append(authorlist)

    authors = []
    lastandfirst = []
    for row in paperauthors:
        lineauthors = row.split(', ')
        for item in lineauthors:
            authors.append(item)
        last = len(lineauthors) - 1
        lastandfirst.append([lineauthors[last], lineauthors[0]])

    authors = pd.Series(authors)
    lastandfirst = pd.DataFrame(lastandfirst)
    lastandfirst.columns = ['Last', 'First']
    firstauthors = lastandfirst.First
    lastauthors = lastandfirst.Last

    lastcounts = lastauthors.value_counts()
    authorcounts = authors.value_counts()
    firstcounts = firstauthors.value_counts()

    top30last = lastcounts.head(30)
    top30authors = authorcounts.head(30)
    top30first = firstcounts.head(30)

    lastlist = top30last.index.tolist()

    fileout = 'top10labs_' + paper + '.txt'
    textout = open(fileout, 'w')
    textout.write("Top first authors in the top 10 labs\n\n")

    row = 0
    while row < 10:
        currentlast = lastandfirst[lastandfirst.Last.isin([lastlist[row]])]
        firstinlast = currentlast.First.value_counts()
        firstinlast = firstinlast.head(5)
        lab = 'Lab: ' + lastlist[row] + ' (Papers: ' + str(top30last[row]) + ')\n'
        textout.write(lab)
        textout.write(firstinlast.to_string())
        textout.write('\n\n')
        row += 1
    textout.close()

    fileout = 'topauthors_' + paper + '.txt'
    textout = open(fileout, 'w')
    textout.write('Top 30 last authors\n')
    textout.write(top30last.to_string())
    textout.write('\n\nTop 30 first authors\n')
    textout.write(top30first.to_string())
    textout.write('\n\nTop 30 authors\n')
    textout.write(top30authors.to_string())
    textout.close()
