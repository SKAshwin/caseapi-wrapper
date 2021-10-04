# API for judicial cases
Author: Ashwin Kumar

A wrapper around the [case-repository API](https://github.com/SKAshwin/case-repository)
currently hosted at lcsscaseapi.duckdns.org (if this changes you need to change the domain
name in `lcsscaseapi/constants.py`).

Any use of the wrapper begins by initializing an LCSSClient object (defined in
`lcsscaseapi/client.py`). This requires supplying a valid username and password. After
this, requests can be made using methods of the object, and will return objects of types
specified in `lcsscaseapi/types.py`. 

*Warning: Do not write the username and password supplied to the LCSSClient object in code
that is committed to a repository. Fetch these details instead from environmental
variables. Otherwise anyone reading your repository can access the API.*

Testing uses pytest and requests-mocker and tests are located in the `tests/` directory.


### Example use cases
Fetching cases
```
from lcsscaseapi.client import LCSSClient
from lcsscaseapi.types import USCircuitCaseMeta

client = LCSSClient(USER_NAME, PASSWORD)
cases = client.get_cases(circuit=USCircuitCaseMeta.FIRST_CIRCUIT,
                         date_after='1996-01-01', date_before='1996-12-31')
```


### Publishing to Pypi

To publish new versions, change the version number in setup.cfg, generate a new
distribution and upload it to twine. See here:
https://packaging.python.org/tutorials/packaging-projects/ 

To be precise, run `python3 -m build`. Then run `twine upload dist/*`.
