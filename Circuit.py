from Gates import *
import matplotlib.patches as patches
import matplotlib.pyplot as plt

class Circuit:
    def __init__(self):
        self.gates = []
        self.num_bits = 0
        self.next_x = 0

    def __str__(self):
        return "\n".join([g.__str__() for g in self.gates])

    def add_gate(self, type, control=None, target=0, x=None, face_color='w', edge_color='k'):
        self._update_num_bits(control, target)

        if x is None:
            x = self.next_x
            self.next_x += 1
        elif x >= self.next_x:
            self.next_x = x + 1

        self.gates.append(Gate(type=type, control=control, target=target, x=x, face_color=face_color, edge_color=edge_color))

    def add_correction(self, measurement, correction, x=None, face_color='w', edge_color='k'):
        self._update_num_bits(measurement[0], correction[0])

        if x is None:
            x = self.next_x
            self.next_x += 1
        elif x >= self.next_x:
            self.next_x = x + 1

        self.gates.append(PauliCorrection('', measurement[0], correction[0], measurement[1], correction[1], x, face_color, edge_color))

    def _draw(self, canvas, size, scale):

        x0 = 0
        x1 = len(self.gates) * size
        for bit in range(self.num_bits + 1):
            y = (bit + 0.5) * size
            canvas.add_patch(patches.ConnectionPatch(xyA=(x0, y), xyB=(x1, y), coordsA="data"))

        for gate in self.gates:
            gate.draw(canvas, size, scale)

    def disp(self, size, scale):
        canvas = plt.axes()
        self._draw(canvas, size, scale)

        self._init_plt(canvas)
        plt.show()

    def save(self, size, scale, filename):
        canvas = plt.axes()
        self._draw(canvas, size, scale)

        self._init_plt(canvas)
        plt.savefig(filename)


    def _init_plt(self, canvas):
        canvas.set_axis_off()
        plt.gca().invert_yaxis()
        plt.box("off")
        plt.axis('scaled')

    def _update_num_bits(self, control, target):
        if control is None:
            self.num_bits = max(self.num_bits, target)
        else:
            self.num_bits = max(self.num_bits, control, target)