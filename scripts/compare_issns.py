# Script to compare lists of ISSNS in catalog and from vendor

# Citation: The Librarian's Introduction to Programming Languages : A LITA Guide, edited by Beth Thomsett-Scott, Rowman & Littlefield Publishers, Incorporated, 2016. ProQuest Ebook Central, http://ebookcentral.proquest.com/lib/upenn-ebooks/detail.action?docID=4503922.
# Created from upenn-ebooks on 2023-07-17 16:24:35.
# Detailed walkthrough is available at the above source!

#csv library handles operations in a csv
import csv

#open the catalog csv and read it into a list
with open('issns_from_catalog.cvs', 'r') as f:
    catalog_reader = csv.reader(f, delimiter=',')
    from_catalog = list(catalog_reader) 
    

#do the same with the vendor csv
with open('issns_from_vendor.csv', 'r') as f: 
    vendor_reader = csv.reader(f, delimiter=',') 
    from_vendor = list(vendor_reader) 
    
#create an empty list in preparation for comparison
not_in_both = [] 

#look at the catalog csv and compare it line by line to the vendor csv
#if the issn is not in both, add the issn to the list you made in line 21
#do this over and over until you reach the end of the csv
for issn in from_catalog: 
    if issn not in from_vendor: 
        not_in_both.append(issn) 
    

#convert the list with nonmatched issns into a text file
with open('compared_lists.txt', 'w') as f:
    for issn in not_in_both:
        f.write(issn+'\n')