# AmazonScraper
Practing more on web scraping by scraping Amazon item pages for their reviews. For this project I scraped the review page for 2 video game items on Amazon 
and took 3 pieces of information from each review. The title, rating out of 5 stars, and the body of the review. 

There are two versions of this program.
They both work pretty much the exact same, the only difference is that in Ver1 it was used for a product with only Canadian reviews
and in Ver2 it was used for a product with both Canadian and international reviews. So Ver1 is useful if you're only concerned about reviews
from Canada, and Ver2 is good if you wanted to look at foreign reviews as well. Small note for Ver2 is that I only looked at the first 4 pages
of the reviews because there were 5000 reviews on this item and I didn't want to go through everything, just wanted to see if this works.

After the info is obtained it's stored into an excel file with columns for the title, rating, and body. In Ver2's excel file the Canadian
and international reviews are on seperate sheets of the same file. Then the number of occurances for each rating out of 5 stars was collected and printed
out (also printed seperately for Canadian/international in Ver2).
