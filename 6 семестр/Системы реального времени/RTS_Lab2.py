import math
import time
import matplotlib.pyplot as plt
import Lab1.RTS_Lab1 as Lab1
import numpy as np

w = [1, -1]
N = 1024
x_t = list(range(0, N))


def factor(pk: int, n: int):
    arg = -2*math.pi/n*pk
    return complex(math.cos(arg), math.sin(arg))


def dft(signal: list):
    start = time.time()
    time.sleep(1)
    n = len(signal)
    res = list(map(lambda p: sum(map(lambda k: signal[k] * factor(p * k, n), range(n))), range(n)))
    end = time.time() - start - 1
    return res, end


def fft_step(signal: list, p: int, level_factor):
    n = len(signal)
    new_n = n // 2
    new_p = p % new_n
    if n > 2:
        signal_1 = signal[1::2]
        signal_2 = signal[::2]
        next_level_factor = factor(new_p, new_n)
        f1 = fft_step(signal_1, new_p, next_level_factor)
        f2 = fft_step(signal_2, new_p, next_level_factor)

        return f2 + level_factor*f1
    else:
        return signal[0]*w[0]+signal[1]*w[p % 2]


def fft(signal: list):
    start = time.time()
    time.sleep(1)
    n = len(signal)
    res = list(map(lambda p: fft_step(signal, p, factor(p, n)), range(n)))
    end = time.time() - start - 1
    return res, end


def labs2x():
    # Calculating
    (signal, _, _) = Lab1.generate_rand_signal(N)
    (dft_spectrum, dft_time) = dft(signal)
    (fft_spectrum, fft_time) = fft(signal)

    # Plotting
    plt.figure(1)
    plt.subplot(511)
    plt.title("Signal")
    plt.plot(x_t, signal)

    plt.subplot(513)
    plt.title("DFT Spectrum (Real part)")
    plt.bar(x_t, list(map(lambda c: c.real, dft_spectrum)))

    plt.subplot(515)
    plt.title("DFT Spectrum (Imaginary part)")
    plt.bar(x_t, list(map(lambda c: c.imag, dft_spectrum)))

    plt.savefig("./DFT.png")
    plt.close(1)

    plt.figure(2)
    plt.subplot(511)
    plt.title("Signal")
    plt.plot(x_t, signal)

    plt.subplot(513)
    plt.title("FFT Spectrum (Real part)")
    plt.bar(x_t, list(map(lambda c: c.real, fft_spectrum)))

    plt.subplot(515)
    plt.title("FFT Spectrum (Imaginary part)")
    plt.bar(x_t, list(map(lambda c: c.imag, fft_spectrum)))

    plt.savefig("./FFT.png")
    plt.close(2)

    # Text to write into a file compare.txt
    text = [
        "N = {}\n\n".format(N),
        "-- DFT\n\t"
        "Time: {:.4}\n".format(dft_time),
        "-- FFT\n\t"
        "Time: {:.4}\n".format(fft_time),
    ]

    # Writing into a file
    f = open("./compare.txt", "w")
    for i in text:
        f.write(i)
    f.close()


def additional_task():
    (signal, _, _) = Lab1.generate_rand_signal(N)
    (fft_mine, _) = fft(signal)
    fft_np = np.fft.fft(signal)
    deviation = fft_mine - fft_np

    plt.figure(1)

    plt.subplot(511)
    plt.title("Mine FFT (Abs value)")
    plt.bar(x_t, list(map(lambda c: abs(c), fft_mine)))

    plt.subplot(513)
    plt.title("NumPy FFT (Abs value)")
    plt.bar(x_t, list(map(lambda c: abs(c), fft_np)))

    plt.subplot(515)
    plt.title("Deviation")
    plt.bar(x_t, deviation)

    plt.savefig("./Deviation.png")
    plt.close(1)


if __name__ == '__main__':

    additional_task()
