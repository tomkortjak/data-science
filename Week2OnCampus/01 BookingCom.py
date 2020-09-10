import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

citiesUrls = []
with open('bookingCom.txt') as webSet:
    for url in webSet:
        citiesUrls.append(url.replace('\n', ''))

scrapedAccommodations = []
accommodationsDF = pd.DataFrame()
for url in citiesUrls:
    # Check if page gives a response back
    getPage = requests.get(url)  # 1
    statusCode = getPage.status_code  # 2

    if (statusCode == 200):  # 3
        soup = BeautifulSoup(getPage.text, 'html.parser')  # 1

        for item in soup.findAll('div', class_="sr__card"):  # 2
            hotelName = item.find('span', class_="bui-card__title").text  # 3
            totalReviewsText = item.find('div', class_="bui-review-score__text").text  # 4
            average_score = item.find('div', class_="bui-review-score__badge").get_text(strip=True)
            city = item.find('p', class_="bui-card__subtitle").find('span').get_text(strip=True)
            price = item.find('div', class_="sr__card_price").find('span').text

            hotelName = hotelName.replace('\n', '')
            totalReviews = totalReviewsText.split(' ', 1)[0]  # 5
            city = city.split(', ')[-1]
            price = price.split('£')[1]
            city = city.replace('Hotel in ', '')
            totalReviews = totalReviews.replace(',', '')
            scrapedAccommodations.append([hotelName, city, int(totalReviews), float(average_score), int(price)])  # 6

            accommodationsDF = pd.DataFrame(scrapedAccommodations,
                                            columns=['hotel_name', 'city', 'total_reviews', 'average_score', 'price'])
        print("Total Accommodations Scraped: ", len(scrapedAccommodations))
    else:
        print("Page doesn't respond")

# Saving data to database
engine = create_engine('mysql://admin:adminadmin123@localhost:3306/gekke_database')

accommodationsDF.to_sql(name='accommodations', con=engine, if_exists='fail', index=False)

# Retrieve data
accommodationsDF = pd.read_sql("SELECT price, average_score FROM accommodations WHERE city = 'Amsterdam'", con=engine)

print(accommodationsDF.head())

accommodationsDF.plot(kind="scatter", x='price', y='average_score', ylim=(0, 10), xlim=(0, 150))
