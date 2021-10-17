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
    def deserialize_from_sql(sql):
        pred = sql.split(',', 1)
        return Point(int(pred[0]), int(pred[1]))
