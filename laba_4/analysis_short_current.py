import numpy as np
from scipy.fft import fft

class ShortCurrentDetect:
    def __init__(self, cfg_file, dat_file):
        self.cfg_file = str(cfg_file)
        self.dat_file = str(dat_file)
        self.rms_value = None

    def number_of_channels(self, channel_type='total'):
        cfg_file = self.cfg_file
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

    def calculate_rms_value(self, instant_values):
        sampling_rate = 1000
        n = len(instant_values)
        t = np.arange(n) / sampling_rate
        values_fft = fft(instant_values)
        values_fft_mag = np.abs(values_fft)
        rms_value = values_fft_mag * np.sqrt(2) / n
        rms_value = self.rms_value

        return rms_value

    def get_channel_values(self):
        channel_n = self.number_of_channels('analog')
        with open(self.cfg_file, 'r') as cfg_file:
            list_channel = [] #Создание списка для хранения единиц измерений всех каналов измерений
            cfg_file.readline()
            cfg_file.readline()
            for i in range(0, channel_n): #Цикл по добавлению единиц измерения каналов в список
                list_cfg_1 = cfg_file.readline().split(',') #Перевод строки в список элементов по разделителю ","
                list_channel.append(list_cfg_1[4])
        with open(self.dat_file, 'r') as dat_file:
            raw_data = np.loadtxt(dat_file, delimiter=',')

        raw_data_indent = raw_data[:, 2:]
        list_channel_of_currents = [list_channel[index] for index in np.where(np.isin(list_channel, ['kA', 'A', 'A/pu']))[0]]
        list_channel_of_currents_indecies = [i for i, name in enumerate(list_channel) if name in list_channel_of_currents]
        current_channel = raw_data_indent[:, list_channel_of_currents_indecies]

        return current_channel

    def calculate_time(self):
        sample_rate = 20000
        n = int(20 / (1/sample_rate * 1000))
        current_channel = self.get_channel_values()
        time_id = np.zeros(2)
        for row, column in enumerate(current_channel.T):
            column_mean = np.mean(column)
            column = column - column_mean
            ustavka = np.max(np.abs(fft(column[n:(2*n)]))) * np.sqrt(2) * 1.2 / n
            time_id_row = np.array([])
            time_start_end = 0
            for i in range(0, len(column), n):
                one_period = column[i:i+n]
                rms_on_period = np.max(np.abs(fft(one_period))) * np.sqrt(2) / n
                if rms_on_period > ustavka:
                    time_id_row = np.append(time_id_row, i)
            time_start_end = np.array([min(time_id_row), max(time_id_row)])
            time_id = np.vstack((time_id, time_start_end))
        return time_id
