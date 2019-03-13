import requests
from bs4 import BeautifulSoup
import re

def scrape(n, save_func):
  # Initializing class
  escortfish = EscortFish(save_func=save_func)
  n_pages = int(n / escortfish.POSTS_PER_PAGE)
  n_excess = n % escortfish.POSTS_PER_PAGE
  if n_excess is not 0:
    n_pages += 1
  n_done = 0  # counter
  for page_number in range(1, n_pages + 1):
    if (n_excess is not 0) and (page_number == n_pages):
      link_limit = n_excess
    else:
      link_limit = escortfish.POSTS_PER_PAGE
    escortfish.get_ad_links(page_number=page_number, link_limit=link_limit)


class EscortFish():
  POSTS_PER_PAGE = 40

  def __init__(self, save_func):
    self.save_func = save_func

  def get_ad_links(self, page_number, link_limit):
    link_items = []
    get = 'https://escortfish.ch/manhattan/'
    get_this = str(get) + str(page_number) + '/'
    page = requests.get(str(get_this))
    soup = BeautifulSoup(page.content, 'html.parser')
    count = 0  # Counter
    for link in soup.find_all('a', href=True):
      if link['href'].split('/')[-1].isdigit():
        link_items.append(link['href'])
        self.get_ad_data(link['href'])
        count += 1
      if count == link_limit:
        break

  def get_ad_data(self, url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')

    link = soup.find_all('a',class_='tel-num', href=True)[0]
    a = (link['href'])
    phone = a.split(':')[-1]

    spans = soup.find_all('span', {'class' : 'location-text'})
    for span in spans:
      from geopy.geocoders import Nominatim
      geolocator = Nominatim(user_agent="APP")
      location = (span.get_text())
      try:
        loc = geolocator.geocode(location)
        latitude = loc.latitude
        longitude = loc.longitude
      except Exception:
        latitude = None
        longitude = None

    age = self.find_by_label(soup, "Age:").strip()

    a = (soup.select('.post-details > .description > p'))
    ad = []
    for item in a:
      ad.append(item.get_text())
    ad_text = (' '.join(ad))

    for i in soup.findAll('time'):
      if i.has_attr('datetime'):
        time = (i['datetime']).split(' ')[-1]
        date = (i['datetime']).split(' ')[-2]
    for i in soup.findAll('img'):
      image = i['src'] 
    # return phone, location, age, ad_text, time, date
    ad_data = {
      'phone': phone,
      'location':location,
      'age':age,
      'ad_text':ad_text,
      'time':time,
      'date':date,
      'image':image,
      'latitude':latitude,
      'longitude':longitude
    }
    self.save_func(ad_data)

  def find_by_label(self, soup, label):
    return soup.find("span", text=re.compile(label)).next_sibling