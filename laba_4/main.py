import sys
import fill_DB
import Comtrade
import numpy as np
from analysis_short_current import ShortCurrentDetect
#from test123 import Parser

db_filler = fill_DB.FillDb('mydb', 'postgres', '123', '5432', 'localhost')
db_filler.create_table(sys.argv[1])
db_filler.insert_data_in_table(sys.argv[1], sys.argv[2])
raw_data = ShortCurrentDetect(sys.argv[1], sys.argv[2])
current_channel = raw_data.get_channel_values()
time = raw_data.calculate_time()
#Comtrade.plot_comtrade(sys.argv[1], sys.argv[2])
print(time)
time_start = db_filler.get_time(np.min(time[1]))
time_end = db_filler.get_time(np.max(time[1]))
print("Время начала короткого замыкания", time_start, "мс")
print("Время конца короткого замыкания", time_end, "мс")
#a = Parser()
#print(a.data_load_in_table(sys.argv[1], sys.argv[2]))
