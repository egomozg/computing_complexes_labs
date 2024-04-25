import matplotlib.pyplot as plt
import threading

# Function to plot data in a separate thread
def plot_data(x, y):
    plt.plot(x, y)
    plt.savefig('/home/egorsuse/Documents/smb_share/test.png')

# Sample data
x1 = [1, 2, 3, 4, 5]
y1 = [10, 20, 25, 30, 35]
x2 = [1, 2, 3, 4, 5]
y2 = [5, 10, 15, 20, 25]

# Create and start threads for each plot
thread1 = threading.Thread(target=plot_data, args=(x1, y1))
thread2 = threading.Thread(target=plot_data, args=(x2, y2))
thread1.start()
thread2.start()
