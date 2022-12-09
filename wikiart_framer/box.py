class Point:
    def __init__(self, x: int = 0, y: int | None = None):
        self.x = x

        if y is None:
            self.y = x
        else:
            self.y = y

    def get_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


class Box:
    def __init__(self) -> None:
        self.originPoint = Point()
        self.cornerPoint = Point()

    def get_width(self) -> float:
        return abs(self.originPoint.x - self.cornerPoint.x)

    def get_height(self) -> float:
        return abs(self.originPoint.y - self.cornerPoint.y)

    def set_width(self, x: int) -> None:
        self.cornerPoint.x = self.originPoint.x + x

    def set_height(self, y: int) -> None:
        self.cornerPoint.y = self.originPoint.y + y

    def set_x_offset(self, x: int) -> None:
        self.originPoint.x = self.originPoint.x + x
        self.cornerPoint.x = self.cornerPoint.x + x

    def set_y_offset(self, y: int) -> None:
        self.originPoint.y = self.originPoint.y + y
        self.cornerPoint.y = self.cornerPoint.y + y

    def scale(self, factor: float) -> None:
        self.cornerPoint.x = self.cornerPoint.x * factor
        self.cornerPoint.y = self.cornerPoint.y * factor

    def get_center(self) -> Point:

        centerPoint = Point()
        centerPoint.x = int((self.originPoint.x + self.cornerPoint.x) / 2)
        centerPoint.y = int((self.originPoint.y + self.cornerPoint.y) / 2)

        return centerPoint

    def get_ratio(self) -> float:
        if self.get_height() == 0.0:
            return 0.0

        return self.get_width() / self.get_height()

    def get_tuple(self):
        return (
            self.originPoint.x,
            self.originPoint.y,
            self.cornerPoint.x,
            self.cornerPoint.y,
        )

    def __str__(self) -> str:
        return (
            "Larghezza: "
            + str(self.get_width())
            + " Altezza: "
            + str(self.get_height())
        )
