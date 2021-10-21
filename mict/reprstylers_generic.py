
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

_pandas_available = False
try:
    import pandas
    _pandas_available = True
except:
    pass


def reprstyler_basic(subject=None):
    txt = 'keys:'
    for key in subject.keys():
        if key == 'reprstyler' or key == 'reprstyler_html':  # do not list reprstyler
            continue
        txt = f"{txt}'{key}', "
    return txt


def reprstyler_basic_html(subject=None, second_arg=None):
    from .mict import mict
    # print(second_arg) ??? why would it give me two arguments?? python bug?
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
        value = subject[key]
        # display the content according to type
        if isinstance(subject[key], float):
            txt = f'{txt} <td> {subject[key]:0.2f}</td>'
        elif callable(subject[key]):
            # display a function name and signature
            qf = subject[key]
            fname = qf.__code__.co_name
            if fname[0] == '<': # in case if it is a lambda, strip the html tag
                fname=fname[1:-1]
            rstr = f'{key}'
            rstr = f'{rstr}('
            for var_ in qf.__code__.co_varnames:
                rstr = f'{rstr}{var_},'
            rstr = f'{rstr[:-1]})'
            txt = f'{txt}<td> <code>{rstr}</code></td>'
        elif isinstance(subject[key], int):
            txt = f'{txt} <td> {subject[key]}</td>'
        elif isinstance(subject[key], str):
            txt = f'{txt} <td> {subject[key]}</td>'
        elif isinstance(subject[key], list):
            this_list = subject[key]
            if len(this_list)>5:
                first_element_type=str(type(this_list[0]))
                txt = f'{txt} <td> list({first_element_type},...) len={len(this_list)} </td>'
            else:
                proposed_str = this_list.__repr__()
                if len(proposed_str)<40:
                    txt = f'{txt} <td> {proposed_str}</td>'
                else:
                    txt = f'{txt} <td> {proposed_str[0:40]} (...)</td>'
        elif _numpy_available and isinstance(subject[key], np.ndarray):
            txt = f'{txt} <td>np.array(shape={subject[key].shape}) </td>'
        elif _tensorflow_available and tf.is_tensor(subject[key]):
            txt = f'{txt} <td>tf tensor(shape={subject[key].shape}) </td>'
        elif _pandas_available and isinstance(value, pandas.core.frame.DataFrame):
            col_names = f''.join(f'{v},</br>' for v in value.columns)
            txt = f'{txt}<td><strong>pandas.DataFrame</strong>(columns=([</br>{col_names}]) --- rows:{len(value)}.</td>'
        elif isinstance(subject[key], bytes):
            txt = f'{txt}<td><strong>bytes</strong>[{len(subject[key])}]</td>'
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
