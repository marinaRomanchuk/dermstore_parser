import urllib
import requests
import csv
import re
import warnings
from bs4 import BeautifulSoup as bs
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def get_results(html) -> dict:
    results_dict = {}
    regexp_name = r'^productName'
    regexp_brand = r'^productBrand'
    regexp_price = r'^productPrice'
    regexp_image = r'ProductImage'
    regexp_use = r'How to Use'
    regexp_overview = r'Product Overview'

    results_dict['Product name'] = html.find('h1', {'class': re.compile(regexp_name)}).text

    results_dict['Brand name'] = html.find('img', {'class': re.compile(regexp_brand)}).get('alt')

    results_dict['Price'] = html.find('div', {'class': re.compile(regexp_price)}).find('p', {'class': re.compile('price')}).text.strip()

    results_dict['Main image url'] = html.find('img', {'class': re.compile(regexp_image), 'height': '600px'}).get('src')
    
    html_overview = html.find('div', text=re.compile(regexp_overview)).parent.parent
    results_dict['Product overview block'] = html_overview.find('div', {'class': 'productDescription_synopsisContent'}).text
    
    html_use = html.find('div', text=re.compile(regexp_use)).parent.parent
    results_dict['How to use block'] = html_use.find('div', {'class': 'productDescription_synopsisContent'}).text
    
    return results_dict


def writing_csv(results: dict):
    with open('results.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(results.keys()))
 
        writer.writeheader()
        writer.writerow(results)
 
    print("writing complete")


if __name__ == '__main__':
    warnings.simplefilter("ignore")

    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-u", "--url", default="https://www.dermstore.com/tripollar-desire-toning-device/13525895.html", help="Url of the dermstore")
    args = vars(parser.parse_args())
 
    # Set up parameters
    link = args["url"]
    
    try:
        response = requests.get(link)
    except Exception:
        print("Some problems with connection")
        exit()
    if response is not None:
        html = bs(response.text, 'html.parser')
        
        results_dict = get_results(html)
        writing_csv(results_dict)

