import matplotlib.pyplot as plt
import numpy as np

# Fréquences (Hz)
f = np.array([0, 48, 49.5, 50.5, 52.08, 100])
# Atténuation correspondante (dB)
a = np.array([0, 3, 10, 10, 3, 3])

plt.figure(figsize=(10, 5))
plt.plot(f, a, 'b', linewidth=2, label='Gabarit du filtre')
plt.fill_between(f, a, 20, color='lightblue', alpha=0.4)  # zone hors spécifications

# Limites et style
plt.title("Gabarit du filtre coupe-bande à symétrie géométrique", fontsize=14)
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Atténuation (dB)")
plt.grid(True)
plt.ylim(0, 20)
plt.xlim(0, 100)
plt.axhline(3, color='gray', linestyle='--', label='3 dB')
plt.axhline(10, color='gray', linestyle='--', label='10 dB')
plt.legend()
plt.tight_layout()
plt.show()
