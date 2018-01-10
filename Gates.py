import matplotlib.lines as lines
import matplotlib.patches as patches
from PIL import ImageFont

LINE_WIDTH = 2
CONTROL_SCALE = 0.2

class Gate:
    def __init__(self, type, control, target, x, face_color, edge_color):
        self.type = type.upper()
        self.control = control
        self.target = target
        self.x = x
        self.face_color = face_color
        self.edge_color = edge_color

    def __str__(self):
        if self.control is not None:
            return "{}({},{})".format(self.type, self.control, self.target)

        else:
            return "{}({})".format(self.type, self.target)

    def draw(self, canvas, size, scale):
        if self.control is not None:
            self._draw_control(canvas, size, scale)
        self._draw_target(canvas, size, scale)

    def _draw_control(self, canvas, size, scale):
        x = self._get_central_axis(self.x, size)
        control_y = self._get_central_axis(self.control, size)
        target_y = self._get_central_axis(self.target, size)
        radius = size * CONTROL_SCALE * .5

        canvas.add_line(lines.Line2D(xdata=(x, x), ydata=(control_y, target_y), color=self.edge_color, linewidth=LINE_WIDTH))
        canvas.add_patch(patches.Circle(xy=(x, control_y), radius=radius, fc=self.edge_color, ec=self.edge_color))

    def _draw_target(self, canvas, size, scale):
        if self.type == 'NOT' or self.type == 'CNOT':
            self._draw_not(canvas, self.x, self.target, size, scale)
        else:
            self._draw_square_target(canvas, self.x, self.target, size, scale, self.type)

    def _draw_not(self, canvas, x, y, size, scale):
        x = self._get_central_axis(x, size)
        y = self._get_central_axis(y, size)
        radius = size * scale * 0.5
        canvas.add_patch(patches.Circle(xy=(x, y), radius=radius, fc=self.face_color, ec=self.edge_color, linewidth=LINE_WIDTH))
        canvas.add_line(lines.Line2D(xdata=[x - radius, x + radius], ydata=[y, y], color=self.edge_color, linewidth=LINE_WIDTH)) # 横線
        canvas.add_line(lines.Line2D(xdata=[x, x], ydata=[y - radius, y + radius], color=self.edge_color, linewidth=LINE_WIDTH)) # 縦線

    def _draw_square_target(self, canvas, x, y, size, scale, s):
        x = self._get_central_axis(x, size)
        y = self._get_central_axis(y, size)
        length = size * scale
        x0 = x - length * 0.5
        y0 = y - length * 0.5
        canvas.add_patch(patches.Rectangle(xy=(x0, y0), width=length, height=length, facecolor=self.face_color, edgecolor=self.edge_color, fill=True, linewidth=LINE_WIDTH))
        self._write_type(canvas, x, y, size, scale, s)

    def _write_type(self, canvas, x, y, size, scale, s):
        canvas.text(x=x, y=y, s=s, style='italic', family='serif', ha='center', va='center', weight='bold', color=self.edge_color)

    def _get_central_axis(self, value, size):
        return (value + 0.5) * size

class PauliCorrection(Gate):
    def __init__(self, type, control, target, measure_basis, correction_basis, x, face_color, edge_color):
        super().__init__('PC', control, target, x, face_color, edge_color)
        self.measure_basis = measure_basis
        self.correction_basis = correction_basis

    def draw(self, canvas, size, scale):
        self._draw_vertical_lines(canvas, size, scale)
        self._draw_measurement(canvas, size, scale)
        self._draw_square_target(canvas, self.x, self.target, size, scale, self.correction_basis)

    def _draw_vertical_lines(self, canvas, size, scale):
        x = self._get_central_axis(self.x, size)
        width = size * CONTROL_SCALE / 2
        x0 = x - width * .5
        y0 = self._get_central_axis(self.control, size)
        y1 = self._get_central_axis(self.target, size)
        canvas.add_patch(
            patches.Rectangle(xy=(x0, y0), width=width, height=y1 - y0, facecolor='w', edgecolor=self.edge_color,
                              fill=True, linewidth=LINE_WIDTH))

    def _draw_measurement(self, canvas, size, scale):
        x = self._get_central_axis(self.x, size)
        y = self._get_central_axis(self.control, size)
        radius = size * scale * .5
        canvas.add_patch(patches.Circle(xy=(x, y), radius=radius, fc=self.face_color, ec=self.edge_color, linewidth=LINE_WIDTH))

        canvas.text(x=x, y=y, s=self.measure_basis, style='italic', family='serif', ha='center', va='center', weight='bold', color=self.edge_color)

