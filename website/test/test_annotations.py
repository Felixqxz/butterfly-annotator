import unittest
from ..images.geometry import Point, PolygonalRegion
from random import randint

RAND_ITERATIONS = 100


def random_point():
    return Point(randint(1, 1001), randint(1, 1001))


class TestPolygonalRegions(unittest.TestCase):
    @staticmethod
    def random_gen(angles):
        return [random_point() for _ in range(angles)]

    def test_simple_serialization_case(self):
        tri = PolygonalRegion(
            [Point(123, 456), Point(124, 234), Point(435, 128)]
        )
        self.assertEqual(tri.sql_serialize_region(), '123,456;124,234;435,128')

    def test_serialize_random_triangles(self):
        for i in range(RAND_ITERATIONS):
            all_points = TestPolygonalRegions.random_gen(3)
            tri = PolygonalRegion(all_points)
            self.assertEqual(tri.sql_serialize_region(),
                             f'{all_points[0].x},{all_points[0].y};'
                             f'{all_points[1].x},{all_points[1].y};'
                             f'{all_points[2].x},{all_points[2].y}')

    def test_deserialize_random_triangles(self):
        for i in range(RAND_ITERATIONS):
            all_points = TestPolygonalRegions.random_gen(3)
            raw_input = f'{all_points[0].x},{all_points[0].y};' \
                        f'{all_points[1].x},{all_points[1].y};' \
                        f'{all_points[2].x},{all_points[2].y}'
            tri = PolygonalRegion.deserialize_from_sql(raw_input)
            self.assertEqual(tri.sql_serialize_region(), raw_input)


if __name__ == '__main__':
    unittest.main()
