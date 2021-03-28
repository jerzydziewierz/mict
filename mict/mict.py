from warnings import warn
from .reprstylers_generic import reprstyler_basic_html
from .reprstylers_generic import reprstyler_basic




class mict(dict):
    """Provides matlab-like setting/storage of items in a dict (dictionary) and a handful of interactivity tools.

    `mict` is intended to be a middle ground between dict and full fledged object for data storage

    it does a bit more than basic dict, but does not attempt to superseede pandas, numpy nor other advanced data storage tools

    ### Usage

    ```python
    from mict import mict
    q=mict()
    q.new_key = 'Hello world!'
    print(q.new_key)
    print(q)
    ```


    example reprstyler:

    ```python
    from mict import mict
    q=mict(zap=None,bald=6.28)

    def baldstyler(subject):
        return f'baldness score: {subject.bald:0.3f}'

    q.reprstyler=baldstyler

    q
    ```

    then, if you want a different styler for jupyter, and a different one for text-only, you can (optionally) override the reprstyler with reprstyler_html. It will only be used if _repr_html_ is called.

    ```
    def baldstyler_html(subject):
        return f'<h1>baldness score: {subject.bald:0.3f}</h1>'
    q.reprstyler_html = baldstyler_html
    q
    ```

    If you really feel like it, this could be extended to markdown, png, svg and other visualizers supported by jupyter.

    Importantly, you can still see the regular dict __repr__ (lists all keys/values) using

    ```python
    super(handybeam.dict,q).__repr__()
    ```


    ### Pickle convenience interface

    These work as you would expect:

    ```python
    q1.to_pickle(filename)
    q2=mict.from_pickle(filename)
    ```


    ### Gotchas

    * `mict` does not throw an error when trying to access undefined field. Instead, it returns `None`


    ### Attributions

    Happily copypasted from https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary , and modified only slightly.

    then, extended a bit.

    then, a bit more, with optional reprstyler. See self.__repr__();


    """

    def __init__(self, args={}, reprstyler_html=reprstyler_basic_html, **kwargs):
        """ starts the instance.

        example use:

        ```python
        from mict import mict
        q=mict(a=3,b=4,c="covid")

        ```

        :param args: initial value in the dictionary.
        """
        super(mict, self).__init__(args)
        if args is not None:
            if isinstance(args, dict):
                for k, v in args.items():
                    if not isinstance(v, dict):
                        self[k] = v
                    else:
                        self.__setattr__(k, mict(v))

        # add a hard-coded value "reprstyler". This will be used to redirect repr to the given function

        # self.update({'reprstyler': None})  # Note: do not depend on this key being in the dictionary -- I might decide to not put it in as default
        for key, value in kwargs.items():
            self.update({key: value})

        # if reprstyler is not set to "none",
        if not 'reprstyler_html' in self.__dict__.keys():
            self.update({'reprstyler_html': reprstyler_html})

    def __getattr__(self, attr):
        """ responds to :code:`answer=dict.attribute`"""
        answer = self.get(attr)
        if answer is None:
            # skip warning if jupyter tries to access some typical methods
            if attr not in ('_ipython_canary_method_should_not_exist_',
                            '_ipython_display_',
                            '_repr_mimebundle_',
                            'reprstyler_html',
                            'reprstyler',
                            '_repr_markdown_',
                            '_repr_svg_',
                            '_repr_png_',
                            '_repr_pdf_',
                            '_repr_jpeg_',
                            '_repr_latex_',
                            '_repr_json_',
                            '_repr_javascript_',
                            'is_tensor_like',  # tensorflow uses this to check for tensors
                            ):
                # give meaningful error message:
                warn(f'no key "{attr}" in this dictionary. \nvalid keys are {[key for key in self.keys()]}',
                     stacklevel=2)
                warn('in ', stacklevel=3)
                warn('in ', stacklevel=4)
                # attempt to continue by returning None:
        return self.get(attr)

    def __setattr__(self, key, value):
        """ responds to :code:`dict.key=value` """
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        """ responds to :code:`dict['key']=value` """
        super(mict, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        """ ? I don't know what this does."""
        self.__delitem__(item)

    def __delitem__(self, key):
        """ ? I don't know what this does."""
        super(mict, self).__delitem__(key)
        del self.__dict__[key]

    def __repr__(self):
        """
        If available, calls the reprstyler. If not available,just calls the default __repr__()
        """
        if self.reprstyler is not None:
            try:
                return self.reprstyler(self)
            except Exception as E:
                print(E)
                print('-- falling back to super...')
                return super(mict, self).__repr__()
        else:  # if reprstyler not set
            return super(mict, self).__repr__()

    def __str__(self):
        """just wrap to self.__repr__()"""
        return self.__repr__()

    def _repr_html_(self):
        if self.reprstyler_html is not None:
            try:
                return self.reprstyler_html(self)
            except Exception as reprstyler_html_fail:
                print(reprstyler_html_fail)
                print('-- falling back to super.__repr__() --')
                return super(mict, self).__repr__()  # note that dict has no _repr_html_() to call.
        else:  # if reprstyler_html not set
            # at this point, if reprstyler is set, use it. Otherwise it will fall back too early and all Jupyter output would be bad.
            if self.reprstyler is not None:
                try:
                    return self.reprstyler(self)
                except Exception as reprstyler_fail:
                    print(reprstyler_fail)
                    print('-- falling back to super...')
                    return super(mict, self).__repr__()
            else:  # if reprstyler not set
                return super(mict, self).__repr__()

    # turns out that these two methods are essential to enable pickling of this object
    #  https://stackoverflow.com/questions/2049849/why-cant-i-pickle-this-object
    def __getstate__(self):
        """This is used by pickle and other serializers.
        :return: `self.__dict__`
        """
        return self.__dict__

    def __setstate__(self, data):
        """This is used by pickle when deserializing an object."""
        self.__dict__.update(data)

    def to_pickle(self, filename):
        """ Save the contents of this object to a file using pickle.

        :param filename: file name to attempt to write to. Overwritten if already exists.
        :return: True on success.
        """
        import pickle
        with open(filename, 'wb') as file_output:
            pickle.dump(self, file_output)
        return True

    @staticmethod
    def from_pickle(filename):
        """ load something from file using pickle.
        note that this DOES NOT check what exactly gets loaded with pickle -- it just returns whatever was there in the pickle file.

        :param filename: file name to load
        :return: whatever pickle thinks that was there under file name provided.
        """
        import pickle
        with open(filename, 'rb') as file_input:
            data = pickle.load(file_input)
        return data

    @staticmethod
    def from_locals(reprstyler_html=reprstyler_basic_html):
        """generates a mdict from local variables.

        Primary use is intended to be a return type from functions.

        uses `reprstyler_basic_html` as the default reprstyler

        ### Example
        ```python

        # define a function
        def do_maths(x=1,y=2):
            a=x+y
            b=a*x
            c=b*y
            result = mict.from_locals()  # puts `a`,`b`,`c` into `result`
            return result

        demo_result = do_maths(x=1,y=2)
        demo_result
        ```

        """
        import inspect
        import types
        local_list = inspect.currentframe().f_back.f_locals
        skip_list = ['In', 'Out', 'get_ipython', 'exit', 'quit', 'inspect']
        result = mict()
        for item in local_list:
            if not item[0] == '_':
                if not item in skip_list:
                    value = inspect.currentframe().f_back.f_locals[item]
                    if isinstance(value, types.FunctionType):
                        # print(f'function: {item}')
                        pass
                    elif isinstance(value, types.ModuleType):
                        # print(f'module: {item}')
                        pass
                    else:
                        # print(f'var: {item} = {value}')
                        result.update({item: value})

        # set the reprstyler
        result.reprstyler_html = reprstyler_basic_html
        return result




