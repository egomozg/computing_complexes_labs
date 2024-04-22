import psycopg2

class FillDb:
    def __init__(self, dbname, user, password, port, host):
        self.dbname=dbname
        self.user=user
        self.password=password
        self.port=port
        self.host=host
        self.conn = None
        self.cur = None
        self.channel_n = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    port=self.port,
                    host=self.host
            )
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print("Ошибка при подключении к БД PostgreSQL", e)


    def create_table(self, name_CfgFile):
        # Подключаемся к PostgreSQL БД
        self.connect()
        try:
            self.cur.execute("DROP TABLE IF EXISTS measurements;")
            self.channel_n = self.number_of_channels(name_CfgFile)
            print("Количество каналов измерений: " + str(self.channel_n))
            cfg_file = str(name_CfgFile)
            with open(cfg_file, 'r') as cfg:
                cfg.readline()
                cfg.readline()
                request_formation = "CREATE TABLE IF NOT EXISTS measurements (id BIGINT PRIMARY KEY, time BIGINT," #Создание строки, содержащей начало запроса
                for i in range(self.channel_n): #Цикл для формирования полного запроса на создание таблицы
                    list_i = cfg.readline().split(',') #Запись элементов строки в список, с разделителением по ','
                    if i == self.channel_n - 1:
                        request_formation += " " + '"' + str(list_i[1]).lstrip() + '"' + " REAL"
                    else:
                        request_formation += " " + '"' + str(list_i[1]).lstrip() + '"' + " REAL,"

            request_formation += ")" 
            self.cur.execute(request_formation)
            self.conn.commit()
            print("Таблица успешно создана")
        except psycopg2.Error as e:
            print("Ошибка при создании таблицы:", e)

        finally:
            if self.conn:
                self.cur.close()
                self.conn.close()

    def insert_data_in_table(self, name_cfg_file, name_dat_file):
        self.connect()
        try:
            request_formation_cfg = '"id", "time"' #Создание начала строки названия столбцов
            name_cfg_file = str(name_cfg_file)
            with open(name_cfg_file, 'r') as cfg:
                cfg.readline()
                cfg.readline()
                for i in range(self.channel_n): #Цикл по добавлению в строку названия столбцов таблицы
                    list_i = cfg.readline().split(',') #Запись элементов строки в список, с разделителением по ','
                    request_formation_cfg += ", " + '"' + str(list_i[1]).lstrip() + '"' #Добавление в строку название нового столбца
                list_index = request_formation_cfg.split(',') #Создание списка, элементами которого являются названия столбцов
            placeholders = ', '.join(['%s'] * len(list_index))
            query = f"INSERT INTO measurements ({request_formation_cfg}) VALUES ({placeholders})"

            name_dat_file = str(name_dat_file)
            with open(name_dat_file, 'r') as dat:
                lines = dat.readlines()

            values = []
            for line in lines:
                values.append(tuple(line.strip().split(',')))

            self.cur.executemany(query, values)
            self.conn.commit()
            print("Данные успешно загрузились")

        except psycopg2.Error as e:
            print("Ошибка при добавлении данных в таблицу: ", e)

        finally:
            if self.conn:
                self.cur.close()
                self.conn.close()

    def number_of_channels(self, cfg_file, channel_type='total'):
        cfg_file = str(cfg_file)
        with open(cfg_file, 'r') as cfg:
            cfg.readline()
            cfg_list = cfg.readline().split(',')
            if channel_type == 'total':
                channel_n = str(cfg_list[0])
                channel_n = channel_n.replace(' ', '')
                channel_n = int(channel_n)

            elif channel_type == 'analog':
                channel_n = str(cfg_list[1])
                channel_n = channel_n.replace(' ', '')
                channel_n = int(channel_n[0])

            elif channel_type == 'discrete':
                channel_n = str(cfg_list[2])
                channel_n = channel_n.replace(' ', '')
                channel_n = int(channel_n[0])
        return channel_n

    def get_time(self, time):
        self.connect()
        try:
            self.cur.execute(f'SELECT time FROM measurements WHERE id = {time}')
            needed_value = self.cur.fetchone()
            self.conn.commit()
        except psycopg2.Error as e:
            print("Ошибка при извлечении времени", e)
            needed_value = None
        finally:
            self.cur.close()
            self.conn.close()
        return needed_value

            
