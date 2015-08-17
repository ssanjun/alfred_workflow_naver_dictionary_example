#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow, ICON_WEB, web

SEARCH_URL = 'http://dic.naver.com/search.nhn'

class Word(object) :
    pass

def search(query) :
    from bs4 import BeautifulSoup

    params = dict(query=query)
    r = web.get(SEARCH_URL, params)

    # throw an error if request failed
    # Workflow will catch this and show it to the user
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.select('dl.dic_search_result')

    wordList = []
    wordCount = 0

    if len(result) == 0 :
        wf.send_feedback();
        return
    
    for ele in result[0].children :
        if ele.name == 'dt' :
            w = Word()
            w.title = ' '.join(ele.span.stripped_strings)
            w.url = ele.a['href']
            wordList.append(w)
            wordCount += 1


        if ele.name == 'dd' :
            if not hasattr(wordList[wordCount-1],'desc') :
                wordList[wordCount-1].desc = []

            wordList[wordCount-1].desc.append(' '.join(ele.stripped_strings))
    
    return wordList

def main(wf):
    # The Workflow instance will be passed to the function
    # you call from `Workflow.run`
    # Your imports here if you want to catch import errors
    # or if the modules/packages are in a directory added via `Workflow(libraries=...)`


    # Get args from Workflow, already in normalised Unicode
    args = wf.args
    words = search(args[0])    

    # Add an item to Alfred feedback
    if len(words) > 0 :
        for w in words :
            wf.add_item(title=w.title, subtitle=' '.join(w.desc), icon=ICON_WEB, arg=w.url, valid=True)
        
    # Send output to Alfred
    wf.send_feedback()  
    
if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
