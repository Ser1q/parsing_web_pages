### parsing of txt file 

# file_path = './some_file.txt'
# with open(file_path, 'r') as f:
#     content = f.read()
#     names = content.split(',')

# i = 0
# for name in names:
#     names[i] = name.strip()
#     i += 1 

# print(names)

### parsing of csv file

# import csv

# path = './HR_employee_attrition_sample.csv'

# with open(path, 'r') as f:
#     csv_reader = csv.reader(f)
    
#     headers = next(csv_reader) # skipping first row and saving as header
#     print(headers)
    
    
    
#     for row in csv_reader:
#         row[0] = int(row[0]) # first column's data type to int 
        
#         print(row)
    
### parsing of json files 
# import json

# path = './data.json'
# with open(path, 'r') as f:
#     data = f.read()
    
# parsed_data = json.loads(data)

# print(parsed_data['company'])

# employees = parsed_data['employees']
# print(employees[0])
    
### parsing XML files
# XML - eXtensible Markup Language
# import xml.etree.ElementTree as ET

# tree = ET.parse('some_data.xml')
# root = tree.getroot()

# print(root)

# for child in root:
#     print(child.tag, child.attrib)
