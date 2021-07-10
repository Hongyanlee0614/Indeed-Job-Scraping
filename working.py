import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(url):
    headers = {'User-Agent': 'MY USER AGENT'} # replace with your user agent
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
    for item in divs:
        title = item.find('a').text.strip()
        company = item.find('span', class_='company').text.strip()
        try:
            location = item.find('span', class_='location').text.strip()
        except:
            location = ''
        try:
            salary = item.find('span', class_='salaryText').text.strip()
        except:
            salary = ''
        try:
            remote = item.find('span', class_='remote').text.strip()
        except:
            remote = ''
        summary = item.find('div',{'class':'summary'}).text.strip()
        try:
            link = item.find('a')['href']
        except:
            link = ''
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'remote': remote,
            'summary': summary,
            'link': 'malaysia.indeed.com' + link
        }
        joblist.append(job)
    return

joblist = []
for i in range(0,200,10):
    url = f"https://malaysia.indeed.com/jobs?q=data+analyst+intern&l=Malaysia&start={i}"
    print(f'Getting', {url})
    c = extract(url)
    transform(c)
print(len(joblist))

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('indeed_job.csv')
