from jinja2 import Environment, PackageLoader
from jsonschema import validate
import json


class AnnotationWriter:

    '''
    AnnotationWriter is a lightweight VOC/YOLO annotation generator for use in
    machine learning.
    '''

    def __init__(self):

        environment = Environment(
            loader=PackageLoader('annotationfactory', 'templates'),
            keep_trailing_newline=True)

        self.annotation_voc_template = environment.get_template(
            'annotation.xml')
        self.annotation_yolo_template = environment.get_template(
            'annotation.txt')
        self.schema = json.loads(
            environment.get_template("schema.json").render())

        self.template_voc_parameters = None
        self.template_yolo_parameters = None

    def initVoc(self, file, width, height,
                depth=3, database='Unknown', segmented=0):

        '''
        Initialised AnnotationWriter to generate VOC annotations.

        Args:
            file (str): Name of image associated to annotation.
            width (int): Width of image.
            height (int): Height of image.

        Optional:
            depth (int): Depth of image.
            database (str): Name of database image belong to.
            segmented (int): Number of segmentations.
        '''

        self.width = width
        self.height = height
        self.file = file

        self.template_voc_parameters = {
            'filename': file,
            'folder': "images",
            'width': self.width,
            'height': self.height,
            'depth': depth,
            'database': database,
            'segmented': segmented,
            'objects': []
        }

    def initYolo(self):

        '''
        Initialised AnnotationWriter to generate YOLO annotations.
        '''

        self.template_yolo_parameters = []

    def addVocObject(
            self, annotation, pose='Unspecified', truncated=0, difficult=0):

        '''
        Add object annotation to VOC writer.

        Args:
            annotation (dict): Annotation object used to
                               generate VOC annotation.

        Optional:
            pose (str): Specify the pose of the annotation.
            truncated (int): Set the truncated vaule of annotation.
            difficult (int): Set difficulty index of annotation.

        Raises:
            NotImplementedError
            jsonschema.exceptions.ValidationError
        '''

        if self.template_voc_parameters is None:
            raise NotImplementedError("VOC has not been initialised.")

        validate(annotation, self.schema)

        box = annotation["region"]
        name = annotation["tagName"]

        xmin = float(box["left"]) * self.width
        ymin = float(box["top"]) * self.height
        xmax = float(box["width"]) * self.width
        ymax = float(box["height"]) * self.height

        self.template_voc_parameters['objects'].append({
            'name': name,
            'xmin': xmin,
            'ymin': ymin,
            'xmax': xmax,
            'ymax': ymax,
            'pose': pose,
            'truncated': truncated,
            'difficult': difficult,
        })

    def addYoloObject(self, annotation):

        '''
        Add object annotation to YOLO writer.

        Args:
            annotation (dict): Annotation object used to
                               generate YOLO annotation.

        Raises:
            NotImplementedError
            jsonschema.exceptions.ValidationError
        '''

        if self.template_yolo_parameters is None:
            raise NotImplementedError("YOLO has not been initialised.")

        validate(annotation, self.schema)

        box = annotation["region"]
        tag = annotation["tagId"]

        x_centre = float(box["left"] + (box["width"] / 2))
        y_centre = float(box["top"] + (box["height"] / 2))
        x_width = float(box["width"])
        y_height = float(box["height"])

        self.template_yolo_parameters.append({
            'id': tag,
            'x_centre': x_centre,
            'y_centre': y_centre,
            'x_width': x_width,
            'y_height': y_height
        })

    def saveVoc(self, annotation_path):

        '''
        Output VOC annotations to file.

        Args:
            annotation_path (str): Path of file to write annotation to.

        Raises:
            NotImplementedError
        '''

        if self.template_voc_parameters is None:
            raise NotImplementedError("VOC has not been initialised.")

        with open(annotation_path, 'w') as file:
            content = self.annotation_voc_template.render(
                **self.template_voc_parameters)
            file.write(content)

    def saveYolo(self, annotation_path):

        '''
        Output YOLO annotations to file.

        Args:
            annotation_path (str): Path of file to write annotation to.

        Raises:
            NotImplementedError
        '''

        if self.template_yolo_parameters is None:
            raise NotImplementedError("YOLO has not been initialised.")

        with open(annotation_path, 'w') as file:
            content = self.annotation_yolo_template.render(
                annotation=self.template_yolo_parameters)
            file.write(content)
