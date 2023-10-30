from geolite2 import geolite2
import xml.etree.ElementTree as ETREE
import sys

tree = ETREE.parse(sys.argv[1])
top=tree.getroot()  #getting the top of the tree

ipadress=[]
for child in top:
    for nextchild in child:
        q=0
        for nnextchild in nextchild:
            rr=str(nnextchild.get('showname'))
            if rr[:-4] == "Via: Internet.org":    #we will enter the next loop only if there is a showname in this proto with showname "Via: Internet.orgr\r\n"
                q = 1     #q=1 indicates there exists a field with the particular showname "Via: Internet.org\r\n"
        if q == 1:
            for nnextchild in nextchild:
                if nnextchild.get('name') == "http.x_forwarded_for": #for all names which are "http.x_forwarded_for" we are collecting their ip adresses
                    ipadress.append(nnextchild.get('show'))


unique_ips=set(ipadress)  # selecting only non repeated ip adresses
country_name=[] #list to store  country names linked to the ip adresses

for ip in unique_ips:
    var = geolite2.reader()
    country =var.get(ip)['country']['names']['en'] #using geolite2 library to get country name from ip adress
    country_name.append(country)

countries = set(country_name)  #selecting country names by not including repeated names
rows=[]
for country in countries:
    x=country_name.count(country)
    rows.append([country,x]) # creating rows which contain country name and their frequency

import csv

filename = "data.csv"
with open(filename, 'w',newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(rows)  #writing all the rows into the csv file





