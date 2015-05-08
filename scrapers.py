from bs4 import BeautifulSoup
import urllib2

def scrape_a1(url):
    soup = url_to_soup(url)
    if not soup:
        return False

    # Fields to scrape:
    # -----------------
    # Contributed By    Name in format (Last, First Middle
    #   Occupation:     (optional) Job in format 'Occupation: <Job>'
    #   Employer:       (optional) Employer in format 'Employer: <Employer>'
    # Address
    # Amount:           $#,###.##
    #   Date            m/d/yyyy
    # Report Type       ##
    #   Received by     Hyperlinked text with link to Committee page
    # Description
    # Vendor Name
    # Vendor Address

    committee_name = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblName'}).text
    data_table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_tblA1List'})
    for tr in data_table.findAll('tr')[1:]:
        contributor = tr.find('td', {'class': 'tdA1ListContributor'}).text
        contributor_address = tr.find('td', {'class': 'tdA1ListAddress'}).text

        # Amounts
        amount_field = tr.find('td', {'headers': 'ctl00_ContentPlaceHolder1_thA1Amount'})
        date = amount_field.br.next_sibling
        amount = amount_field.text[0:len(amount_field.text)-len(date)]

        received_field = tr.find('td', {'headers': 'ctl00_ContentPlaceHolder1_thRecievedBy'})
        received_text = received_field.text
        received_by = received_field.br.next_sibling
        receipt_type = received_text[0:2]

        data = {'contributor': contributor,
                'contributor_address': contributor_address,
                'date': date,
                'amount': amount,
                'received_by': received_by.text,
                'receipt_type': receipt_type,
        }

        return data

def url_to_soup(url):
    """ Takes an url and returns a BS4 object of the page at that url. Assumes a valid url """
    try:
        response = urllib2.urlopen(url)
    except:
        return False
    html = response.read()
    return BeautifulSoup(html)


a1_url = 'http://www.elections.il.gov/CampaignDisclosure/A1List.aspx?ID=577607&FiledDocID=577607&ContributionType=All%20Types&Archived=False'

print scrape_a1(a1_url)