#!/usr/bin/python

"""
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

# Imports

INIT_URL = "https://aulavirtual.frbb.utn.edu.ar/"

# Variables

def run():
    pass

def main():
    run()

if __name__ == "__main__":
    main()
