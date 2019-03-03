class Pose:
    def __init__(self, x, y, z, a , b, c):
        """
        :param x: unit(mm)
        :param y: unit(mm)
        :param z: unit(mm)
        :param a: unit(degree)
        :param b: unit(degree)
        :param c: unit(degree)
        """
        self.X = x
        self.Y = y
        self.Z = z
        self.A = a
        self.B = b
        self.C = c


class Color:
    def __init__(self, r, g, b, a):
        """
        :param r: 0-255
        :param g: 0-255
        :param b: 0-255
        :param a: 0-255
        """
        self.R = r
        self.G = g
        self.B = b
        self.A = a