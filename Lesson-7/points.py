
import math

class Point2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def __str__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        print("inside __eq__ of Point2D")
        if not isinstance(other, Point2D):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        print("inside __ne__ of Point2D")
        return self.x != other.x or self.y != other.y

    def __add__(self, other):
        if not isinstance(other,Point2D):
            return None
        new_point = Point2D(self.x+other.x , self.y + other.y)
        return new_point