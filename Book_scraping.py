import requests
import openpyxl
from bs4 import BeautifulSoup

# Initialize Excel
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'books'
sheet.append(['Title','Category','Rating','Price','Availability'])

# Loop through pages
for page_num in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all book entries on the current page
    books = soup.find_all('h3')

    for book in books:
        book_url = book.find('a')['href']
        book_response = requests.get('https://books.toscrape.com/catalogue/' + book_url)
        book_soup = BeautifulSoup(book_response.content, 'html.parser')

        title = book_soup.find('h1').text
        category = book_soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip() 
        rating = book_soup.find('p', class_='star-rating')['class'][1]
        price = book_soup.find('p', class_='price_color').text
        availability = book_soup.find('p', class_='availability').text.strip()

        # Append the data to the Excel sheet
        sheet.append([title,category,rating,price,availability])

# Save the Excel file after the loop
excel.save('Books1.xlsx')
