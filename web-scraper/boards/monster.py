from bs4 import BeautifulSoup
import sys
from boards.helpers import HttpHelpers
from parsing.models import Jobs
from mongoengine import connect
from mongoengine import NotUniqueError
from datetime import datetime

connect('jobs_db')
# this term is added to the DB as my search term

class MonsterJobs:
    def __init__(self, url, term):
        #use repr to check the url
        self.url = url
        self.term = term
        self.helpers = HttpHelpers()

    def get(self, term):
        page = self.helpers.download_page(self.url)
        if page is None:
            sys.exit('There was a monster downloading the monster jobs webpage. cannot continue further, so fix this first')
        monster_jobs = self.__parse_index(page)

    def __parse_index(self, htmlcontent):
        #downloading the content
        soup = BeautifulSoup(htmlcontent, 'html.parser')
        #Using BeautifulSoup I pulled certain parts of the page that had the info I needed, specifically: job title, description, company, location
        jobs_container = soup.find('div', {'class': 'results-list'})
        try:
            job_items = jobs_container.find('h2', class_='card-title')
        except:
            print('job items is not found')
            return[]
        if job_items is None or len(job_items) == 0:
            print('zero job_items')
            return []
        for job_elem in jobs_container:
            job_info = job_elem.find('div', class_='title-company-location')
        self.cleanData(job_info,soup)

    def cleanData(self, job_info, soup):
            for i in job_info:
            # from the job_elem section you pull out the key words
                title_elem = job_info.find('h2', class_='card-title')
                company_elem=job_info.find('h3', attrs={'name': 'card_companyname'})
                location=job_info.find('span',class_='card-job-location')
                if None in (title_elem, company_elem, location):
                    continue
                #making it all lowercase made it easier to spot duplicates
                t=title_elem.text.strip().lower()
                c =company_elem.text.strip().lower()
                l=location.text.strip().lower()
                #add the date
                date = datetime.now()
                job_description=soup.find('div', attrs={'name': 'sanitizedHtml'})
                descStr= job_description.text.strip().lower()
            self.database(self.term,t,c,l,descStr,date)

    def database(self,term,t,c,l,descStr,date):
                jobs = Jobs(term=term, jobTitle=t, jobCompany=c, jobLocation=l,jobDesc=descStr,date=date)
                try:
                    jobs.save()
                    print('new job')
                except NotUniqueError as e:
                    print('this is a duplicate')
