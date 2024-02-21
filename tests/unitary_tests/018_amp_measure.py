import matplotlib.pyplot as plt
import numpy as np

def get_amp(s, t, freq, ts=None):
    ts = ts or t[1]-t[0]
    n_per = int(t[-1]*freq)
    n_iper = int(1/(freq*ts))

    I_max = np.zeros(n_per, dtype=int)
    I_min = np.zeros(n_per, dtype=int)
    for i in range(n_per):
        i_min, i_max = i*n_iper, (i+1)*n_iper
        I_max[i] = np.argmax(s[i_min: i_max]) + i_min
        I_min[i] = np.argmin(s[i_min: i_max]) + i_min

    amps = s[I_max] - s[I_min]
    return np.mean(amps)

# sampling rate
sr = 2e6
# sampling interval
ts = 1.0/sr
t = np.arange(0,10e-3,ts)
freq1 = 1000
x = 3*np.sin(2*np.pi*freq1*t)

freq = 4000
x += np.sin(2*np.pi*freq*t)

freq = 7000
x += 0.5* np.sin(2*np.pi*freq*t)



x_noised = x + 0.2*(np.random.rand(len(x))-0.5)
freq = 10
#x_noised = x * (1-0.2* np.sin(2*np.pi*freq*t))

print(get_amp(x, t, freq1, ts))
print(get_amp(x_noised, t, freq1, ts))

plt.figure(figsize = (8, 6))
plt.plot(t, x_noised, 'r')
plt.plot(t, x, 'g')
plt.ylabel('Amplitude')



from scipy.fftpack import fft, ifft

X0 = fft(x)
X = fft(x_noised)


N = len(X)
n = np.arange(N)
T = N/sr
freq = n/T
print(N, freq, freq1)
I = np.isclose(freq, freq1, atol=300)
print(I, X0[I])
Xfilt = X
Xfilt[~I] *= 0
amp_0 = np.trapz(np.abs(X0[I])/N)
amp = np.trapz(np.abs(X[I])/N)
print(amp_0, amp)

plt.figure(figsize = (12, 6))
plt.subplot(121)

plt.stem(freq, np.abs(X)/N, 'b', \
         markerfmt=" ", basefmt="-b")
plt.xlabel('Freq (Hz)')
plt.ylabel('FFT Amplitude |X(freq)|')
plt.xlim(0, 1e4)

plt.subplot(122)
plt.plot(t, ifft(X).real, 'r')
plt.plot(t, ifft(Xfilt).real, 'r')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
