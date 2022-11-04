#! /usr/bin/env python
"""Test Script for CPSC 419 Pset 3"""

import difflib
from time import sleep
from multiprocessing import Process
import subprocess
import unittest
from urllib.request import urlopen
from urllib.parse import urlencode

from bs4 import BeautifulSoup as BS4, Tag, NavigableString

def main():

    server = Process(target=start_server)
    server.start()
    # Let the server come online
    sleep(1)

    unittest.main(exit=False)

    kill_server()

def start_server():
    subprocess.run(["sh startserver.h"], shell=True)

def kill_server():
    pid = subprocess.run(["lsof", "-t", "-i:8000"], capture_output=True, text=True).stdout.splitlines()
    subprocess.run(["kill", *pid])
    # print("Killed server.")

class TestSubmission(unittest.TestCase):

    def _ST_ASSERT(self, st_msg: str, pts, assertmethod, *args, **kwargs):
        with self.subTest(st_msg):
            assertmethod(*args, **kwargs)
            self.score += pts

    def _is_text_input(self, item: Tag) -> bool:
        return type(item is Tag) and item.name == "input" and item["type"] == "text"

    def _endpoint_from_form(self, form: Tag) -> dict:
        endpoint = { "action": form["action"], "params": {} }
        inputs = form.find_all("input")
        inputnames = [i["name"] for i in inputs if "name" in i.attrs]
        approximations = {"department":"depar", "subject":"subj", "num":"num", "title":"tit"}
        for key, approx in approximations.items():
            closest_input = difflib.get_close_matches(approx, inputnames, n=1, cutoff=0.1)

            self._ST_ASSERT(
                f"The form contains a field with a value something like {key}", 1,
                self.assertTrue, 
                closest_input, 
                msg=f"No apparent input field for '{key}' out of {inputnames}.")

            endpoint["params"][key] = closest_input[0]
        return endpoint

    def _is_details_link(self, item: Tag) -> bool:
        return "href" in item.attrs and item["href"].startswith("details?crn=")

    def _is_info_table(self, tag):
        if tag.name != "table":
            return False
        reqd_headers = ["Department Name", "Subject Code", "Course Number"]
        th_tags = tag.find_all("th")
        for req, th in zip(reqd_headers, th_tags):
            if req != th.string:
                return False
        return True

    def _is_sections_table(self, tag):
        if tag.name != "table":
            return False
        reqd_headers = ["Section Number", "CRN", "Meetings"]
        th_tags = tag.find_all("th")
        for req, th in zip(reqd_headers, th_tags):
            if req != th.string:
                return False
        return True

    def _is_crosslistings_table(self, tag):
        if tag.name != "table":
            return False
        reqd_headers = ["Subject Code", "Course Number"]
        th_tags = tag.find_all("th")
        for req, th in zip(reqd_headers, th_tags):
            if req != th.string:
                return False
        return True

    def _is_profs_table(self, tag):
        if tag.name != "table":
            return False
        reqd_headers = ["Professors"]
        th_tags = tag.find_all("th")
        for req, th in zip(reqd_headers, th_tags):
            if req != th.string:
                return False
        return True

    def _is_return_link(self, tag):
        if tag.name != "a":
            return False
        possible_hrefs = ["search", "/"]
        return difflib.get_close_matches(tag["href"], possible_hrefs)

    def setUp(self) -> None:
        self.score = 0
        self.base_page = None
        with urlopen("http://localhost:8000") as resp:
            self.base_page = resp.read().decode("utf-8")
        return super().setUp()

    def tearDown(self) -> None:
        print(f"**** Score for this test case is {self.score} ****")
        return super().tearDown()

    def test_root(self):
        page = self.base_page

        self.assertIsNotNone(page, msg="Root page exists")
        self.score += 5

        soup = BS4(page, 'html.parser')
        form: Tag = soup.find("form")

        self._ST_ASSERT(
            "There is a form on the page", 2,
            self.assertIsNotNone,
            form
        )

        form.select("input[type='submit']")
        inputfield_count = 0
        reqd_labels = {"Department", "Course Number", "Subject", "Title"}
        actual_labels: set[str] = set()
        for desc in form.descendants:
            if self._is_text_input(desc):
                inputfield_count += 1
            elif type(desc) is NavigableString:
                actual_labels.add(str(desc))
        for req in reqd_labels:
            label_is_present = bool(difflib.get_close_matches(req, actual_labels, n=1))
            
            self._ST_ASSERT(
                f"Label like '{req}' is present", 1,
                self.assertTrue, label_is_present)
        
        self._ST_ASSERT(
            "There is no results table in an empty search", 2,
            self.assertFalse,
            soup.select(":not(form) > table"))

    def test_empty_search(self):
        base_page = self.base_page
        
        soup = BS4(base_page, 'html.parser')
        form: Tag = soup.find("form")
        endpt_dict = self._endpoint_from_form(form)

        self._ST_ASSERT(
            "Form action is 'search'", 1,
            self.assertEqual,
            endpt_dict["action"],
            "search"
        )

        paramdict = {value : "" for value in endpt_dict["params"].values()}
        params = urlencode(paramdict)
        endpt_url = f"http://localhost:8000/{endpt_dict['action']}?{params}"
        results_page = None
        with urlopen(endpt_url) as resp:
            results_page = resp.read().decode("utf-8")
        
        self._ST_ASSERT(
            "Results page exists", 5,
            self.assertIsNotNone, results_page
        )

        soup = BS4(results_page, 'html.parser')
        results_table = soup.select(":not(form) > table")

        self._ST_ASSERT(
            "There is exactly one table of results", 2,
            self.assertEqual,
            len(results_table),
            1
        )

        table_rows = results_table[0].find_all("tr")
        
        nrows = 3061
        self._ST_ASSERT(
            f"The table contains all {nrows-1} courses (this number is valid as of 2022-10-27)", 2,
            self.assertEqual,
            len(table_rows),
            nrows
        )

        td_first = table_rows[1].find_all("td")

        self._ST_ASSERT(
            "The results table contains 5 columns", 1,
            self.assertEqual,
            len(td_first), 5
        )

        column_vals = {td.string for td in td_first}

        self._ST_ASSERT(
            "First row contains the appropriate course information (order ignored)", 3,
            self.assertSetEqual,
            column_vals,
            {
                '12841',
                'Aerospace Studies (USAF)',
                'USAF',
                '101',
                'Heritage and Values of the U.S. Air Force I'
            })

        crn_link = td_first[0].find("a")

        self._ST_ASSERT(
            "First column is a link to details page", 2,
            self.assertTrue, self._is_details_link(crn_link)
        )

    def test_search_d_cpsc_n_419(self):
        base_page = self.base_page
        
        soup = BS4(base_page, 'html.parser')
        form: Tag = soup.find("form")
        endpt_dict = self._endpoint_from_form(form)

        self._ST_ASSERT(
            "Form action is 'search'", 1,
            self.assertEqual,
            endpt_dict["action"],
            "search"
        )

        paramdict = {value : "" for value in endpt_dict["params"].values()}
        paramdict[endpt_dict["params"]["department"]] = "cpsc"
        paramdict[endpt_dict["params"]["num"]] = "419"
        params = urlencode(paramdict)
        endpt_url = f"http://localhost:8000/{endpt_dict['action']}?{params}"

        results_page = None
        with urlopen(endpt_url) as resp:
            results_page = resp.read().decode("utf-8")
        
        self._ST_ASSERT("Results page exists", 5, self.assertIsNotNone, results_page)

        soup = BS4(results_page, 'html.parser')
        results_table = soup.select(":not(form) > table")

        self._ST_ASSERT(
            "There is exactly one table of results", 2,
            self.assertEqual,
            len(results_table),
            1
        )

        table_rows = results_table[0].find_all("tr")
        
        nrows = 2
        self._ST_ASSERT(
            f"The table contains all {nrows-1} courses (this number is valid as of 2022-10-27)", 2,
            self.assertEqual,
            len(table_rows),
            nrows
        )

        td_first = table_rows[1].find_all("td")

        self._ST_ASSERT(
            "The results table contains 5 columns", 1,
            self.assertEqual,
            len(td_first), 5
        )

        column_vals = {td.string for td in td_first}

        self._ST_ASSERT(
            "First row contains the appropriate course information (order ignored)", 3,
            self.assertSetEqual,
            column_vals,
            {
                '13382',
                'Computer Science (CPSC)',
                'CPSC',
                '419',
                'Full Stack Web Programming'
            })

        crn_link = td_first[0].find("a")

        self._ST_ASSERT(
            "First column is a link to details page", 2,
            self.assertTrue, self._is_details_link(crn_link)
        )

    def test_details_12841(self):
        details_page = None
        with urlopen("http://localhost:8000/details?crn=12841") as resp:
            details_page = resp.read().decode("utf-8")
        
        self.assertIsNotNone(details_page, msg="Details page for crn 12841 exists")
        self.score += 5

        soup = BS4(details_page, 'html.parser')

        info_table = soup.find(self._is_info_table)

        self._ST_ASSERT(
            "Page contains a table with basic course info", 2,
            self.assertIsNotNone, info_table
        )

        if info_table:
            tds = info_table.find_all("td")
            values = ["Aerospace Studies (USAF)", "USAF", "101"]
            self._ST_ASSERT(
                "Info table has the correct values", 3,
                self.assertListEqual, values,
                list(map(lambda t: t.string, tds))
            )

        title_string = soup.find(string="Heritage and Values of the U.S. Air Force I")

        self._ST_ASSERT(
            "Page contains correct title string somewhere", 5,
            self.assertIsNotNone, title_string
        )

        descrip_a = soup.find("p",
            string="Introduction to the U.S. Air Force and how it works as a military institution, including an overview of its basic characteristics, missions, and organizations.")
        descrip_b = soup.find("p", 
            string=" Students attend one 50-minute lecture and one 110-minute laboratory each week.")
        
        self._ST_ASSERT(
            "Page contains the correct description string somewhere, formatted as HTML", 1,
            self.assertIsNotNone, descrip_a and descrip_b
        )
        self._ST_ASSERT(
            "The two pieces of the description string are appropriately colocated", 4,
            self.assertTrue,
            descrip_a.find_next_sibling() == descrip_b
        )

        prereq = soup.find(
            "p", 
            attrs={"class": "prerequisites"},
            string="For enrollment credit only; cannot be applied toward the 36-course-credit requirement for the Yale bachelor's degree. Grades earned in this course do not count toward GPA or eligibility for General Honors."
        )

        self._ST_ASSERT(
            "Page contains correct prerequisite string and it is properly formatted as HTML", 5,
            self.assertIsNotNone, prereq
        )

        section_table = soup.find(self._is_sections_table)

        self._ST_ASSERT(
            "Page contains a sections table with appropriate column headers", 1,
            self.assertIsNotNone, section_table
        )

        if section_table:
            tds = section_table.find_all("td")
            values = ["1", "12841", "T 7.30-8.20 @ WALL53 208"]
            self._ST_ASSERT(
                "Sections table has the correct values", 4,
                self.assertListEqual, values,
                list(map(lambda t: t.string.strip(), tds))
            )

        cross_table = soup.find(self._is_crosslistings_table)

        self._ST_ASSERT(
            "Page contains crosslisting table", 1,
            self.assertIsNotNone, cross_table
        )

        if cross_table:
            tds = cross_table.find_all("td")
            values = ["USAF", "101"]
            self._ST_ASSERT(
                "Crosslistings table has the correct values", 4,
                self.assertListEqual, values,
                list(map(lambda t: t.string, tds))
            )

        profs_table = soup.find(self._is_profs_table)

        self._ST_ASSERT(
            "Page contains professors table", 1,
            self.assertIsNotNone, profs_table
        )

        if profs_table:
            tds = profs_table.find_all("td")
            values = ["Greg Jeong"]
            self._ST_ASSERT(
                "Professors table has the correct values", 4,
                self.assertListEqual, values,
                list(map(lambda t: t.string, tds))
            )

        return_link = soup.find(self._is_return_link)
        self._ST_ASSERT(
            "Page contains a link to search page", 2,
            self.assertIsNotNone, return_link
        )

        self._ST_ASSERT(
            "Page contains a footer", 1,
            self.assertIsNotNone,
            soup.find("footer")
        )

    def test_details_12710(self):
        details_page = None
        with urlopen("http://localhost:8000/details?crn=12710") as resp:
            details_page = resp.read().decode("utf-8")
        
        self.assertIsNotNone(details_page, msg="Details page for crn 12710 exists")
        self.score += 5

        soup = BS4(details_page, 'html.parser')

        info_table = soup.find(self._is_info_table)

        self._ST_ASSERT(
            "Page contains a table with basic course info", 1,
            self.assertIsNotNone, info_table
        )

        if info_table:
            tds = info_table.find_all("td")
            values = ["Chemistry (CHEM)", "CHEM", "600"]
            self._ST_ASSERT(
                "Info table has the correct values", 4,
                self.assertListEqual, values,
                list(map(lambda t: t.string, tds))
            )

        title_string = soup.find(string="Research Seminar")

        self._ST_ASSERT(
            "Page contains correct title string somewhere", 5,
            self.assertIsNotNone, title_string
        )

        descrip = soup.find("p",
            string="Presentation of a student’s research results to the student’s adviser and fellow research group members. Extensive discussion and literature review are normally a part of the series.")
        
        self._ST_ASSERT(
            "Page contains the correct description string somewhere", 5,
            self.assertIsNotNone, descrip
        )

        prereq = soup.find(
            string="None"
        )

        self._ST_ASSERT(
            "Page contains correct prerequisite string", 5,
            self.assertIsNotNone, prereq
        )

        section_table = soup.find(self._is_sections_table)

        self._ST_ASSERT(
            "Page contains a sections table with appropriate column headers", 1,
            self.assertIsNotNone, section_table
        )

        if section_table:
            trs = section_table.find_all("tr")
            self._ST_ASSERT(
                "Sections table has 51 rows (including header row)", 1,
                self.assertEqual, len(trs), 51
            )

            tds = section_table.find_all("td")

            values = {
                '1', '12710', 'HTBA @ TBA', 
                '2', '12713', 'HTBA @ TBA', 
                '3', '12716', 'HTBA @ TBA', 
                '4', '12719', 'HTBA @ TBA', 
                '5', '12722', 'HTBA @ TBA', 
                '6', '12724', 'HTBA @ TBA', 
                '7', '12730', 'HTBA @ TBA', 
                '8', '12732', 'HTBA @ TBA', 
                '9', '12734', 'HTBA @ TBA', 
                '10', '12735', 'HTBA @ TBA', 
                '11', '12738', 'HTBA @ TBA', 
                '12', '12740', 'HTBA @ TBA', 
                '13', '12741', 'HTBA @ TBA', 
                '14', '12743', 'HTBA @ TBA', 
                '15', '12745', 'HTBA @ TBA', 
                '16', '12746', 'HTBA @ TBA', 
                '17', '12747', 'HTBA @ TBA', 
                '18', '12748', 'HTBA @ TBA', 
                '19', '12749', 'HTBA @ TBA', 
                '20', '12750', 'HTBA @ TBA', 
                '21', '12751', 'HTBA @ TBA', 
                '22', '12752', 'HTBA @ TBA', 
                '23', '12753', 'HTBA @ TBA', 
                '24', '12754', 'HTBA @ TBA', 
                '25', '12755', 'HTBA @ TBA', 
                '26', '12756', 'HTBA @ TBA', 
                '27', '12757', 'HTBA @ TBA', 
                '28', '12758', 'HTBA @ TBA', 
                '29', '12759', 'HTBA @ TBA', 
                '30', '12760', 'HTBA @ TBA', 
                '31', '12761', 'HTBA @ TBA', 
                '32', '12762', 'HTBA @ TBA', 
                '33', '12763', 'HTBA @ TBA', 
                '34', '12764', 'HTBA @ TBA', 
                '35', '12765', 'HTBA @ TBA', 
                '36', '12766', 'HTBA @ TBA', 
                '37', '12767', 'HTBA @ TBA', 
                '38', '12768', 'HTBA @ TBA', 
                '39', '12770', 'HTBA @ TBA', 
                '40', '12772', 'HTBA @ TBA', 
                '41', '12773', 'HTBA @ TBA', 
                '42', '12774', 'HTBA @ TBA', 
                '43', '12775', 'HTBA @ TBA', 
                '44', '12776', 'HTBA @ TBA', 
                '45', '12777', 'HTBA @ TBA', 
                '46', '12778', 'HTBA @ TBA', 
                '47', '12779', 'HTBA @ TBA', 
                '48', '12780', 'HTBA @ TBA', 
                '49', '12781', 'HTBA @ TBA', 
                '50', '12782', 'HTBA @ TBA'
            }

            td_strings = {td.string for td in tds}

            self._ST_ASSERT(
                "Sections table has the correct values", 3,
                self.assertSetEqual, values, td_strings
            )

        cross_table = soup.find(self._is_crosslistings_table)

        self._ST_ASSERT(
            "Page contains crosslisting table", 1,
            self.assertIsNotNone, cross_table
        )

        if cross_table:
            tds = cross_table.find_all("td")
            values = {"CHEM", "600"}
            self._ST_ASSERT(
                "Crosslistings table has the correct values", 4,
                self.assertSetEqual, values,
                {td.string for td in tds}
            )

        profs_table = soup.find(self._is_profs_table)

        self._ST_ASSERT(
            "Page contains professors table", 1,
            self.assertIsNotNone, profs_table
        )

        if profs_table:
            tds = profs_table.find_all("td")
            values = {
                "Andrew Miranker",
                "Anna Marie Pyle",
                "Anton Bennett",
                "Benjamin Turk",
                "Caitlin Davis",
                "Corey O'Hern",
                "Craig Crews",
                "Daniel DiMaio",
                "David Spiegel",
                "E. Chui-Ying Yan",
                "Gary Brudvig",
                "Hailiang Wang",
                "J Patrick Loria",
                "James Mayer",
                "Jason Crawford",
                "Jing Yan",
                "Joe Howard",
                "Jon Ellman",
                "Judy Cha",
                "Julien Berro",
                "Krystal Pollitt",
                "Kurt Zilm",
                "Lisa Pfefferle",
                "Mark Hochstrasser",
                "Mark Johnson",
                "Matthew Simon",
                "Nilay Hazari",
                "Patrick Holland",
                "Patrick Vaccaro",
                "Paul Anastas",
                "Sarah Slavoff",
                "Scott Miller",
                "Scott Strobel",
                "Seth Herzon",
                "Sharon Hammes-Schiffer",
                "Stacy Malaker",
                "Stavroula Hatzios",
                "Stephen Strittmatter",
                "Thomas Pollard",
                "Tianyu Zhu",
                "Timothy Newhouse",
                "Victor Batista",
                "W. Mark Saltzman",
                "William Jorgensen"
            }

            self._ST_ASSERT(
                "Professors table has the correct values", 4,
                self.assertSetEqual, values,
                {td.string for td in tds}
            )

        return_link = soup.find(self._is_return_link)

        self._ST_ASSERT(
            "Page contains a link to search page", 2,
            self.assertIsNotNone, return_link
        )

        footer = soup.find("footer")
        self._ST_ASSERT(
            "Page contains a footer", 1,
            self.assertIsNotNone, footer
        )

if __name__ == "__main__":
    main()