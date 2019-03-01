from annotationfactory.annotationwriter import AnnotationWriter
import annotationfactory.annotationconverter as converter

example = {
    'tagId': 0,
    'tagName': 'apples',
    'region': {
        'left': 0.288039029,
        'top': 0.411838,
        'width': 0.291451037,
        'height': 0.4237842
    }
}

writer = AnnotationWriter()

writer.initVoc("test.jpg", 608, 608)
writer.initYolo()

writer.addVocObject(example)
writer.addVocObject(example)

writer.addYoloObject(example)
writer.addYoloObject(example)

writer.saveVoc("myannotation.xml")
writer.saveYolo("myannotation.txt")

converter.convertVocFromPath("myannotation.xml")
converter.convertYoloFromPath("myannotation.txt", "class.names")
