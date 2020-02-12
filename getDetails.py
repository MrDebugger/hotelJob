from bs4 import BeautifulSoup as bs
from requests import Session
from openpyxl import Workbook
book = Workbook()
mails = Workbook()
sheet = book.active
msheet = mails.active
msheet.append(['Id','Job','Email'])
ses = Session()
total = 0
links = open('links.txt').read().splitlines()
print("Total Links:",len(links))
for link in list(set(links)):
	soup = bs(ses.get(link).text,'lxml')
	id_ = int(link.split('/')[-1].split('-')[0])
	jobName = soup.select("#gianhang > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div:nth-child(1) > div.col-xs-8.col-sm-8.col-md-8.col-lg-8 > h1")[0].text.strip()
	address,recruitor,phone,target = '','','',''
	p = str(soup.find('address').find('p'))
	print(jobName)
	for i in p.split('<i '):
		if 'fa-user-tie' in i:
			recruitor = bs('<i '+i,'lxml').text.strip()
		if 'fa-mobile-alt' in i:
			phone = bs('<i '+i,'lxml').text.strip()
		if 'fa-address-card' in i:
			address = bs('<i '+i,'lxml').text.strip()
		if 'fa-crosshairs' in i:
			target = bs('<i '+i,'lxml').text.strip()
	deadline,salary,quantity,gender,workingHours,field,jobCategory,position = '','','','','','','',''
	for item in soup.findAll('div',class_='job-overview-item'):
		item.find('b').extract()
		if 'fa-calendar' in item.find('i')['class']:
			deadline = item.text.strip()
		if 'fa-money-bill' in str(item):
			salary = item.text.strip()
		if 'fa-users' in item.find('i')['class']:
			quantity = item.text.strip()
		if 'fa-clock' in item.find('i')['class']:
			workingHours = item.text.strip()
		if 'fa-bolt' in item.find('i')['class']:
			field = ', '.join([l.text.strip() for l in item.findAll('a')])
		if 'fa-accusoft' in item.find('i')['class']:
			jobCategory = item.text.strip()
		if 'fa-crown' in item.find('i')['class']:
			position = item.text.strip()
		if 'fa-mars' in item.find('i')['class']:
			gender = item.text.strip()
	website,company,companyPhone,companyAddress = '','','',''
	company = soup.find('div',class_='diachi-nhatuyendung-container').find('h4').text.strip()
	for p in soup.find('div',class_='diachi-nhatuyendung-container').findAll('p'):
		if 'Địa chỉ' in p.span.text.strip():
			p.span.extract()
			companyAddress = p''.text.strip()
			continue
		if 'Điện thoại' in p.span.text.strip():
			p.span.extract()
			companyPhone = p.text.strip()
			continue
		if 'Website' in p.span.text.strip():
			p.span.extract()
			website = p.text.strip()
	sheet.append([id_,jobName,address,phone,recruitor,deadline,salary,quantity,gender,workingHours,field,jobCategory,position,website,company,companyPhone,companyAddress])
	emails = []
	slist = soup.find('ol',{'id':'comment_list'})
	ref = slist['data-ref']
	canEdit = slist['can-edit']
	layout = slist['data-layout-new']
	obj = slist['data-object']
	try:
		emails = [email.text.strip() for email in bs(ses.get(f'https://www.hoteljob.vn/comment/list?page=0&object={obj}&ref={ref}&can_delete={canEdit}&layout_new={layout}').text,'lxml').find('div',id='list-comment').findAll('a',class_='url') if '@' in email.text]
	except:
		pass
	for email in emails:
		msheet.append([id_,jobName,email])
	total+=1
	if total%100==0:
		print("Total:",total)
		book.save('jobs.xlsx')
		mails.save('mails.xlsx')
print("Done")
