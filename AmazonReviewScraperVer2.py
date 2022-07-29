import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewList = []
reviewListIntl = []


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
    #now try to get international reviews
    try:
        for item in reviews:
                reviewIntl = {
                'title': item.find('span', {'data-hook': 'review-title'}).text.strip(),
                'rating': float(item.find('i', {'data-hook': 'cmps-review-star-rating'}).text.replace('out of 5 stars','').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip()
                }
                reviewListIntl.append(reviewIntl)

    except:
        pass

#just going to go through the first 4 pages because this is just a practice
#could increase the range to a large number like 1000 if we wanted to make sure we went through everything
for x in range(1,5):
    print(f'Getting page: {x}')
    #send the url to get_soup, we can use the same url and change the page number to x to loop through the pages
    soup = get_soup(f'https://www.amazon.ca/Monster-Hunter-Rise-Nintendo-Switch/product-reviews/B08JJ37XVW/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    get_reviews(soup)
    #check if it's at the last page/next page button cannot be pressed
    #if it's not the last page then we can just move on
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    #otherwise, we are on the last page so we need to break out of the loop
    else:
        break

#make dataframes with our two review lists and put it in an excel file
dfCanada = pd.DataFrame(reviewList)
dfIntl = pd.DataFrame(reviewListIntl)
writer = pd.ExcelWriter('amazonScraper2.xlsx')
#save the Canadian reviews in Canadian sheet and international one in International sheet
dfCanada.to_excel(writer, sheet_name = 'Canadian',index=False)
dfIntl.to_excel(writer, sheet_name = 'International',index=False)

#for adjusting the width of the excel columns so that all the content can be seen
#loop through the columns
for column in dfCanada:
    #find the item with the largest length in the column
    column_width = max(dfCanada[column].astype(str).map(len).max(), len(column))
    col_idx = dfCanada.columns.get_loc(column)
    #now we can set the width of the column to the size of this largest item
    writer.sheets['Canadian'].set_column(col_idx, col_idx, column_width)

for column in dfIntl:
    #find the item with the largest length in the column
    column_width = max(dfIntl[column].astype(str).map(len).max(), len(column))
    col_idx = dfIntl.columns.get_loc(column)
    #now we can set the width of the column to the size of this largest item
    writer.sheets['International'].set_column(col_idx, col_idx, column_width)

writer.save()

#count the nuber of occurances of each rating
canadaOcc = dfCanada.groupby(['rating'])['rating'].count()
intlOcc = dfIntl.groupby(['rating'])['rating'].count()

#iterate through the series and print out the results
print("Results for Canadian reviews")
for rating, num in canadaOcc.items():
    print(f"Rating: {rating}  Occurances: {num}")

print("Results for international reviews")
for rating, num in intlOcc.items():
    print(f"Rating: {rating}  Occurances: {num}")