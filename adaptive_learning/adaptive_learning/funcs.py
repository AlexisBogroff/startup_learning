"""
General purpose functions that are used in the whole program
"""
import json
import uuid
from distutils.util import strtobool

def _add_end_of_line_to_file(f_without_empty_line):
    """
    Enables further data to be appened on a new line

    Args:
        f: file that should be opened in write 'w' or append 'a' mode

    Returns:
        Void. The function only has side effect on the file in argument
    """
    # Mac version
    f_without_empty_line.write('\n')



def append_to_file(data, f_path):
    """
    Append the dump to the existing text file

    It is a library style db, since it stores an independant instances
    each time the function is called
    """
    with open(f_path, 'a') as library:
        json.dump(data, library)
        _add_end_of_line_to_file(library)


def input_bool(message):
    """
    Ask the user a question expecting a boolean answer

    Args:
        message: string displayed to the user

    Returns:
        user_ans (boolean) if corresponds to a boolean-like value
    """
    ATTEMPTS = 3
    answer = None

    for _ in range(ATTEMPTS):
        try:
            answer = bool(strtobool(get_input(message)))
            return answer
        except:
            pass


def input_from_list(message, vals):
    """
    Ask user to enter a value from a list

    Args:
        message: string displayed to the user
        vals: list of values used for validation

    Returns:
        the answer
    """
    ATTEMPTS = 3
    answer = None

    for _ in range(ATTEMPTS):
        answer = get_input(message)

        if answer in vals:
            return answer


def cast(data, cast_to_type):
    """
    Cast input data into the specified type

    Args:
        data: of any format that can be casted into one of cast_into_type option
        cast_into_type: to into which the data should be casted. options: str,
                        int, float, bool

    Returns:
        data casted in the specified type

    TODO: add an inplace argument?
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
                    " type: {exp_type}".format(d=data,
                                               d_type=type(data),
                                               exp_type=cast_to_type)
        raise TypeError(error_msg)


def generate_uuid(type=str):
    """ Generate unique identifier """
    if type is str:
        return str(uuid.uuid4())


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
