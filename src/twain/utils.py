import platform


def is_windows():
    """
    Returns true if running on Windows
    """
    return platform.system() == 'Windows'
