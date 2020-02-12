from bs4 import BeautifulSoup as bs
from requests import Session
ses = Session()
#nghenghiep > div > div.breadcrumbs-custom > div:nth-child(1) > ul > li
total = 0
soup = bs(ses.get('https://hoteljob.vn/').text,'lxml')
for a in soup.select('#nghenghiep > div > div.breadcrumbs-custom')[0].findAll('a'):
	print("Link:",a['href'])
	next = True
	page = 1
	while next:
		soup = bs(ses.get('https://hoteljob.vn'+a['href']+f'/page-{page}').text,'lxml')
		fields = ['https://hoteljob.vn'+link.find('a')['href']+'\n' for link in soup.findAll('p',{'class':'i-title'})] 
		with open('links.txt','a') as file:
			file.writelines(fields)
		total+= len(fields)
		if not soup.find('li',class_='next'):
			next = False
		page+=1
		print("Total:",total)
	print("Done:",a['href'])
	print()
print("Done")
