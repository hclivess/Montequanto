import math
import cairo
import ndist


class Animation:
    def __init__(self):
        self.filename = 0
        self.animate = False
        self.steps = 100


class TexasRanger:
    def __init__(self, x, y, curve):
        self.x_position = x
        self.y_position = y
        self.curve_match = False
        self.curve = curve
        self.path = []
        self.weight = 1.1
        self.exhausted = False

    def descend(self):
        self.y_position += 1
        self.path.append([self.x_position, self.y_position])
        self.weight = abs(100 / (self.x_position if self.x_position != 0 else 1))
        self.exhausted = self._is_exhausted()

    def check_found(self):
        self.curve_match = any(
            x == self.x_position and y == self.y_position for x, y in self.curve)

    def paint_walker(self, ctx, color):
        self._paint_path(ctx, color)
        if self.curve_match:
            self._paint_collision_dot(ctx)

    def _paint_path(self, ctx, color):
        for (prev_x, prev_y), (x, y) in zip(self.path[:-1], self.path[1:]):
            ctx.move_to(prev_x, prev_y)
            ctx.set_source_rgb(*color if self.curve_match else (1, 0, 1))
            ctx.line_to(x, y)
            ctx.stroke()

    def _paint_collision_dot(self, ctx):
        ctx.set_source_rgb(1, 1, 0)
        ctx.arc(self.x_position, self.y_position, 10, 0, 2 * math.pi)
        ctx.fill()

    def _is_exhausted(self):
        return self.weight < 1 or abs(self.x_position) > 500 or abs(self.y_position) > 500


def spawn_walkers(x_range, step, curve, ctx):
    for x_position in range(-x_range, x_range, step):
        spawn_walker(x_position, -500, curve, ctx, color=(1, 0, 0))


def spawn_walker(x, y, curve, ctx, color):
    walker = TexasRanger(x, y, curve)
    while not walker.curve_match and not walker.exhausted:
        walker.descend()
        walker.check_found()
    walker.paint_walker(ctx, color)


animation = Animation()
instances = 200

for instance in range(instances):
    y_axis = ndist.get_y_axis(ndist=ndist.get_ndist_list(size=500))
    x_axis = ndist.define_x_axis(y_axis)
    curve = ndist.get_curve(x_axis, y_axis, reverse=True)

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000)
    ctx = cairo.Context(surface)
    ctx.translate(500, 500)

    # Paint curve
    for (prev_x, prev_y), (x, y) in zip(curve[:-1], curve[1:]):
        ctx.move_to(prev_x, prev_y)
        ctx.line_to(x, y)
        ctx.set_source_rgb(1, 1, 1)
        ctx.stroke()

    spawn_walkers(500, 20, curve, ctx)
    surface.write_to_png(f'{instance}.png')
