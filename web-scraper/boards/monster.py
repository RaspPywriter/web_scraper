import pymongo
from bs4 import BeautifulSoup
import sys
from boards.helpers import HttpHelpers
import csv
from parsing.models import Jobs
from mongoengine import connect

connect('jobs_db')

# this term is added to the DB as my search term

#term = 'Business Intelligence Architect'


class MonsterJobs:
    def __init__(self, url, term):
        self.url = url
        self.term = term
        self.helpers = HttpHelpers()

    def get(self, term):
        page = self.helpers.download_page(self.url)
        if page is None:
            sys.exit('There was a monster downloading the monster jobs webpage. cannot continue further, so fix this first')

        monster_jobs = self.__parse_index(page)


        for job in monster_jobs:

            job_content = self.helpers.download_page(job["href"])
            if job_content is None:
                continue

            parsed_details = self.__parse_details(job_content, term)
            job["description_text"] = parsed_details


            job["description"] = parsed_details

        return monster_jobs

    def __parse_index(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')

        jobs_container = soup.find(id='ResultsContainer')

        job_items = jobs_container.find_all('section', class_='card-content')
        if job_items is None or len(job_items) == 0:
            return []
        
        all_jobs = []

        for job_elem in job_items:
            # from the job_elem section you pull out the key words
            title_elem = job_elem.find('h2', class_='title')
            company_elem = job_elem.find('div', class_='company')
            location_elem = job_elem.find('div', class_='location')
            url_elem = job_elem.find('a')
            if None in (title_elem, company_elem, url_elem, location_elem):
                continue


            href = url_elem.get('href')
            if href is None:
                continue

            item = {
                "href" : href,
                "description" : "",
                "description_text" : ""
            }
            all_jobs.append(item)

        return all_jobs


    def __parse_details(self, htmlcontent, term):
        # lxml method of pulling data vs
        global title, company, location
        soup = BeautifulSoup(htmlcontent, 'lxml')
        # scrape the section - I had to use trial and error because I could not find where it was pulling this from
        # so i had to print it and work backwards by scraping the scrape section
        scrape = soup.select('#main-content > div > div > div')

        for job_elem in scrape:
            title = job_elem.find('h1', class_='job_title')
            company = job_elem.find('div', class_='job_company_name')
            location = job_elem.find('div', class_='location c-gray-6')
            if None in (title, company, location):
                continue
            t = title.text.strip()
            c = company.text.strip()
            l = location.text.strip()
            date = datetime.now()

            description_element = soup.select('#main-content > div > div > div > div.container.job-body-container > div > div.job-description.col-md-8.col-sm-12.order-2.order-sm-2.order-md-1 > div')
            # this element is successfully pulling data, but there are characters that cause it to fail
                        for i in description_element:
                # removing characters and joining to a string
                descStr = ''
                for desc in i:

                    descStrip=desc.text.strip()
                    descStr=''.join(descStrip)
                    descStr=descStr.lower()

                    jobs = Jobs(term=term, jobTitle=t, jobCompany=c, jobLocation=l,jobDesc=descStr,date=date)
                    try:
                        jobs.save()
                    except NotUniqueError as e:
                        continue

                return (description_element, str(description_element))
