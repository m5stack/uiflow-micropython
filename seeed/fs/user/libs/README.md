## /flash/libs

You can put some drivers in this folder.

### example

Create a new **test.py** driver file and put to this folder.

```python
class test():

    def __init__(self):
        print("test class")

    def test(self):
        print("test function")
```

You can import this driver in your application.

```python
from test import test

t = test()
t.test()
```