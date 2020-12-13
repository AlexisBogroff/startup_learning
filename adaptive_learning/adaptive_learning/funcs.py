"""
General purpose functions that are used in the whole program
"""
import json
import uuid
from distutils.util import strtobool


def add_end_of_line_to_file(f_without_empty_line):
    """
    Enables further data to be appened on a new line

    Args:
        f: file that should be opened in write 'w' or append 'a' mode

    Returns:
        Void. The function only has side effect on the file in argument
    """
    # Mac version
    f_without_empty_line.write('\n')


def append_to_file(exportable, f_path):
    """
    Append the dump to the existing text file

    It is a library style db, since it stores an independant instances
    each time the function is called
    """
    with open(f_path, 'a') as library:
        json.dump(exportable, library)
        add_end_of_line_to_file(library)


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


def extract_data(id, data):
    """
    Extract the specific sample

    Hopefully returns a singleton (a list with only one element).

    Args:
        id: the id of elemnt to extract
        data: a list containing dictionaries, the latter having the key 'id'.

    data = [
        {'id': 123, 'foo1': 'bar1'},
        {'id': 433, 'foo2': 'bar2'},
        ...
    ]

    Returns:
        a list of the matching samples
    """
    samples = [sample for sample in data if sample['id'] == id]
    return samples


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


def get_single_elem(list_):
    """ Get the first and only element of a list """
    return list_[0]


def is_empty(data):
    """
    Check that input contains an element

    Args:
        data (list)
    """
    if data:
        return False
    else:
        return True


def is_single(data):
    """
    Check data contains a single sample

    Args:
        data (list)
    """
    if len(data) == 1:
        return True
    else:
        return False


def load_table(f_path):
    """
    Loads data from a text file

    Returns:
        the whole file content in a list

    TODO: add a method to load only part of the file
    """
    with open(f_path, 'r') as library:
        table = [json.loads(row) for row in library]
    return table


def retrieve_sample_from_table(id_sample, path_table):
    """
    Retrieve unique sample from table given its id

    Args:
        id_sample: the id of the sample to retrieve
        path_table: the path to the table containing the sample

    Returns:
        dictionary containing the unique sample
    """
    table = load_table(f_path=path_table)
    extracted_data = extract_data(id_sample, table)

    if is_empty(extracted_data):
        raise ValueError("Missing sample id {}".format(id_sample))

    if not is_single(extracted_data):
        raise ValueError("Duplicate sample ids {}".format(id_sample))

    sample_unique = get_single_elem(extracted_data)
    return sample_unique
