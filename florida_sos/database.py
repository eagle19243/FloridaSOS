import pymysql


class Database:
    def __init__(self, settings):
        host = settings.get('MYSQL')['host']
        user = settings.get('MYSQL')['user']
        password = settings.get('MYSQL')['password']
        db = settings.get('MYSQL')['db']

        self.con = pymysql.connect(host=host, user=user, password=password,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE DATABASE IF NOT EXISTS %s' % db)
        self.con = pymysql.connect(host=host, user=user, password=password, db=db,
                                   autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS `corps` ('
                         '`id` int(11) NOT NULL auto_increment, '
                         '`corp_name` VARCHAR(50), '
                         '`fei_ein_number` VARCHAR(15), '
                         '`date_filed` VARCHAR(15), '
                         '`status` VARCHAR(50), '
                         '`last_event` VARCHAR(100), '
                         '`principal_addr` VARCHAR(200), '
                         '`mailing_addr` VARCHAR(200), '
                         '`registered_agent_addr` VARCHAR(200), '
                         '`officer_addr` VARCHAR(1000), '
                         '`url` VARCHAR(400), '
                         'PRIMARY KEY (`id`))')

    def remove_data(self):
        self.cur.execute('TRUNCATE TABLE `corps`')
        return

    def get_data(self):
        self.cur.execute('SELECT * FROM `corps`')
        result = self.cur.fetchall()
        return result

    def save_data(self,
                  corp_name,
                  fei_ein_number,
                  date_filed,
                  status,
                  last_event,
                  principal_addr,
                  mailing_addr,
                  registered_agent_addr,
                  officer_addr,
                  url):
        query = """INSERT INTO `corps` (`corp_name`, 
                `fei_ein_number`, 
                `date_filed`, 
                `status`, 
                `last_event`, 
                `principal_addr`, 
                `mailing_addr`, 
                `registered_agent_addr`, 
                `officer_addr`, 
                `url`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                % (corp_name,
                   fei_ein_number, 
                   date_filed, status, 
                   last_event, 
                   principal_addr, 
                   mailing_addr, 
                   registered_agent_addr, 
                   officer_addr, 
                   url)
        self.cur.execute(query)

        return
