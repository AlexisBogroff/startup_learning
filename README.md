# Future official Dev branch
In the process of extracting code of the business case from the web application layer. The web application will then be importing "adaptive_learning" as a library.

To make this possible, "adaptive_learning" should be a package. Run the following instructions in a terminal, where the file setup.py is located:
```
python sdist bdist_wheel build
python setup.py develop
```

To understand where these come from see [a very quick note](https://github.com/AlexisBogroff/CheatSheets/blob/master/PythonPackaging.md#install-the-package)
or its [source article](https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html)


# Development Branch (Dev)
Most up to date branch, containing beta features

For a more stable version use the Master's

## Style guide
- PEP8: https://www.python.org/dev/peps/pep-0008/
- PEP257: https://www.python.org/dev/peps/pep-0257/
- Google Style Guide: https://google.github.io/styleguide/pyguide.html

```python
def test_function(arg1):
    """
    Describe the goal of the function in few words, not how
    the function reaches this goal

    Args:
        arg1: describe the first parameter
        arg2: describe the second parameter

    Returns:
        describe what is returned

    Examples:
        show some examples on how to use the function

    Notes:
        describe eventual side-effects
    """
```

Use pylint to highlight mistakes and rate your code.
