from bs4 import BeautifulSoup
import requests


class Scraper:
    """Customer Scraper class
    """

    def __init__(self, settings):
        self.settings = settings

    def run(self):
        page = requests.get(self.settings['entry_url'])
        soup = BeautifulSoup(page.content, 'html.parser')

        corp_name = self._get_corp_name(soup)
        fei_ein_number = self._get_fei_ein_number(soup)
        date_filed = self._get_date_filed(soup)
        status = self._get_status(soup)
        last_event = self._get_last_event(soup)
        principal_addr = self._get_principal_addr(soup)
        mailing_addr = self._get_mailing_addr(soup)
        registered_agent_addr = self._get_registered_agent_addr(soup)
        officer_addr = self._get_officer_addr(soup)

        print(corp_name)
        print(fei_ein_number)
        print(date_filed)
        print(status)
        print(last_event)
        print(principal_addr)
        print(mailing_addr)
        print(registered_agent_addr)
        print(officer_addr)

    def _get_corp_name(self, soup):
        return soup.select('.detailSection.corporationName p')[1].get_text(strip=True)

    def _get_fei_ein_number(self, soup):
        return soup.find('label', {'for': 'Detail_FeiEinNumber'}) \
            .next_element \
            .next_element \
            .get_text(strip=True)

    def _get_date_filed(self, soup):
        return soup.find('label', {'for': 'Detail_FileDate'}) \
            .next_element \
            .next_element \
            .get_text(strip=True)

    def _get_status(self, soup):
        return soup.find('label', {'for': 'Detail_Status'}) \
            .next_element \
            .next_element \
            .get_text(strip=True)

    def _get_last_event(self, soup):
        return soup.find('label', {'for': 'Detail_LastEvent'}) \
            .next_element \
            .next_element \
            .get_text(strip=True)

    def _get_principal_addr(self, soup):
        el_div = soup.select('.searchResultDetail .detailSection:nth-child(4) span:nth-child(2) div')[0]
        return ' '.join(el_div.get_text().split())

    def _get_mailing_addr(self, soup):
        el_div = soup.select('.searchResultDetail .detailSection:nth-child(5) span:nth-child(2) div')[0]
        return ' '.join(el_div.get_text().split())

    def _get_registered_agent_addr(self, soup):
        agent_name = soup.select('.searchResultDetail .detailSection:nth-child(6) span:nth-child(2)')[0]
        agent_addr = soup.select('.searchResultDetail .detailSection:nth-child(6) span:nth-child(3) div')[0]

        return agent_name.get_text(strip=True) + '\r\n' + ' '.join(agent_addr.get_text().split())

    def _get_officer_addr(self, soup):
        el = soup.select('.searchResultDetail .detailSection:nth-child(7)')[0]

        return ' '.join(el.get_text().split()[5:])
