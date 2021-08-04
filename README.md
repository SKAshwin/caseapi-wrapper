A wrapper around the [case-repository API](https://github.com/SKAshwin/case-repository) currently hosted at lcsscaseapi.duckdns.org (if this changes you need to chang the domain name in `lcsscaseapi/constants.py`).

Any use of the wrapper begins by initializing an LCSSClient object (defined in `lcsscaseapi/client.py`). This requires supplying a valid username and password. After this, requests can be made using methods of the object, and will return objects of types specified in `lcsscaseapi/types.py`. 

*Warning: Do not write the username and password supplied to the LCSSClient object in code that is committed to a repository. Fetch these details instead from environmental variblaes. Otherwise anyone reading your repository can access the API*

Testing uses pytest and requests-mocker and tests are located in the `tests/` directory.