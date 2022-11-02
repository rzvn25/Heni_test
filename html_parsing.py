from lxml import html
import re
import pandas as pd
from datetime import datetime

# get html and tree
html_page_link = 'candidateEvalData/webpage.html'

with open(html_page_link, encoding="utf8") as f:
    html_string = f.read()

html_text = html.fromstring(html_string)

# parse artist name
artist_name_content = html_text.xpath('//h1[@class="lotName"]/text()')
artist_name = re.sub("\([\S\s]+\)", "", artist_name_content[0] if artist_name_content else '').strip()

# parse painting name
painting_name = html_text.xpath("//h2[@class='itemName']/i/text()")[0].strip()

# parse price GBP
price_GBP = html_text.xpath("//span[contains(@id,'PriceRealizedPrimary')]/text()")[0].strip()

# parse price US
price_US = html_text.xpath("//div[contains(@id,'PriceRealizedSecondary')]/text()")[0].strip()

# parse price GBP est
GBP_est = html_text.xpath("//span[contains(@id,'PriceEstimatedPrimary')]//text()")[0].strip()

# parse price US est
US_est = html_text.xpath("//span[contains(@id,'PriceEstimatedSecondary')]//text()")[0].strip()

# image link
image_link = html_text.xpath("//img[@id='imgLotImage']/@src")[0]

# sale date
sale_date = html_text.xpath("//span[contains(@id,'SaleDate')]/text()")[0].strip()

data = [[artist_name, painting_name, price_GBP, price_US, GBP_est, US_est, image_link, sale_date]]

df = pd.DataFrame(data,  columns=['artist_name', 'painting_name', 'price_GBP', 'price_US', 'GBP_est', 'US_est', 'image_link', 'sale_date'])
print(df)
