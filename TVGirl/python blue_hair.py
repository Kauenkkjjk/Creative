import os
import re
import sys
import time

BASE = (0, 150, 255)
BRILHO = (200, 235, 255)
INICIO_EM = 120.7
FPS = 60
CAUDA = 6


def cor(c):
    return f"\033[38;2;{c[0]};{c[1]};{c[2]}m"


def misturar(a, b, k):
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def carregar(caminho):
    linhas = []
    with open(caminho, encoding="utf-8") as f:
        for l in f:
            m = re.match(r"\[(\d+):(\d+(?:\.\d+)?)\](.*)", l.strip())
            if m and m.group(3).strip():
                linhas.append((int(m.group(1)) * 60 + float(m.group(2)), m.group(3).strip()))
    return sorted(linhas)


def quadro(texto, n):
    saida = ""
    for i, c in enumerate(texto[:n]):
        k = max(0.0, 1 - (n - 1 - i) / CAUDA)
        saida += cor(misturar(BASE, BRILHO, k)) + c
    if n < len(texto):
        saida += cor(BRILHO) + "\u258c"
    return "\r" + saida + "\033[0m"


def suave(p):
    return p * p * (3 - 2 * p)


def tocar(linhas):
    os.system("")
    sys.stdout.reconfigure(encoding="utf-8")
    inicio = time.perf_counter() - INICIO_EM
    for i, (t, texto) in enumerate(linhas):
        if t < INICIO_EM:
            continue
        while time.perf_counter() - inicio < t:
            time.sleep(0.002)
        fim = linhas[i + 1][0] if i + 1 < len(linhas) else t + 3
        dur = min(max(fim - t, 0.5), 5) * 0.85
        while True:
            p = (time.perf_counter() - inicio - t) / dur
            if p >= 1:
                break
            n = int(suave(max(p, 0)) * len(texto))
            sys.stdout.write(quadro(texto, n))
            sys.stdout.flush()
            time.sleep(1 / FPS)
        sys.stdout.write(quadro(texto, len(texto)) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "blue_hair.lrc"
    tocar(carregar(arquivo))