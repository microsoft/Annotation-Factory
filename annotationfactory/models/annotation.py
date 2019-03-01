import annotationfactory.models.region as Region


class Annotation:
    tagName = None
    region = None

    def __init__(self, tagName: str = None, region: Region = None):

        self.tagName = tagName
        self.region = region
