import pytest
import tkinter


@pytest.fixture(scope="session")
def root_window() -> tkinter.Tk:
    root = tkinter.Tk()
    root.title("pytwain testing")
    return root
