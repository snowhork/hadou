import matplotlib.pyplot as plt

ns = [6, 7, 8]

qtt4_times = [11.078975, 23.266405, 51.722268]
qtt6_times = [12.182592, 31.813745, 77.791213]
full_times = [3.117936, 40.912759, 405.339133]

plt.plot(ns, qtt4_times, '-o', label="QTT-tol:1e-4")
plt.plot(ns, qtt6_times, '-o', label="QTT-tol:1e-6")
plt.plot(ns, full_times, '-o', label="Full")

# qtt4_times = [180, 601, 4499]
# qtt4_deim_times = [364, 420, 798]
# cg4_times = [29, 353, 4486]
# cg8_times = [37, 524, 6270]

# plt.plot(ns, qtt4_times, '-o',      label="QTT-tol:1e-4")
# plt.plot(ns, qtt4_deim_times, '-o', label="QTT-deim-tol:1e-4")
# plt.plot(ns, cg4_times, '-o',       label="CG-tol:1e-4")
# plt.plot(ns, cg8_times, '-o',       label="CG-tol:1e-8")



plt.legend(loc="lower right")

plt.xlabel("n")
plt.xlim([5.5, 8.5])
plt.xticks(ns, ns)

plt.ylabel("time[sec]")
plt.yscale("log")
plt.ylim([1,1000])

# plt.annotate('QTT-tol:1e-4',
#             xy=(6, qtt4_times[0]), xycoords='data',
#             xytext=(-50, 30),
#             textcoords='offset points',
#             arrowprops=dict(arrowstyle="->")
#             )

# plt.annotate('QTT-tol:1e-6',
#             xy=(6, qtt6_times[0]), xycoords='data',
#             xytext=(-50, 80),
#             textcoords='offset points',
#             arrowprops=dict(arrowstyle="->")
#             )

# plt.annotate('Full',
#             xy=(6, full_times[0]), xycoords='data',
#             xytext=(-50, 30),
#             textcoords='offset points',
#             arrowprops=dict(arrowstyle="->")
#             )

plt.show()
