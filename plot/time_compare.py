import matplotlib.pyplot as plt

ns = [6, 7, 8]

qtt_times = [45.168193, 112.6786, 377.187791]
full_times = [7.723154, 100.053465, 1021.394188]

plt.plot(ns, qtt_times, '-o', label="qtt_format")
plt.plot(ns, full_times, '-o', label="full_model")

plt.legend(loc="lower right")

plt.xlabel("n")
plt.xlim([5.5, 8.5])
plt.xticks(ns, ns)

plt.ylabel("time[sec]")
plt.yscale("log")
plt.ylim([5,1300])

plt.annotate('qtt_format', 
            xy=(6, qtt_times[0]), xycoords='data',
            xytext=(-50, 30), 
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->")
            )


plt.annotate('full_model', 
            xy=(6, full_times[0]), xycoords='data',
            xytext=(-50, 30), 
            textcoords='offset points',
            arrowprops=dict(arrowstyle="->")
            )

plt.show()
