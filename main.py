#!/usr/bin/python

"""
Author: Joel Ermantraut
File: main.py
Desc: Main file of project.

This script opens a faculty WEB, and downloads
any new content on it. Depending on content, it
saves it in different ways.

WEB used: https://www.frbb.utn.edu.ar/
"""

"""
WEB STRUCTURE

After login.

To select career:
    - #inst4991
     - .content
      - .no-overflow
       - ul
        - li (one for each career)
         - a
          - Inside it, career name
          - In href attribute, url

To select cathedra
     - .course_category_tree clearfix
      - .content
       - .courses category-browse category-browse-6
        - .coursebox clearfix odd first collapsed (one for each cathedra)
         - .info
          - .coursename
           - a
            - Inside, cathedra name
            - In href, url

Inside each cathedra
     - .section get each section
      - aria-label attribute the title (could be empty)
      - .content
       - h3.sectionname
        - span
       - ul.section
        - li.activity
         - If it is a:
             - Forum: .forum
             - PDF: .resource
             - To deliver: .assign
             - Zoom: .zoom

"""

from automation_scripts.web_scrapping import WebScrapper
import os.path

# Imports

INIT_URL = "https://aulavirtual.frbb.utn.edu.ar/"

# Variables

class Faculty(object):
    """
    Script to control faculty WEB.
    """
    def __init__(self, chromedriver):
        self.chromedriver = chromedriver

    def init(self):
        """
        Inits objects.
        """
        self.driver = WebScrapper(
            self.chromedriver,
            "https://web.whatsapp.com"
        )

def run():
    chromedriver = os.path.expanduser("~/Apps/chromedriver")
    faculty = Faculty(chromedriver)

def main():
    run()

if __name__ == "__main__":
    main()
