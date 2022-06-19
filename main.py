import requests
from bs4 import BeautifulSoup
import re


def get_url_and_parse(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def remove_extra_and_irrelevant(results):
    list_to_stop_repeats = []
    results_manicured = []
    for i in results:
        if i.attrs['data-slug'] not in ['intro', 'newsletter', 'related-links']:  # ignore irrelevant
            if i.attrs['data-slug'] not in list_to_stop_repeats:  # check if name is in list
                list_to_stop_repeats.append(i.attrs['data-slug'])  # add to list if not
    for i in results:
        if i.attrs['data-slug'] in list_to_stop_repeats:  # check if name is in list
            results_manicured.append(i)  # add to new list if it is
            list_to_stop_repeats.remove((i.attrs['data-slug']))  # remove from old list, preventing another append
    return results_manicured


def get_content(html_block):
    try:
        address = html_block.find('div', class_='c-mapstack__address')
        address = address.decode_contents().replace('<br/>', ', ')
    except:
        address = 'n/a'

    try:
        phone = html_block.find('div', class_='c-mapstack__phone desktop-only').text
    except:
        phone = 'n/a'

    try:
        website = ''
        for i in html_block.find_all('a', href=True):
            if 'visit website' in i.text.lower():
                website = i.attrs['href']
    except:
        website = 'n/a'

    content = {'Address': address, 'Phone': phone, 'Website': website}
    return content


def extract_name_and_format(html_block):
    try:
        head_div = html_block.find('div', class_='c-mapstack__card-hed')
        h1_text = head_div.find('h1').text
        #         remove_number_punc = re.sub(r'[\d\s][^\w]', '', h1_text).strip()
        #         return remove_number_punc
        #         return h1_text
        number_removed = h1_text.split('.')
        formatted_name = number_removed[1].strip()
        content = get_content(html_block)
        return formatted_name, content
    except Exception as e:
        print(e)
        # pass


def generate_dict(results_manicured):
    dict_of_restaurants = {}
    for i in range(0, len(results_manicured)):
        try:
            name, content = extract_name_and_format(results_manicured[i])
            dict_of_restaurants[name] = content
        except Exception as e:
            print(e)

    return dict_of_restaurants


def main():
    test_url1 = 'https://seattle.eater.com/maps/best-new-restaurants-seattle-heatmap'
    test_url2 = 'https://seattle.eater.com/maps/pike-place-market-where-to-eat-seattle'
    soup = get_url_and_parse(test_url1)
    results = soup.find_all('section', class_='c-mapstack__card')
    results_manicured = remove_extra_and_irrelevant(results)
    dict_of_restaurants = generate_dict(results_manicured)

    for i in dict_of_restaurants.items():
        print(i)
        print('testing git cmd push')


if __name__ == '__main__':
    main()
