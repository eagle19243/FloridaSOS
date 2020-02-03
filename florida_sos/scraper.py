import requests
from bs4 import BeautifulSoup
from datetime import date
from .util import save_data, remove_output_csv
from .database import Database


class Scraper:
    """Customer Scraper class
    """

    def __init__(self, settings):
        self.entry_url = settings.get('SCRAPER')['entry_url']
        self.database = Database(settings)

    def run(self):
        remove_output_csv()
        self._process(self.entry_url)

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
                  officer_addr,
                  url)
        self.database.save_data(corp_name,
                                fei_ein_number,
                                date_filed,
                                status,
                                last_event,
                                principal_addr,
                                mailing_addr,
                                registered_agent_addr,
                                officer_addr,
                                url)
        if url_next_on_list:
            self._process(url_next_on_list)

    def _get_corp_name(self, soup):
        el = soup.select('.detailSection.corporationName p')
        return el[1].get_text(strip=True) if el and len(el) > 1 else ''

    def _get_fei_ein_number(self, soup):
        el = soup.find('label', {'for': 'Detail_FeiEinNumber'})
        return el.next_element.next_element.get_text(strip=True) if el else ''

    def _get_date_filed(self, soup):
        el = soup.find('label', {'for': 'Detail_FileDate'})
        return el.next_element.next_element.get_text(strip=True) if el else ''

    def _get_status(self, soup):
        el = soup.find('label', {'for': 'Detail_Status'})
        return el.next_element.next_element.get_text(strip=True) if el else ''

    def _get_last_event(self, soup):
        el = soup.find('label', {'for': 'Detail_LastEvent'})
        return el.next_element.next_element.get_text(strip=True) \
            if el \
            else ''

    def _get_principal_addr(self, soup):
        el_filing_info = soup.select('.searchResultDetail .detailSection.filingInformation')

        if not el_filing_info or len(el_filing_info) is 0:
            return ''

        el_principal = el_filing_info[0].next_sibling.next_sibling.select('span:nth-child(2) div')
        return ' '.join(el_principal[0].get_text().split()) if el_principal and len(el_principal) > 0 else ''

    def _get_mailing_addr(self, soup):
        el_filing_info = soup.select('.searchResultDetail .detailSection.filingInformation')

        if not el_filing_info or len(el_filing_info) is 0:
            return ''

        el_mailing = el_filing_info[0].next_sibling.next_sibling.next_sibling.next_sibling.select(
            'span:nth-child(2) div')
        return ' '.join(el_mailing[0].get_text().split()) if el_mailing and len(el_mailing) else ''

    def _get_registered_agent_addr(self, soup):
        el_filing_info = soup.select('.searchResultDetail .detailSection.filingInformation')

        if not el_filing_info or len(el_filing_info) is 0:
            return ''

        el_registered = el_filing_info[0].next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
        agent_name = el_registered.select('span:nth-child(2)')
        agent_addr = el_registered.select('span:nth-child(3) div')

        return agent_name[0].get_text(strip=True) + '\r\n' + ' '.join(agent_addr[0].get_text().split()) \
            if agent_name and agent_addr and len(agent_name) > 0 and len(agent_addr) > 0 \
            else ''

    def _get_officer_addr(self, soup):
        el_filing_info = soup.select('.searchResultDetail .detailSection.filingInformation')

        if not el_filing_info or len(el_filing_info) is 0:
            return ''

        el_officer = el_filing_info[
            0].next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling

        if el_officer is None:
            return ''

        tmp_ary = list(filter(('').__ne__, el_officer.get_text().split('\n')))
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
        el = soup.find('a', {'title': 'Next On List'})
        link = None

        if el:
            link = 'http://search.sunbiz.org' + el['href']

        return link

    def _is_corp_contain_llc(self, corp):
        return 'LLC' in corp

    def _is_date_filed_greater_than_5(self, date_filed):
        date_filed_year = int(date_filed.split('/')[2])
        current_year = date.today().year

        return current_year - date_filed_year > 5

    def _is_stauts_inact_ua(self, status):
        return status is 'INACT/UA'

    def _is_last_event_matched(self, last_event):
        return last_event is 'ADMIN DISSOLUTION FOR ANNUAL REPORT'
