import numpy as np
import random


class Expr:

    def __call__(self, x, y):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class X(Expr):

    def __call__(self, x, y):
        return x

    def __str__(self):
        return "x"


class Y(Expr):

    def __call__(self, x, y):
        return y

    def __str__(self):
        return "y"


class Times(Expr):

    def __init__(self, prob):
        self.left = mkexpr(prob * prob)
        self.right = mkexpr(prob * prob)

    def __call__(self, x, y):
        return self.left(x, y) * self.right(x, y)

    def __str__(self):
        return '{} * {}'.format(self.left, self.right)


class Average(Expr):

    def __init__(self, prob):
        self.left = mkexpr(prob * prob)
        self.right = mkexpr(prob * prob)

    def __call__(self, x, y):
        return (self.left(x, y) + self.right(x, y)) / 2

    def __str__(self):
        return 'avg({}, {})'.format(self.left, self.right)


class SinPi(Expr):

    def __init__(self, prob):
        self.arg = mkexpr(prob * prob)

    def __call__(self, x, y):
        return np.sin(np.pi * self.arg(x, y))

    def __str__(self):
        return "sin(π{})".format(self.arg)


class CosPi(Expr):

    def __init__(self, prob):
        self.arg = mkexpr(prob * prob)

    def __call__(self, x, y):
        return np.cos(np.pi * self.arg(x, y))

    def __str__(self):
        return "cos(π{})".format(self.arg)


def mkexpr(prob=.999):
    if random.random() < prob:
        return random.choice([CosPi, SinPi, Average, Times])(prob)
    else:
        return random.choice([X, Y])()
