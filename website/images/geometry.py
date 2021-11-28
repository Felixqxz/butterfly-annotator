from abc import abstractmethod


class Point:
    """
    Represents a 2D point.
    """

    def __init__(self, x, y):
        """
        :param x: x-coordinate
        :param y: y-coordinate
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def sql_serialize(self):
        return f'{self.x},{self.y}'

    @staticmethod
    def deserialize(sql):
        pred = sql.split(',', 1)
        return Point(int(pred[0]), int(pred[1]))


class ImageRegion:
    """
    Represents annotations on an image region described by a tag.

    The shape of the region depends on the chosen implementation.
    """

    def __init__(self):
        pass

    @abstractmethod
    def sql_serialize_region(self):
        """
        Returns a string representation of the annotation's region ready
        for the SQL storage.
        """
        pass


class PolygonalRegion(ImageRegion):
    """
    An implementation of `ImageRegion` for polygonal regions.

    Use `RectangularAnnotation` for rectangular regions.
    """

    def __init__(self, points):
        """
        :param points: a list of at least three 2D points (`Point` class
            from `geometry.py`) that define the polygon
        """
        super().__init__()
        # allow 2 points for rectangles
        assert points is not None and len(points) > 1
        self.points = points

    def sql_serialize_region(self):
        raw = [f'{point.sql_serialize()}' for point in self.points]
        return ';'.join(raw)

    @staticmethod
    def deserialize_from_sql(sql):
        """
        Deserializes a `PolygonalRegion` from `sql`.

        :param sql: the raw serialization text
        """
        parts = sql.split(';')
        new_points = [Point.deserialize(part) for part in parts]
        return PolygonalRegion(new_points)

    @staticmethod
    def deserialize_from_json(raw):
        """
        Deserializes a `PolygonalRegion` from `raw`.

        :param raw: the raw JSON array of input points
        """
        return PolygonalRegion([Point(p['x'], p['y']) for p in raw])
