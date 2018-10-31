import numpy as np
import matplotlib.pylab as plt

data = np.memmap("C:/Users/station/Desktop/spaceapps2018_findmark/SDRSharp_20181021_111419Z_446050000Hz_IQ_channel4_1pps_and_signals_200m_shack_to_imdegentrafficlight.wav", offset=44)
data = data[0:50000000]

samples = (data[0::2]**2 + data[1::2]**2)**0.5

N = 10000
s = []
for i in range(0, len(samples), N):
    s.append(np.mean(samples[i:i+N]))


N1 = 3000
print(N1)
samples = np.convolve(samples, np.ones((N1,)) / N1, mode='same')
print(N1)

plt.plot(samples)
plt.show()


plt.plot(s)
plt.grid()
plt.show()


flips = np.zeros(len(s))

criteria = (np.max(s) - np.min(s)) / 2.0

for i in range(len(s)):
    if s[i] >= criteria:
        flips[i] = 1

plt.plot(flips)


# growing the flips and most likely merging them, when only one flip is different

for i in range(len(flips)-1):
    if flips[i] >= 0 and flips[i+1] == 1:
        flips[i] = 1

start = []
stop = []

for i in range(len(flips)-1):
    # rising edge
    if flips[i] >= 1 and i == 0:
        start.append(i)

    if flips[i] == 0 and flips[i+1] == 1:
        start.append(i)

    # falling edge
    if flips[i] >= 1 and i == len(flips)-1:
        stop.append(i)

    if flips[i] == 1 and flips[i + 1] == 0:
        stop.append(i)



pps = []
pps_start = []

signals = []
signals_start = []

print("determination of pulse length in recording")
for i in range(len(stop)):
    if (stop[i] - start[i]) < 40:
        pps.append(1)
        pps_start.append(start[i])
        a = 1
    else:
        signals.append(1.5)
        signals_start.append(start[i])

plt.plot(flips)
plt.plot(s)
plt.plot(pps_start, pps, "*")
plt.plot(signals_start, signals, "o")
plt.grid()
plt.show()


# finding the shorter 1pps
print("finding 1pps")
pps_start_better = []

for i in range(len(pps_start)):
    tmp = np.convolve(samples[pps_start[i]*N - N*4 : pps_start[i]*N + N*10], np.ones((N,)) / N, mode='same')
    plt.plot(tmp)

    j = 0
    while tmp[j] < np.min(tmp) + (np.max(tmp) - np.min(tmp)) * 0.8:
        j += 1
    pps_start_better.append(pps_start[i]*N - N*4 + j)
    print("#", i, "pps start sample location is", pps_start[i]*N - N*4)

plt.show()

for i in range(len(pps_start_better)):
    tmp = np.convolve(samples[pps_start_better[i]: pps_start_better[i] + N * 10], np.ones((N,)) / N, mode='same')
    print("#", i, "pps start sample location is redefined as", pps_start_better[i])
    plt.plot(tmp)

plt.show()


### finding the signals
print("finding signals")
signals_start_better = []

for i in range(len(signals_start)):
    tmp = np.convolve(samples[signals_start[i]*N - N*4 : signals_start[i]*N + N*10], np.ones((N,)) / N, mode='same')
    plt.plot(tmp)

    j = 0
    while tmp[j] < np.min(tmp) + (np.max(tmp) - np.min(tmp)) * 0.8:
        j += 1
    signals_start_better.append(signals_start[i]*N - N*4 + j)
    print("#", i, "signal start sample location is", signals_start[i]*N - N*4)

plt.show()

for i in range(len(signals_start_better)):
    tmp = np.convolve(samples[signals_start_better[i]: signals_start_better[i] + N * 10], np.ones((N,)) / N, mode='same')
    print("#", i, "signal start sample location is redefined as", signals_start_better[i])
    plt.plot(tmp)

plt.show()



# mathmagic is happening here
print("TDOA")
samplingrate = 2048000
speedoflight = 300000000
samplingtime = 1.0 / samplingrate

for signal_start_time in range(len(signals_start_better)):
    time = signals_start_better[signal_start_time]
    #print(signal_start_time, time)

    for pps_start_time in range(len(pps_start_better)-1):
        if time >= pps_start_better[pps_start_time] and time < pps_start_better[pps_start_time + 1]:
            tdoa = (time - pps_start_better[pps_start_time]) * samplingtime
            print(signal_start_time, pps_start_better[pps_start_time], time, time - pps_start_better[pps_start_time], tdoa)