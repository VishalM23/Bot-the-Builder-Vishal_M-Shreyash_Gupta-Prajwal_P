import os
import sys
import winsound
import subprocess
import collections
import tkinter as tk
import tkinter.tix as tix


class TkCapException(Exception):
    '''
    tkcap raise this exception if pyautogui module was not found installed
    or master parameter in CAP class is not an instance of tkinter.Tk,
    or tkinter.TopLevel or tkinter.tix.Tk or tkinter.tix.Toplevel or if
    pyautogui module is found not installed.
    '''

    pass


class ExtensionError(TkCapException):
    '''
    This exception is raised by tkcap when the extension provided by user
    is invalid.
        VALID_EXTENSION = ['tif', 'tiff', 'jpg', 'png', 'jpeg', 'jpe',
                           'jfif', 'bmp', 'dib', 'gif']
    '''

    pass


class PathNotFoundError(TkCapException):
    '''
    This exception is raised when the user provides invalid path.
    '''

    pass


class ImageNameExistsError(TkCapException):
    '''
    This exception is raised when the user provides the name of image
    that already exists in the same directory.
    '''

    pass

if sys.version_info.major < 3:
    raise TkCapException('tkcap supports Python 3+')

try:
    import pyautogui

except ModuleNotFoundError:
    raise TkCapException('tkcap is unable to import pyautogui. Please install pyautogui to use tkcap')


Region = collections.namedtuple('Region', 'x y width height')


class CAP:
    def __init__(self, master):
        if isinstance(master, (tk.Tk, tk.Toplevel, tix.Tk, tix.Toplevel)):
            self.master = master
            self.wav_path = os.path.join(os.path.dirname(__file__), 'data', 'shutter.wav')
            self.VALID_EXTENSION = ['tif', 'tiff', 'jpg', 'png', 'jpeg', 'jpe', 'jfif', 'bmp', 'dib', 'gif']

        else:
            raise TkCapException('master parameter was expected to be the instance of tkinter')

    def get_region(self):
        '''Gets x-coordinate, y-coordinate, width and height of the tkinter window'''

        self.master.update()

        x_pos, y_pos = self.master.winfo_x() + 8, self.master.winfo_y() + 2
        width, height = self.master.winfo_width(), self.master.winfo_height() + 29

        return Region(x_pos, y_pos, width, height)

    def capture(self, imageFilename, overwrite=False):
        '''Capture and save screenshot of the tkinter window'''

        path = os.path.abspath(os.path.join('.', imageFilename))
        head, tail = os.path.split(path)
        extension = tail.split('.')[-1]

        if not os.path.exists(head):
            raise PathNotFoundError(f'The system cannot find path: {head}')

        elif extension not in self.VALID_EXTENSION:
            if '.' in tail:
                extension = '.' + extension

            else:  # If extension is not provided by the user.
                extension = ''

            raise ExtensionError(f'unknown file extension: {extension}')

        elif os.path.exists(path) and overwrite is False:
            raise ImageNameExistsError(f'Cannot store image having same name: {tail}')

        if overwrite:
            os.remove(path)

        # winsound.PlaySound(self.wav_path, winsound.SND_ASYNC)

        pyautogui.screenshot(path, region=self.get_region())

        # self.master.after(1100, lambda: subprocess.run([os.path.join(os.getenv('WINDIR'), 'explorer.exe'), '/select,', os.path.normpath(path)]))