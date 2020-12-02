"""
General purpose functions that are used in the whole program
"""


def get_input(data_structure_along_prompt_messages):
    """
    Get data from user

    Args:
        data_structure_along_prompt_messages: a dictionary with keys and
            messages providing the user indications on data to enter.
            It must be of the form:
            {
                'data1': 'msg1',
                'data2': 'msg2',
                ...
                'datan': 'msgn',
            }
            If no message is used for a key, leave an empty string.

    Returns:
        Input data in a dictionary

    Notes:
        Methods:
        1. via python built-in input function
        2. [not implemented] via web interface
    """
    # Method 1:
    data_output = {}

    # Prompt user with the specified messages and store data
    for key, msg in data_structure_along_prompt_messages.items():
        data_output[key] = input(msg + "\n")

    return data_output


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
