"""
General purpose functions that are used in the whole program
"""


def get_input(message):
    """
    Get data from user

    Args:
        message: the message to pass to user

    Returns:
        the data input

    Notes:
        Methods:
        1. extension of python built-in input function
        2. [not implemented] via web interface
    """
    # Method 1:
    eof = '\n'
    data_input = input(message + eof)
    return data_input


def cast(data, cast_into_type):
    """
    Cast input data into the specified type

    Args:
        data: of any format that can be casted into one of cast_into_type option
        cast_into_type: to into which the data should be casted. options: 'str',
                        'int', 'float'

    Returns:
        data casted in the specified type
    """
    raise NotImplementedError
