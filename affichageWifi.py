import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
SLEEP = 5
UNITE = "ko"
TRAFFIC = "both"

def run():
    if TRAFFIC == "both":
        fig, axes = plt.subplots(2, 1, figsize=(8, 6))
        ax_down, ax_up = axes
    elif TRAFFIC == "download":
        fig, ax_down = plt.subplots()
        ax_up = None
    else:
        fig, ax_up = plt.subplots()
        ax_down = None

    def read_file(path):
        if not os.path.exists(path):
            return []
        with open(path) as f:
            lines = f.read().strip().split('\n')
        result = []
        for line in lines:
            if line.strip():
                try:
                    result.append(float(line))
                except ValueError:
                    pass
        return result

    def animate(i):
        if ax_down is not None:
            yarr = read_file("debit_down.txt")
            ax_down.clear()
            ax_down.plot(range(len(yarr)), yarr, 'b-')
            ax_down.set_xlabel(f'Mesure (toutes les {SLEEP}s)')
            ax_down.set_ylabel(f'Débit ({UNITE}/s)')
            ax_down.set_title('Download - Interface 33')
            ax_down.grid(True)

        if ax_up is not None:
            yarr = read_file("debit_up.txt")
            ax_up.clear()
            ax_up.plot(range(len(yarr)), yarr, 'r-')
            ax_up.set_xlabel(f'Mesure (toutes les {SLEEP}s)')
            ax_up.set_ylabel(f'Débit ({UNITE}/s)')
            ax_up.set_title('Upload - Interface 33')
            ax_up.grid(True)

        plt.tight_layout()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()