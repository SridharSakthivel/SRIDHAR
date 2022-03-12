import requests
import os
import subprocess
from tqdm import tqdm
from time import sleep
from os import listdir
from fpdf import FPDF
#SEARCH SECTION
headers={
    'Users-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}
print("Welcome to the project")
print("Please enter your good name:")
User_Name=input()
print()
print("Enter the keyword of the image to search:")
query=input()
capital_query=query.capitalize()
print()
print(f'Dear {User_Name}, Enter the number of images you need to extract')
User_Images_Count=int(input())
print()
if User_Images_Count%2==0:
    pages=User_Images_Count//2
else:
    pages=(User_Images_Count//2)+1
print(f'Your Output PDF will consists of {pages} pages, 2 images per page.')
print()
print('Execution is in progress...')
cur_dir=os.getcwd()
output=cur_dir+ f'/{query}'
if not os.path.exists((output)):
    os.mkdir(output)
api_url=['https://unsplash.com/napi/search/photos?query={}&per_page={}&page=1&xp='.format(query,User_Images_Count)]
for url in tqdm(api_url):
    r=requests.get(url, headers=headers)
    json_data = r.json()
    description=[]
    for image in tqdm(json_data['results']):
        image_title=image['alt_description']
        description.append(image_title)
        image_url=image['urls']['raw']
        try:
            with open(output + '/' + image_title + '.jpg', 'wb') as file:
                r = requests.get(image_url,stream=True)
                file.write(r.content)
        except:
            pass
    sleep(1)
#PDF SECTION
path = cur_dir+ f'/{query}/'
imagelist = listdir(path)
pdf = FPDF('L','mm','A4')
x,y,w,h = 15,30,120,100
a,b,c,d = 160,30,120,100
Counter=0
Description_Count=0
Folder_Image_Count=0
for image in imagelist:
    Counter+=1
    Folder_Image_Count+=1
    if Counter==1:
        pdf.add_page()
        pdf.set_font("Arial", size = 25)
        pdf.cell(270, 10, txt =f'{capital_query}',ln = 1, align = 'C')
        pdf.image(path+image,x,y,w,h)
        pdf.set_font("Arial", size = 20)
        pdf.text(15,150, txt ="Image Description:")
        pdf.text(15,165, txt =f'{description[Description_Count]}')
    if Counter==2:
        pdf.image(path+image,a,b,c,d)
        pdf.text(160, 150, txt ="Image Description:")
        pdf.text(160,165, txt =f'{description[Description_Count]}')
        Counter=0
    Description_Count+=1
if Folder_Image_Count<User_Images_Count:
    print("Unfortunately the system has identified only {} images in unsplash website".format(Folder_Image_Count))
    if Folder_Image_Count%2==0:
        print("Due to this the output PDF file has impacted, and it has {} pages".format(Folder_Image_Count//2))
    else:
        print("Due to this the output PDF file has impacted, and it has {} pages".format((Folder_Image_Count//2)+1))
else:
    print("The Output file is created Successfully!")
pdf.output("images.pdf","F")
