# web_scraper
This is  a job to scrape monster job descriptions that match certain key words, and load them into MongoDB.
Change the parameters.txt file to be whatever job title you want to search (as it will appear in the database, then the title in lowercase with a dash (to be added to the search parameter in Monster), city (lowercase and with hyphens - if needed)

Example:
Software Engineer,software-engineer,new-york</br>
Chef,chef,memphis</br>
</br>
The fields that are scraped from the project are:</br>
Date</br>
Search Term (taken from parmeters.txt)</br>
Title</br>
Company</br>
Location</br>
Description</br>




