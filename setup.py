import setuptools
setuptools.setup(
    name='mict',  # it seems that doing that in setup.cfg doesn't work for me
    version='0.0.37',
)


def get_version():
    """
    try using `git rev-parse HEAD --short` here to get the git commit.

    """
    return '0.0.37'
