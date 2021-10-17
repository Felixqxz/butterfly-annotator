import unittest
from ..images.annotations import RectangularAnnotation, PolygonalAnnotation
from ..images.geometry import Point
from random import randint

RAND_ITERATIONS = 100


def random_point():
    return Point(randint(1, 1001), randint(1, 1001))


class TestRectangularRegions(unittest.TestCase):
    def test_simple_serialization_case(self):
        rect = RectangularAnnotation(Point(168, 517), Point(352, 194), '')
        self.assertEqual(rect.sql_serialize_region(), '168,517;352,194')

    def test_serialize_random(self):
        for i in range(RAND_ITERATIONS):
            x = randint(1, 1001)
            y = randint(1, 1001)
            a = randint(1, 1001)
            b = randint(1, 1001)
            rect = RectangularAnnotation(Point(x, y), Point(a, b), '')
            self.assertEqual(f'{x},{y};{a},{b}', rect.sql_serialize_region())

    def test_deserialize_random(self):
        for i in range(RAND_ITERATIONS):
            x = randint(1, 1001)
            y = randint(1, 1001)
            a = randint(1, 1001)
            b = randint(1, 1001)
            raw_input = f'{x},{y};{a},{b}'
            annotation = RectangularAnnotation.deserialize_from_sql(raw_input, '')
            self.assertEqual(annotation.low_left.x, x)
            self.assertEqual(annotation.low_left.y, y)
            self.assertEqual(annotation.up_right.x, a)
            self.assertEqual(annotation.up_right.y, b)
            self.assertEqual(raw_input, annotation.sql_serialize_region())


class TestPolygonalAnnotations(unittest.TestCase):
    @staticmethod
    def random_gen(angles):
        return [random_point() for _ in range(angles)]

    def test_simple_serialization_case(self):
        tri = PolygonalAnnotation(
            [Point(123, 456), Point(124, 234), Point(435, 128)], ''
        )
        self.assertEqual(tri.sql_serialize_region(), '123,456;124,234;435,128')

    def test_serialize_random_triangles(self):
        for i in range(RAND_ITERATIONS):
            all_points = TestPolygonalAnnotations.random_gen(3)
            tri = PolygonalAnnotation(all_points, '')
            self.assertEqual(tri.sql_serialize_region(),
                             f'{all_points[0].x},{all_points[0].y};'
                             f'{all_points[1].x},{all_points[1].y};'
                             f'{all_points[2].x},{all_points[2].y}')

    def test_deserialize_random_triangles(self):
        for i in range(RAND_ITERATIONS):
            all_points = TestPolygonalAnnotations.random_gen(3)
            raw_input = f'{all_points[0].x},{all_points[0].y};' \
                        f'{all_points[1].x},{all_points[1].y};' \
                        f'{all_points[2].x},{all_points[2].y}'
            tri = PolygonalAnnotation.deserialize_from_sql(raw_input, '')
            self.assertEqual(tri.sql_serialize_region(), raw_input)


if __name__ == '__main__':
    unittest.main()
