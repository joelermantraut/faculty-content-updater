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

Another way to select subjects - Going through Personal Area
    - .toggle-display textmenu
        - .icon menu-action
            - .span6
                - .well well-small
                    - .course-info-container
                        - .media
                            - .media-body
                                - .media-heading
                                    - a
            - #pb-for-in-progress
                - ul
                    - li.page-item

"""

from automation_scripts.web_scrapping import WebScrapper
from automation_scripts.auto_gui import AutoGUI
import os.path
import time

# Imports

INIT_URL = "https://aulavirtual.frbb.utn.edu.ar/"

# Variables

class Faculty(object):
    """
    Script to control faculty WEB.
    """
    def __init__(self, chromedriver, INIT_URL, career, subjects):
        self.chromedriver = chromedriver
        self.INIT_URL = INIT_URL
        self.career = career
        self.subjects = subjects
        self.credentials = list()
        self.credentials_file = ".credentials"
        self.download_folder = "/home/joel/Downloads/"
        self.profile = {"plugins.plugins_list": [{"enabled": False,
                                                "name": "Chrome PDF Viewer"}],
                       "download.default_directory": self.download_folder,
                       "download.prompt_for_download": False,
                       "download.extensions_to_open": ""}
        self.pdf_download_button_filename = "images/pdf_download_button.png"
        self.init()

    def init(self):
        """
        Inits objects.
        """
        self.driver = WebScrapper(
            self.chromedriver,
            self.INIT_URL,
            self.profile
        )

        self.autogui = AutoGUI()

        self.get_credentials()
        self.login()
        self.goto_personal_area()
        self.walk_personal_subjects()

    def download_pdf(self, element):
        """
        Gets an element which has a PDF and
        downloads it.
        """
        a = self.driver.get_elements("a", element)
        self.driver.click_elements(a)
        # This opens the PDF
        time.sleep(2)
        # Waits to it to charge
        coords = self.autogui.get_on_screen(self.pdf_download_button_filename)
        self.autogui.mouse_move([coords.x, coords.y])
        self.autogui.click()
        # Clicks on download PDF button
        # self.driver.driver.wait.until(self.driver.driver.expected_conditions.alert_is_present())
        time.sleep(2)
        alert = self.driver.driver.switch_to.alert

        alert.accept()
        # TODO: Manage save prompt

    def solve(self, activity):
        """
        Receives an element and decides what
        to do with it.
        """
        classes = self.driver.get_properties("class", activity)
        if "resource" in classes[0]:
            self.download_pdf(activity)

    def download_all(self):
        """
        Being in correct page, navigates through
        all page downloading content.
        """
        sections = self.driver.get_elements(".topics .section .content .section")
        for section in sections:
            activities = self.driver.get_elements(".activity", section)
            for activity in activities:
                self.solve(activity)

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
                break

    def open_subject(self, subject):
        """
        Opens subject page.
        """
        main_wrapper = self.driver.get_elements(".course_category_tree")
        courses_el = self.driver.get_elements(".courses .coursebox .info .coursename", main_wrapper)
        for element in courses_el:
            text = self.driver.driver.execute_script(
                'return arguments[0].firstChild.textContent;', element
            ).strip()
            if text == subject:
                self.driver.click_elements(element)
                break

    def walk_subjects(self):
        """
        Take an array with subjects from download
        content to drive, and does that.
        """
        for subject in self.subjects:
            self.open_subject(subject)
            # After this, driver will be standing
            # in actual subject page, ready to
            # download all content
            self.download_all()
            # TODO: Correct this

    def goto_personal_area(self):
        """
        Goes to personal area tab.
        """
        user_button = self.driver.get_elements(".toggle-display.textmenu")
        self.driver.click_elements(user_button)
        personal_area_button = self.driver.get_elements(".icon.menu-action")
        self.driver.click_elements(personal_area_button)

    def walk_personal_subjects(self):
        """
        Like walk_subjects, but with personal area page.
        """
        links_list = list()

        subjects = self.driver.get_elements(".course-info-container")
        for subject in subjects:
            subjects_box = self.driver.get_elements("a", subject)
            for subject_box in subjects_box:
                subject_name = self.driver.get_inner_text(subject_box)
                for my_subject in self.subjects:
                    if subject_name == my_subject:
                        links_list.append(*self.driver.get_properties("href", subject_box))

        for link in links_list:
            self.driver.get(link)
            # Opens the page
            self.download_all()

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
    faculty = Faculty(
            chromedriver,
            INIT_URL,
            "Ingeniería Electrónica",
            ["Técnicas Digitales III (Friedrich - Ing. Electrónica - 2021)"]
    )

    time.sleep(2)

def main():
    run()

if __name__ == "__main__":
    main()
