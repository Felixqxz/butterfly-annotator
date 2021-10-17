from abc import abstractmethod
from .geometry import Point


class ImageAnnotation:
    """
    Represents annotations on an image region described by a tag.

    The shape of the region depends on the chosen implementation.
    """

    def __init__(self, tag):
        """
        :param tag: is the tag that describes the current annotation
        """
        self.tag = tag

    def get_tag(self):
        """
        Returns the tag of the annotation, i.e. the textual description 
        of the annotation.
        """
        return self.tag

    @abstractmethod
    def sql_serialize_region(self):
        """
        Returns a string representation of the annotation's region ready
        for the SQL storage.
        """
        pass


class RectangularAnnotation(ImageAnnotation):
    """
    An implementation of ImageAnnotation for rectangular regions.
    """

    def __init__(self, low_left, up_right, tag):
        """
        :param low_left: the lower left corner of the rectangle
        :param up_right: the upper right corner of the rectangle
        """
        super().__init__(tag)
        self.low_left = low_left
        self.up_right = up_right

    def sql_serialize_region(self):
        return f'{self.low_left.sql_serialize()};{self.up_right.sql_serialize()}'

    @staticmethod
    def deserialize_from_sql(sql, tag):
        """
        Deserializes a `RectangularAnnotation` from `sql`.

        :param sql: the raw serialization text
        :param tag: the annotation's tag
        """
        spl = sql.split(';', 1)
        a = Point.deserialize_from_sql(spl[0])
        b = Point.deserialize_from_sql(spl[1])
        return RectangularAnnotation(a, b, tag)


class PolygonalAnnotation(ImageAnnotation):
    """
    An implementation of ImageAnnotation for polygonal regions.

    Use `RectangularAnnotation` for rectangular regions.
    """
    def __init__(self, points, tag):
        """
        :param points: a list of at least three 2D points (`Point` class 
            from `geometry.py`) that define the polygon
        """
        super().__init__(tag)
        assert points is not None and len(points) > 2
        self.points = points

    def sql_serialize_region(self):
        raw = [f'{point.sql_serialize()}' for point in self.points]
        return ';'.join(raw)

    @staticmethod
    def deserialize_from_sql(sql, tag):
        """
        Deserializes a `RectangularAnnotation` from `sql`.

        :param sql: the raw serialization text
        :param tag: the annotation's tag
        """
        parts = sql.split(';')
        new_points = [Point.deserialize_from_sql(part) for part in parts]
        return PolygonalAnnotation(new_points, tag)
