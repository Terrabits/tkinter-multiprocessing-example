# TKInter Multiprocessing Example

This is a simple example of a python application with a `tkinter` GUI in a main process that spawns a "worker" process. The worker process periodically communicates with the main process via a `multiprocess.Queue`. `multiprocess.Value` is used as well for setting a bool value that indicates whether or not the second process should stop.

## Requirements

- Python 3 (for `tkinter.scrolledtext` reference)

## Issues

I noticed that text and certain features would sometimes be missing from the GUI on my system (MacOS Mojave 10.14.2, Python 3.7.0 installed via `pyenv`). Sometimes resizing the window solved the problem; sometimes it did not.

I am not the only one:

[Stack Overflow - button text of tkinter not works in mojave](https://stackoverflow.com/questions/52529403/button-text-of-tkinter-not-works-in-mojave)
