import xmltodict
from annotationfactory.models.annotation import Annotation
from annotationfactory.models.region import Region


class AnnotationConverter:

    '''
    AnnotationConvert helps converts Pascal VOC and YOLO to
    CustomVision annotations.

    Optional:
        classes ([str]): Object class list for use when
                         converting YOLO annotations.
    '''

    def __init__(self, classes=None):

        self.classes = classes

    def convertVoc(self, area: dict, dim: [2]) -> Annotation:

        '''
        Convert VOC object to CustomVision annotations.

        Args:
            area (dict): VOC annotation of a single region.
            dim ([float, float]): Width and height of target
                                  image.

        Returns:
            ~annotationfactory.models.annotation
        '''

        (w, h) = dim

        region = area["bndbox"]
        tag = area["name"]

        left = float(region['xmin']) / w
        top = float(region['ymin']) / h
        width = float(region["xmax"]) / w
        height = float(region["ymax"]) / h

        region = Region(left, top, width, height)

        return Annotation(tagName=tag, region=region)

    def convertYolo(self, line: str) -> Annotation:

        '''
        Convert YOLO object to CustomVision annotations.

        Args:
            line (str): A single line from YOLO annotation.txt
                        file.

        Returns:
            ~annotationfactory.models.annotation
        '''

        region = line.split()
        tag = None

        (x_centre, y_centre, w, h) = region[1:]

        left = float(x_centre) - (float(w) / 2)
        top = float(y_centre) - (float(h) / 2)
        width = float(w)
        height = float(h)

        if self.classes is not None:
            tag = self.classes[int(region[0])]

        region = Region(left, top, width, height)

        return Annotation(tagName=tag, region=region)


def convertVocFromPath(path: str) -> [Annotation]:

    '''
    Convert VOC annotation.xml file to CustomVision annotations.

    Args:
        path (str): Path directory to annotation.xml file on local machine.

    Returns:
        list[~annotationfactory.models.annotation]
    '''

    converter = AnnotationConverter()

    with open(path) as f:
        voc = xmltodict.parse(f.read())["annotation"]

    w = float(voc["size"]["width"])
    h = float(voc["size"]["height"])

    annotations = []

    for i in voc["object"]:
        annotations.append(converter.convertVoc(i, (w, h)))

    return annotations


def convertYoloFromPath(path: str, classPath: str = None) -> [Annotation]:

    '''
    Convert YOLO annotation.txt file to CustomVision annotations.

    Args:
        path (str): Path directory to annotation.xml file on local machine.
        classPath (str): Path directory to class.names file on local machine.

    Returns:
        list[~annotationfactory.models.annotation]
    '''

    converter = AnnotationConverter(parseFile(classPath))

    yolo = parseFile(path)

    annotations = []

    for i in yolo:
        annotations.append(converter.convertYolo(i))

    return annotations


def parseFile(path: str) -> [str]:

    '''
    Reads file from path line-by-line into list.

    Args:
        path (str): Path directory to any.txt file on local machine.

    Returns:
        list[str]
    '''

    with open(path) as f:
        result = f.read().split("\n")
        if result[-1] == "":
            result = result[:-1]

    return result
