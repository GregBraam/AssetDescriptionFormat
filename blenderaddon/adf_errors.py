class MissingImageData(Exception):
    """Image missing data."""
    def __init__(self,image_name):
        self.image_name = image_name