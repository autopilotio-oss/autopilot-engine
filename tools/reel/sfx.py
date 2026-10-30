"""Small synth used by mix.py for the reel music bed and transition sounds (no external files)."""
import numpy as np
SR = 44100
L = R = None
def init(dur):
    global L, R, N
    N = int(SR * dur); L = np.zeros(N); R = np.zeros(N)
def add(sig, t, g=1.0, pan=0.0):
    i = int(max(t, 0) * SR); n = min(len(sig), N - i)
    if n <= 0: return
    L[i:i + n] += sig[:n] * g * (1 - max(pan, 0)); R[i:i + n] += sig[:n] * g * (1 + min(pan, 0))
def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def kick():
    n = int(.35 * SR); t = np.arange(n) / SR; f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .12)
def clap():
    n = int(.2 * SR); return np.random.randn(n) * env(n, .001, .05)
def hat():
    n = int(.06 * SR); x = np.random.randn(n); x = np.diff(np.concatenate([[0], x])); return x * env(n, .001, .015)
def note(f, dur, kind='pad'):
    n = int(dur * SR); t = np.arange(n) / SR
    if kind == 'bass': return (np.sin(2 * np.pi * f * t) + .3 * np.sin(4 * np.pi * f * t)) * env(n, .01, dur * .6)
    x = sum(np.sin(2 * np.pi * f * (1 + d) * t) for d in (-.004, 0, .004)) / 3
    a = np.minimum(1, t / .3) * np.minimum(1, (dur - t) / .4).clip(0); return x * a
def whoosh(d=.5):
    n = int(d * SR); x = np.random.randn(n); k = np.linspace(0, 1, n) ** 2
    x = np.convolve(x, np.ones(30) / 30, 'same'); return x * k * 0.6
def click():
    n = int(.03 * SR); return np.sin(2 * np.pi * 2000 * np.arange(n) / SR) * env(n, .0005, .006)
def chime(f=1568):
    n = int(1.2 * SR); t = np.arange(n) / SR; return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.01 * t)) * env(n, .002, .35)
def pop(f=1200):
    n = int(.12 * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * f * (1 - t * 3) * t) * env(n, .001, .04)
