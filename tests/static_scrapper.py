from pandas import DataFrame
import requests
from bs4 import BeautifulSoup

playerUrl = []
page = requests.get('https://coinmarketcap.com/trending-cryptocurrencies/')
soup = BeautifulSoup(page.text, 'html.parser')
# print(soup.get_text())

for link in soup.find_all('a'):
  # print(link.get('href'))
  if link.get('href') and '/currencies/' in link.get('href'):
    playerUrl.append(link.get('href'))
    if len(playerUrl) == 100:
      break

cryptoName = []
picture = []
for url in playerUrl:
  page = requests.get('https://coinmarketcap.com{}'.format(url))

  soup = BeautifulSoup(page.text, 'html.parser')
  coinImgDiv = soup.find('div', {'data-role': 'coin-logo'})
  img = coinImgDiv.find('img').get('src')
  print(f"Image URL: {img}")
  picture.append(img)

  # Find the coin name using data-role attribute
  coinNameSpan = soup.find('span', {'data-role': 'coin-name'})
  h1Name = coinNameSpan.get('title') or coinNameSpan.get_text().replace(' price', '')
  print(f"Coin Name: {h1Name}")
  cryptoName.append(h1Name)


data = {
    'name': cryptoName,
    'image': picture
}
df = DataFrame(data, columns=['name', 'image'])
print(df)