
_numpy_available = False
try:
    import numpy as np

    _numpy_available = True
except:
    pass

_tensorflow_available = False
try:
    import tensorflow as tf

    _tensorflow_available = True
except:
    pass

_pytorch_available = False
try:
    import pytorch

    _pytorch_available = True
except:
    pass

_jax_available = False
try:
    import jax

    _jax_available = True
except:
    pass


def reprstyler_basic(subject=None):
    txt = 'keys:'
    for key in subject.keys():
        if key == 'reprstyler' or key == 'reprstyler_html':  # do not list reprstyler
            continue
        txt = f"{txt}'{key}', "
    return txt


def reprstyler_basic_html(subject=None):
    from .mict import mict
    txt = ''
    if 'type' in subject.keys():
        txt = f'{txt}<em>Type:</em> {subject.type}; '
    if 'name' in subject.keys():
        txt = f'{txt}<em>Name:</em> {subject.name}; '
    txt = f'{txt}<br/>'
    txt = f'{txt}<table><tr><th>key</th><th>value</th></tr>'
    for key in subject.keys():
        if key == 'reprstyler' or key == 'reprstyler_html':  # do not list reprstyler
            continue
        # these two keys were listed already at the top:
        if key == 'type' or key == 'name':
            continue

        # begin row, display key name
        txt = f'{txt}<tr><td>{key}</td>'

        # display the content according to type
        if isinstance(subject[key], float):
            txt = f'{txt} <td> {subject[key]}</td>'
        elif isinstance(subject[key], int):
            txt = f'{txt} <td> {subject[key]}</td>'
        elif isinstance(subject[key], str):
            txt = f'{txt} <td> {subject[key]}</td>'
        elif _numpy_available and isinstance(subject[key], np.ndarray):
            txt = f'{txt} <td> np.array(shape={subject[key].shape}) </td>'
        elif _tensorflow_available and tf.is_tensor(subject[key]):
            txt = f'{txt} <td> tf tensor(shape={subject[key].shape}) </td>'
        elif isinstance(subject[key], mict):
            inner_mict = subject[key]
            inner_mict_visualiser_result = inner_mict._repr_html_()
            txt = f'{txt}<td>{inner_mict_visualiser_result}</td>'
        else:  # any other type:
            txt = f'{txt} <td> {subject[key]} </td>'
        # end of table row
        txt = f'{txt} </tr> '
        # end for key in subject.keys()
    # end of html table
    txt = f'{txt} </table>'
    return txt