class Point:
    x = 0
    y = 0

    def __init__(self, x=0, y=None):
        self.x = x

        if y is None:
            self.y = x
        else:
            self.y = y

    def get_tuple(self):
        return (self.x, self.y)


class Box:
    originX = 0
    originY = 0
    width = 0
    height = 0

    originPoint = Point()
    cornerPoint = Point()

    def get_center(self):

        centerPoint = Point()
        centerPoint.x = int((self.originPoint.x + self.cornerPoint.x) / 2)
        centerPoint.y = int((self.originPoint.y + self.cornerPoint.y) / 2)

        return centerPoint

    def get_tuple(self):
        return (
            self.originPoint.x,
            self.originPoint.y,
            self.cornerPoint.x,
            self.cornerPoint.y,
        )
