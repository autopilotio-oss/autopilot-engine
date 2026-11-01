"""Original music bed for animated carousel covers: a seamless 8 second loop (90 BPM, 12 beats), synthesized here so
there are no rights issues. Dark minor pad, sub kick, clap, soft hats. Every sound wraps around the loop end, so the
loop point is inaudible.

    python3 tools/carousel/beat.py out.wav [mood]      mood: dark (default) | bright | tense
"""
import sys, wave
import numpy as np

SR, BPM, BEATS = 44100, 90, 12
L = int(SR * BEATS * 60 / BPM)          # exactly 8 s
BEAT = L // BEATS
rng = np.random.default_rng(7)

MOODS = {  # chords as semitones from A2 (110 Hz), 4 beats each
    "dark": [[0, 3, 7, 12], [-4, 0, 3, 8], [-2, 2, 5, 10]],      # Am  Fmaj  G
    "bright": [[0, 4, 7, 11], [5, 9, 12, 16], [7, 11, 14, 17]],  # Amaj7 D G-ish lift
    "tense": [[0, 3, 7, 10], [1, 4, 8, 13], [-2, 3, 7, 10]],     # Am7 Bb Gm7
}


def place(buf, sig, at):
    """Add sig into the circular buffer starting at sample `at` (wraps around)."""
    idx = (np.arange(len(sig)) + at) % L
    np.add.at(buf, idx, sig)


def lowpass(x, cut):
    a = np.exp(-2 * np.pi * cut / SR); y = np.empty_like(x); z = 0.0
    for i, v in enumerate(x):
        z = (1 - a) * v + a * z; y[i] = z
    return y


def pad(notes, n):
    t = np.arange(n) / SR; s = np.zeros(n)
    for semi in notes:
        f = 110 * 2 ** (semi / 12)
        for det in (-0.12, 0.0, 0.12):
            ph = 2 * np.pi * f * (1 + det / 100) * t
            s += np.sign(np.sin(ph)) * 0.18 + np.sin(ph) * 0.5    # soft square + sine
    env = np.minimum(1, t / 0.35) * np.exp(-t * 0.35)
    return lowpass(s * env, 900) * 0.035


def kick():
    n = int(SR * 0.45); t = np.arange(n) / SR
    f = 45 + 75 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5) * 0.9


def clap():
    n = int(SR * 0.25); t = np.arange(n) / SR
    nz = rng.standard_normal(n); nz = nz - lowpass(nz, 1200)
    env = sum(np.exp(-np.maximum(t - d, 0) * 60) * (t >= d) for d in (0, 0.011, 0.022)) / 3 + np.exp(-t * 18) * 0.5
    return nz * env * 0.28


def hat(v):
    n = int(SR * 0.06); t = np.arange(n) / SR
    nz = rng.standard_normal(n); nz = nz - lowpass(nz, 6000)
    return nz * np.exp(-t * 90) * v


def make(mood="dark"):
    m = np.zeros(L)
    for k, ch in enumerate(MOODS[mood]):
        place(m, pad(ch, BEAT * 5), k * BEAT * 4)                 # 1 beat overlap into the next chord
        place(m, pad([ch[0] - 12], BEAT * 4) * 1.6, k * BEAT * 4)  # bass
    for b in range(BEATS):
        if b % 2 == 0:
            place(m, kick(), b * BEAT)
        if b % 4 == 2:
            place(m, clap(), b * BEAT)
        place(m, hat(0.05), b * BEAT + BEAT // 2)                 # offbeat 8ths
        place(m, hat(0.025), b * BEAT)
    place(m, kick() * 0.6, 11 * BEAT + BEAT // 2)                 # pickup into the loop
    m = np.tanh(m * 1.1) / np.tanh(1.1)
    m *= 0.85 / np.max(np.abs(m))
    st = np.stack([m, np.roll(m, 90)], 1)                         # tiny stereo width
    return st


if __name__ == "__main__":
    out = sys.argv[1]; mood = sys.argv[2] if len(sys.argv) > 2 else "dark"
    st = make(mood)
    w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
    print("beat", out, mood, f"{L / SR:.2f}s")
