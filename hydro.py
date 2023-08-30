import random
import math
import cairo
import ndist  # Assuming these modules exist in your setup
import hydro

red = 1, 0, 0
green = 0, 1, 0
instances = 1

class Animation:
    def __init__(self):
        self.filename = 0
        self.animate = False
        self.steps = 100

animation = Animation()

class TexasRanger:
    def __init__(self, x, y, curve, weight, ctx):
        self.x_position = x
        self.y_position = y
        self.alive = True
        self.pixel_steps_y = 1
        self.pixel_steps_x = 0
        self.curve_match = False
        self.curve = curve
        self.steps_walked = 0
        self.path = []
        self.exhausted = False
        self.weight = weight
        self.ctx = ctx

    def descend(self):
        self.y_position += self.pixel_steps_y
        self.x_position += self.pixel_steps_x
        self.path.append([self.x_position, self.y_position])
        self.weight = abs(100 / (1 if self.x_position == 0 else self.x_position))
        self.steps_walked += 1
        self.check_exhaustion()
        self.spawn_child()

    def check_exhaustion(self):
        if self.weight < 1 or abs(self.x_position) > 500 or abs(self.y_position) > 500:
            self.exhausted = True

    def spawn_child(self):
        if self.weight > 70 and self.y_position % 50 == 0 and not self.curve_match:
            spawn_walker(self.x_position + random.randint(-5, 5), self.y_position + random.randint(-5, 5), self.curve, self.ctx, color=green)

    def check_found(self, curve):
        for x, y in curve:
            if x == self.x_position and y == self.y_position:
                self.curve_match = True

    def paint_walker(self, ctx, color):
        previous_x, previous_y = None, None
        for x, y in self.path:
            if previous_x and previous_y:
                ctx.move_to(previous_x, previous_y)
            ctx.line_to(x, y)
            ctx.set_source_rgb(*color if self.curve_match else (1, 0, 1))
            ctx.set_line_width(1)
            ctx.stroke()
            if animation.animate and animation.filename % animation.steps == 0:
                surface.write_to_png(f'{animation.filename}.png')
            animation.filename += 1
            previous_x, previous_y = x, y
        if self.curve_match:
            paint_collision_dot(ctx, self.x_position, self.y_position)

def paint_collision_dot(ctx, x, y):
    ctx.set_source_rgb(1, 1, 0)
    ctx.arc(x, y, 10, 0, 2 * math.pi)
    ctx.fill()

def spawn_walkers(x, step, curve, ctx, color=red):
    for x_position in range(-x, x, step):
        walker = TexasRanger(x_position, -500, curve, 1.1, ctx)
        process_walker(walker, curve, ctx, color)

def spawn_walker(x, y, curve, ctx, color=red):
    walker = TexasRanger(x, y, curve, 1.1, ctx)
    process_walker(walker, curve, ctx, color)

def process_walker(walker, curve, ctx, color):
    while not walker.curve_match and not walker.exhausted:
        walker.descend()
        walker.check_found(curve)
    walker.paint_walker(ctx, color)

def main():
    for instance in range(instances):
        y_axis = hydro.get_sample()
        y_axis = [int(item * 1000) for item in y_axis]
        x_axis = ndist.define_x_axis(y_axis)
        curve = ndist.get_curve(x_axis, y_axis, reverse=True)

        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000)
        ctx = cairo.Context(surface)
        ctx.translate(500, 500)

        spawn_walkers(500, 5, curve, ctx)

        if not animation.animate:
            surface.write_to_png(f'{instance}.png')
        else:
            surface.write_to_png(f'{animation.filename}.png')

if __name__ == "__main__":
    main()
