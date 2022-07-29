import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewList = []


#need these things to overcome amazon's bot detection
headers = {
    'authority': 'www.amazon.ca',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

def get_soup(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    #try to get reviews from Canada first, if none, then move on
    try:
        for item in reviews:
            review = {
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            #only want the number rating, so replace the 'out of 5 stars' part to blank, then strip the white space
            #then convert the rating to a float so that it's a numeric value
            'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars','').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip()
            }
            reviewList.append(review)

    except:
        pass

for x in range(1,100):
    print(f'Getting page: {x}')
    #send the url to get_soup, we can use the same url and change the page number to x to loop through the pages
    soup = get_soup(f'https://www.amazon.ca/Capcom-91720-Monster-Hunter-World/product-reviews/B072JTV5S2/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    get_reviews(soup)
    #check if it's at the last page/next page button cannot be pressed
    #if it's not the last page then we can just move on
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    #otherwise, we are on the last page so we need to break out of the loop
    else:
        break

#make a dataframe with our reviewList and put it in an excel file
df = pd.DataFrame(reviewList)
writer = pd.ExcelWriter('amazonScraper1.xlsx')
df.to_excel(writer, sheet_name = 'sheet1',index=False)

#for adjusting the width of the excel columns so that all the content can be seen
#loop through the columns
for column in df:
    #find the item with the largest length in the column
    column_width = max(df[column].astype(str).map(len).max(), len(column))
    col_idx = df.columns.get_loc(column)
    #now we can set the width of the column to the size of this largest item
    writer.sheets['sheet1'].set_column(col_idx, col_idx, column_width)

writer.save()

#count the number of occurances of each rating
occurances = df.groupby(['rating'])['rating'].count()

#iterate through the series and print out the results
for rating, num in occurances.items():
    print(f"Rating: {rating}  Occurances: {num}")
