import pandas as pd, time, os, re, requests

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from tools.utils import get_rootdir

if __name__ == '__main__':
    rootdir = get_rootdir()
    start_time = time.time()
    # using requests module is not possible due to limited data available, and 
    # we need some action in their website to get more data
    # res = requests.get('https://pergikuliner.com/restaurants?default_search=Surabaya',
    #              headers={
    #                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #                  "Cookie": "_session_id=94f9143fce5a8ed76a54246eff45d8c4; default_search=Surabaya; AWSELB=01E129991AF70BA2C1982EA35EEC711555FED64E41C5532D4B466708BC3D75AF29E5DCEDF0647548A4AF06EF170F439B516815629560E1DC9638A049FD456EB67A596BC231; AWSELBCORS=01E129991AF70BA2C1982EA35EEC711555FED64E41C5532D4B466708BC3D75AF29E5DCEDF0647548A4AF06EF170F439B516815629560E1DC9638A049FD456EB67A596BC231",
    #                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    #              })
    
    options = webdriver.ChromeOptions()
    options.add_argument("auto-open-devtools-for-tabs")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    driver.get('https://pergikuliner.com/restaurants?default_search=Surabaya')

    try:
        total_available_str = getattr(driver.find_element(By.ID, 'top-total-search-view').find_element(By.TAG_NAME, 'strong'), 'text', None)
        regex = re.search(r'\d*\s[\w]+', total_available_str)
        total_available_str = total_available_str[regex.end():].strip()
        total_available = int(total_available_str)
    except Exception as error:
        with open(os.path.join(rootdir, 'log/log.txt'), 'a') as fl:
            fl.writelines(f"{datetime.strftime(datetime.now(), format='%D %H:%M:%S')}: [ERROR] {error}\n")
    
        print(f"{datetime.strftime(datetime.now(), format='%D %H:%M:%S')}: [ERROR] - {error}\n")
        total_available = 100 # desired target of restaurants fetched

    time.sleep(10)
    result = {
        'Restaurant Name':[],
        'Category':[],
        'Rating':[],
        'Price':[],
        'Address':[],
        'Restaurant Detail Link':[],
    }
    no_fetched = 0 # number of restaurant fetched
    idx_previous = 0 # idx for tracking which restaurant have been fetched

    while no_fetched < total_available:
        target_container = driver.find_element(By.ID, 'restaurant_contents').get_attribute('outerHTML')
        soup = BeautifulSoup(target_container, 'html.parser')
        list_elements = soup.find_all('div', class_=['restaurant-result-wrapper best-rating'])
        print(f'LENGTH OF LIST: {len(list_elements)}')

        list_elements = list_elements[idx_previous:]
        print(f'PREVIOUS INDEX: {idx_previous}')
        print(f'LIST TO BE LOOP: {len(list_elements)}')
        for target_element in list_elements:
            print(idx_previous)
            resto_name = getattr(target_element.find('h3', class_=['item-name']).a, 'text', None)
            category = getattr(target_element.find('div', class_=['item-group']).find_next('div'), 'text', None)
            item_info = target_element.find('div', class_=['item-info']).find_all('p', class_=['clearfix'])
            address = getattr(item_info[0].find_all('span', class_='truncate')[1], 'text', None)
            price = getattr(item_info[1].find('span', class_='left'), 'text', None)
            rating = getattr(target_element.find('div', class_=['item-rating-result', 'best-rating']), 'text', None)
            detail_link = target_element.find('h3', class_=['item-name']).find('a').get('href', None)

            try:
                resto_name = resto_name.strip()
                category = category.strip()
                address = address.strip()
                price = price.strip()
                rating = rating.strip()
                detail_link = detail_link.strip()
            except Exception as error:
                print(f'Failed to strip whitespace {error}')
                
            
            no_fetched += 1
            
            result['Restaurant Name'].append(resto_name)
            result['Category'].append(category)
            result['Price'].append(price)
            result['Rating'].append(rating)
            result['Address'].append(address)
            result['Restaurant Detail Link'].append(detail_link)
            
            print(f'{no_fetched} / {total_available}')
            print(f'\t{resto_name} ({rating}) {price}')
            print(f'\t{category} at {address}')
            print(f'\t{detail_link}')
        
        idx_previous = no_fetched

        # load more data and simulate real user clicking the button
        try:
            driver.execute_script("document.querySelector('#next').click()")
        except:
            break
        
        time.sleep(5)

    print(f'Scraping finished in {time.time()-start_time}s')
    print(f'TOTAL SUMMARY: \n\tFETCHED: {no_fetched} RESTAURANTS')
    print('\nSaving data locally in excel...')
    try:
        pd.DataFrame(result).to_excel(os.path.join(rootdir, 'data/scraping_result.xlsx'))
        print('\tData saved in local (excel) successfully...')
    except:
        print('Data failed to saved in excel.')
        print('\nSaving data locally in csv...')
        pd.DataFrame(result).to_csv(os.path.join(rootdir, 'data/scraping_result.csv'))
        
        print('\tData saved in local (csv) successfully...')