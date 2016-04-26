"""
shamelessly copied from https://github.com/VitaliyRodnenko/geeknote/blob/master/geeknote/editor.py
"""
import os
import re

import html2text

from bs4 import BeautifulSoup


def enml_to_text(content):
    soup = BeautifulSoup(content.decode('utf-8'), "html.parser")

    for section in soup.select('li > p'):
        section.replace_with(section.contents[0])

    for section in soup.select('li > br'):
        if section.next_sibling:
            next_sibling = section.next_sibling.next_sibling
            if next_sibling:
                if next_sibling.find('li'):
                    section.extract()
            else:
                section.extract()

    for section in soup.findAll('en-todo', checked='true'):
        section.replace_with('[x]')

    for section in soup.findAll('en-todo'):
        section.replace_with('[ ]')

    content = html2text.html2text(str(soup).decode('utf-8'), '', 0)
    content = re.sub(r' *\n', os.linesep, content)

    return content.encode('utf-8')
