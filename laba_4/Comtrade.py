import matplotlib.pyplot as plt
import comtrade

def plot_comtrade(cfg_file, dat_file):
    cfg_file = str(cfg_file)
    dat_file = str(dat_file)
    rec = comtrade.load("I_U.cfg", "I_U.dat")

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(rec.time, rec.analog[0])
    plt.subplot(3, 1, 2)
    plt.plot(rec.time, rec.analog[1])
    plt.subplot(3, 1, 3)
    plt.plot(rec.time, rec.analog[2])
    plt.legend([rec.analog_channel_ids[0], rec.analog_channel_ids[1], rec.analog_channel_ids[2]])
    plt.show()
