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

To login.
     - #inst12780
      - .content
       - .form-group
        - input

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
import time

# Imports

INIT_URL = "https://aulavirtual.frbb.utn.edu.ar/"

# Variables

class Faculty(object):
    """
    Script to control faculty WEB.
    """
    def __init__(self, chromedriver, INIT_URL, career):
        self.chromedriver = chromedriver
        self.INIT_URL = INIT_URL
        self.career = career
        self.credentials = list()
        self.credentials_file = ".credentials"
        self.init()

    def init(self):
        """
        Inits objects.
        """
        self.driver = WebScrapper(
            self.chromedriver,
            self.INIT_URL
        )

        self.get_credentials()
        self.login()
        self.walk_subjects()

    def select_career(self):
        """
        Selects career from menu.
        """
        main_wrapper = self.driver.get_elements("#inst4991")
        main_list = self.driver.get_elements(".content .no-overflow ul", main_wrapper)
        items = self.driver.get_elements("li a", main_list)
        for item in items:
            text = self.driver.get_inner_text(item)
            if text == self.career:
                self.driver.click_elements(item)

    def walk_subjects(self):
        """
        Take an array with subjects from download
        content to drive, and does that.
        """
        self.select_career()

    def get_credentials(self):
        """
        Opens a file, decrypts it, and gets credentials.
        """
        with open(self.credentials_file, "r") as file:
            content = file.read()

        self.credentials.extend(content.split("\n"))

    def login(self):
        """
        Logs in WEB.
        """
        main_wrapper = self.driver.get_elements("#inst12780")
        content = self.driver.get_elements(".content", main_wrapper)
        inputs = self.driver.get_elements(".form-group input", content)
        for input_index in range(len(inputs) - 1):
            self.driver.send_keys(
                    inputs[input_index],
                    self.credentials[input_index]
                    )

        self.driver.send_keys(inputs[2], "enter")

def run():
    chromedriver = os.path.expanduser("~/Apps/chromedriver")
    faculty = Faculty(chromedriver, INIT_URL, "Ingeniería Electrónica")

def main():
    run()

if __name__ == "__main__":
    main()
