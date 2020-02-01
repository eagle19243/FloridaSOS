from bs4 import BeautifulSoup
import requests
from datetime import date
from .util import save_data


class Scraper:
    """Customer Scraper class
    """

    def __init__(self, settings):
        self.settings = settings

    def run(self):
        self._process(self.settings['entry_url'])

    def _process(self, url):
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        url_next_on_list = self._get_url_next_on_list(soup)
        corp_name = self._get_corp_name(soup)
        fei_ein_number = self._get_fei_ein_number(soup)
        date_filed = self._get_date_filed(soup)
        status = self._get_status(soup)
        last_event = self._get_last_event(soup)
        principal_addr = self._get_principal_addr(soup)
        mailing_addr = self._get_mailing_addr(soup)
        registered_agent_addr = self._get_registered_agent_addr(soup)
        officer_addr = self._get_officer_addr(soup)

        # if self._is_corp_contain_llc(corp_name) and \
        #         self._is_date_filed_greater_than_5(date_filed) and \
        #         self._is_stauts_inact_ua(status) and \
        #         self._is_last_event_matched(last_event):
        save_data(corp_name,
                  fei_ein_number,
                  date_filed,
                  status,
                  last_event,
                  principal_addr,
                  mailing_addr,
                  registered_agent_addr,
                  officer_addr)
        if url_next_on_list:
            self._process(url_next_on_list)

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
        tmp_ary = list(filter(('').__ne__, el.get_text().split('\n')))
        tmp_ary = list(filter(('\r').__ne__, tmp_ary))
        tmp_ary = tmp_ary[2:]
        final_ary = []

        for idx, val in enumerate(tmp_ary):
            val = val.replace('\xa0', ' ')
            val = val.replace('\r', '')
            final_ary.append(val.strip())

            if idx % 4 == 0 or idx % 4 == 3:
                final_ary.append('\r\n\r\n')
            else:
                final_ary.append('\r\n')

        return ''.join(final_ary)

    def _get_url_next_on_list(self, soup):
        el_link = soup.find('a', {'title': 'Next On List'})
        link = None

        if el_link:
            link = 'http://search.sunbiz.org' + el_link['href']

        return link

    def _is_corp_contain_llc(self, corp):
        return 'LLC' in corp

    def _is_date_filed_greater_than_5(self, date_filed):
        date_filed_year = date_filed.split('/')[2]
        current_year = date.today().year

        return current_year - date_filed_year > 5

    def _is_stauts_inact_ua(self, status):
        return status is 'INACT/UA'

    def _is_last_event_matched(self, last_event):
        return last_event is 'ADMIN DISSOLUTION FOR ANNUAL REPORT'
