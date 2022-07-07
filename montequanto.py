import random
import time

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math
import cairo
import ndist

red = 1, 0, 0
green = 0, 1, 0
instances = 200


class Animation:
    def __init__(self):
        self.filename = 0
        self.animate = False
        self.steps = 100

animation = Animation()
animation.animate = False


def azero(is_zero):
    """design needs to change"""
    if is_zero == 0:
        return 1
    else:
        return is_zero


class TexasRanger:
    def __init__(self, x, y, curve, weight):
        self.x_position = x
        self.y_position = y
        self.alive = True

        self.pixel_steps_y = +1
        self.pixel_steps_x = 0

        self.curve_match = False
        self.curve = curve

        self.steps_walked = 0
        self.path = []
        self.exhausted = False

        self.weight = weight

    def descend(self):
        self.y_position = self.y_position + self.pixel_steps_y
        self.x_position = self.x_position + self.pixel_steps_x
        self.path.append([self.x_position, self.y_position])

        self.weight = abs(100 / azero(self.x_position))  # +1 hack to avoid 0

        self.steps_walked += 1
        if self.weight < 1 or -500 < self.x_position > 500 or -500 < self.y_position > 500:
            self.exhausted = True

        if self.weight > 70 and self.y_position % 50 == 0 and not self.curve_match:  # limit new spawns to every 50 y descend steps
            spawn_walker(self.x_position + random.randint(-5, 5), self.y_position + random.randint(-5, 5), self.curve,
                         color=green)
            print("child spawned")

    def check_found(self):
        for x, y in curve:

            if x == self.x_position and y == self.y_position:
                self.curve_match = True

                # self.paint_walker(ctx)

    def paint_walker(self, ctx, color):

        previous_x = None
        previous_y = None
        for x, y in self.path:
            if previous_x and previous_y:
                ctx.move_to(previous_x, previous_y)

            if self.curve_match:
                ctx.set_source_rgb(color[0], color[1], color[2])  # 100 red
                ctx.set_line_width(1)
                ctx.line_to(x, y)
                ctx.stroke()
            else:
                ctx.set_source_rgb(1, 0, 1)
                ctx.set_line_width(1)
                ctx.line_to(x, y)
                ctx.stroke()
            if animation.animate:
                if animation.filename % animation.steps == 0:
                    surface.write_to_png(f'{animation.filename}.png')
                animation.filename += 1

            previous_x = x
            previous_y = y

        if self.curve_match:
            # paint collision dot
            ctx.set_source_rgb(1, 1, 0)
            ctx.move_to(self.x_position, self.y_position)
            ctx.arc(self.x_position, self.y_position, 10, 0, 2 * math.pi)
            ctx.fill()
            # paint collision dot

def spawn_walkers(x, step, color=red):
    for x_position in range(-x, x, step):
        walker = TexasRanger(x=x_position, y=-500, curve=curve, weight=1.1)
        while not walker.curve_match and not walker.exhausted:
            walker.descend()
            walker.check_found()
        walker.paint_walker(ctx, color)


def spawn_walker(x, y, curve, color=red):
    walker = TexasRanger(x, y, curve, weight=1.1)
    while not walker.curve_match and not walker.exhausted:
        walker.descend()
        walker.check_found()
    walker.paint_walker(ctx, color)

for instance in range(0,instances):
    offset_x = 0
    offset_y = 250

    y_axis = ndist.get_y_axis(ndist=ndist.get_ndist_list(size=500))
    x_axis = ndist.define_x_axis(y_axis)
    curve = ndist.get_curve(x_axis, y_axis, reverse=True)

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                 1000,
                                 1000)
    ctx = cairo.Context(surface)
    ctx.translate(500, 500)

    # paint curve

    previous_x = None
    previous_y = None
    for x, y in curve:
        if previous_x and previous_y:
            ctx.move_to(previous_x, previous_y)

        # print(x, y)

        ctx.line_to(x, y)
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(1)
        ctx.stroke()

        previous_x = x
        previous_y = y
    # paint curve


    step = 20

    spawn_walkers(500, step)

    if not animation.animate:
        surface.write_to_png(f'{instance}.png')
    else:
        surface.write_to_png(f'{animation.filename}.png')
