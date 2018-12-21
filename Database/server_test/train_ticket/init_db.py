import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



class InitDB:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
        self.query_sql = 'select * from {}'
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def init_stations(self):
        with open(os.path.join(BASE_DIR, '../get_data/data/stations.txt')) as f:
            all_sets = f.readlines()
        for item in all_sets:
            name = item.split(' ')[0]
            code = item.split(' ')[1].split()[0]
            sql = 'insert into train_ticket_stations(station_name, station_code) values("{}", "{}")'.format(name, code)
            #sql2 = 'delete  from train_ticket_stations'
            print(sql)
            self.cursor.execute(sql)
            self.conn.commit()
        result_set = self.conn.execute(self.query_sql.format('train_ticket_stations'))
        for row in result_set:
            print(row)

    def init_train_number(self):
        with open(os.path.join(BASE_DIR, '../get_data/data/train_info.txt')) as f:
            all_sets = f.readlines()
        #self.cursor.execute('delete from train_ticket_trainnumber')
        for index in range(38046, len(all_sets)):
            item = all_sets[index]
            set_ = item.split(' ')
            train_no = set_[0] + set_[1] + set_[4].replace('-', '')
            train_name = set_[1]
            start_station = set_[2]
            end_station = set_[3]
            date = set_[4]
            sql = 'insert into train_ticket_trainnumber(train_num_id, train_name, start_station, end_station, date) values("{}", "{}", "{}", "{}", {})'.format(train_no, train_name, start_station, end_station, date)
            print(index, sql)
            self.cursor.execute(sql)
            self.conn.commit()
        result_set = self.conn.execute(self.query_sql.format('train_ticket_trainnumber'))
        for row in result_set:
            print(row)

    def query_seat(self):
        sql = """ select train_ticket_trainnumber.train_num_id, train_ticket_carriage.seat_type, count(train_ticket_seat.seat_num)
                            from train_ticket_seat join train_ticket_carriage join train_ticket_trainnumber
                              where train_ticket_seat.belong_to_carriage_id = train_ticket_carriage.id and train_ticket_trainnumber.train_num_id = train_ticket_carriage.belong_to_train_id
                              group by train_ticket_carriage.seat_type"""
        res = self.conn.execute(sql)
        for row in res:
            print(row)

    def update_pass(self):
        sql = 'update train_ticket_passstations set arrival_time=date||substr(arrival_time, 11, 19)'
        res = self.conn.execute(sql)
        for row in res:
            print(row)

if __name__ == '__main__':
    db = InitDB()
    db.update_pass()
    db.close()
