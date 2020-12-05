"""
General purpose functions that are used in the whole program
"""
from distutils.util import strtobool


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


def cast(data, cast_to_type):
    """
    Cast input data into the specified type

    Args:
        data: of any format that can be casted into one of cast_into_type option
        cast_into_type: to into which the data should be casted. options: str,
                        int, float, bool

    Returns:
        data casted in the specified type
    """
    try:
        # Booleans must be dealt separatadly since bool('False')
        # returns True instead of False.
        if cast_to_type is bool:
            casted_data = bool(strtobool(data))
        else:
            casted_data = cast_to_type(data)
        return casted_data
    except:
        error_msg = "The value: {d}, of type {d_type}, cannot be casted into" \
                    " type: {exp_type}".format(
                        d=data,
                        d_type=type(data),
                        exp_type=cast_to_type)
        raise TypeError(error_msg)


def add_end_of_line_to_file(f):
    """
    Enables further data to be appened on a new line

    Args:
        f: file that should be opened in write 'w' or append 'a' mode

    Returns:
        Void. The function only has side effect on the file in argument
    """
    # Mac version
    f.write('\n')
