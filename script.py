import requests
from bs4 import BeautifulSoup
import csv

data_2 = []
data_3 = []

column_names = ['Treatment', 'Service', 'Code', 'Description', 'Amount', 'Ans Units', 'Assist Units']

msp_req = requests.get('https://www.dr-bill.ca/ohip_billing_codes')
msp_soup = BeautifulSoup(msp_req.text)
resources = []
for item in msp_soup.find_all('div', {'class':'col-md-6'}):
	resources.append('https://www.dr-bill.ca' + item.find('a')['href'])
data_2 = resources[37:50]
data_3 = resources[50:]

category = []
category.append(data_2)
category.append(data_3)

resources = []

for resource_index, resources in enumerate(category):
	data = []
	for url in resources:
		req = requests.get(url)
		soup = BeautifulSoup(req.text)
		table = soup.find_all('div',{'class':'panel-default'})
		treatment = soup.find('h1').find('strong').text

		for item in table:
			service_data = []
			service_type = item.find('div', {'class': 'panel-heading'})
			if service_type is not None:
				for index, row in enumerate(item.find_all('tr')):
					child = 0
					if row.get('class') is not None:
						if row.get('class')[0] == 'child_row':
							child = 1
					value_data = []
					if index == 0:
						continue
					if child == 1:
						value_data.append('')
						value_data.append('')
					else:
						value_data.append(treatment.strip())
						value_data.append(service_type.text.strip())
					for value in row.text.strip().split('\n'):
						if value.strip() != '':
							value_data.append(value.strip())
					data.append(value_data)

	for i in data:
		print(i)
		print('-----------------------------')
	file_name = str(resource_index) + '.csv'
	outfile = open(file_name, 'w')
	outcsv = csv.writer(outfile)
	outcsv.writerow([column for column in column_names])
	[outcsv.writerow([value for value in item]) for item in data]
	outfile.close()
	print('===================================')
	print(len(data))

# # with open('your_file.txt', 'w') as f:
# #     for item in data:
# #         f.write("%s\n" % item[2])