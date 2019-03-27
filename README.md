# Introduction 

[![Build Status](https://dev.azure.com/aussiedevcrew/Annotation-Factory/_apis/build/status/Microsoft.Annotation-Factory?branchName=master)](https://dev.azure.com/aussiedevcrew/Annotation-Factory/_build/latest?definitionId=9&branchName=master)
[![GitHub](https://img.shields.io/github/license/Microsoft/Annotation-Factory.svg?color=blue&label=License)](https://github.com/Microsoft/Annotation-Factory/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/annotationfactory.svg?label=PyPi)](https://pypi.org/project/annotationfactory/)
![Python Version](https://img.shields.io/pypi/pyversions/annotationfactory.svg?label=Python)

Annotation-Factory Python SDK. This package works specifically with Microsoft Cognitive Services detection results. `AnnotationWriter` takes a JSON object received from Cognitive Services and produces annotation files in both VOC and YOLO formats for use in training machine learning models.

# Getting Started

1. Install `annotationfactory` package via pip:
    
    ```
    pip install annotationfactory
    ```

# Sample to use

```python
from annotationfactory.annotationwriter import AnnotationWriter
import annotationfactory.annotationconverter as converter

example = {
    'tagId': 0,
    'tagName': 'Apples',
    'region': {
        'left': 0.288039029,
        'top': 0.411838,
        'width': 0.291451037,
        'height': 0.4237842
    }
}

# Initialise AnnotationWriter.
writer = AnnotationWriter()

# Initialise annotation handlers.
writer.initVoc("test.jpg", 608, 608)
writer.initYolo()

# Add VOC object to writer.
writer.addVocObject(example)
writer.addVocObject(example)

# Add YOLO object to writer.
writer.addYoloObject(example)
writer.addYoloObject(example)

# Output VOC annotations to file.
writer.saveVoc("myannotation.xml")

# Output YOLO annotations to file.
writer.saveYolo("myannotation.txt")

# Converts VOC annotations back to CustomVision annotation format.
voc2cv = converter.convertVocFromPath("myannotation.xml")

# Converts YOLO annotations back to CustomVision annotation format.
# Requires a txt file with list of label names as an input.
yolo2cv = converter.convertYoloFromPath("myannotation.txt", "class.names")

```

# Run locally

``` 
pip install -r requirements.txt 
python example/test.py
```

# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
