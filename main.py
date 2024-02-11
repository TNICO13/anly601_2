#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: EJones
@Course: ANLY601 - Week 3
"""

import requests, json
import pandas as pd
import numpy as np
import six
from google.cloud import translate_v2 as translate
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.messagebox import showinfo, showwarning


class TranslateGUI:
    def __init__(self, guiWin):
        self.guiWin_ = guiWin
        self.guiWin_.title("Translate")
        self.guiWin_.geometry("780x540")

        # Declares root canvas is a grid of only one row and one column
        self.guiWin_.columnconfigure(0, weight=1)
        self.guiWin_.rowconfigure(0, weight=1)

        # Set styles for TK Label, Entry and Button Widgets
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 20), foreground='maroon')
        self.style.configure("TEntry", font=("Arial", 25), foreground='maroon')
        self.style.configure("TCheckbutton", font=("Arial", 20),
                             foreground='maroon')
        self.style.configure("TButton", font=("Arial", 20), foreground='maroon')

        # Create Frame inside GUI canvas
        self.mainframe = ttk.Frame(self.guiWin_, padding="5 15 5 15")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Label(self.mainframe, text="Short Translation", style='TLabel'). \
            grid(column=1, row=1, sticky=W)
        self.left_frame1 = ttk.Frame(self.mainframe, padding=(5, 5, 5, 5),
                                     relief='sunken', borderwidth=5)
        self.left_frame1.grid(column=1, columnspan=1, row=2, rowspan=5,
                              sticky=(N, W, E, S))

        self.written_txt = StringVar()
        self.written_entry = ttk.Entry(self.left_frame1, width=45,
                                       justify=LEFT, textvariable=self.written_txt,
                                       font=("Arial", 20))
        self.written_entry.grid(column=1, row=1, columnspan=3, rowspan=3,
                                sticky=(N, W, E, S))

        ttk.Button(self.left_frame1, text="Translate", cursor="hand2",
                   width=15, style='TButton', command=self.read_written_text). \
            grid(column=1, row=5, padx=5, sticky=E)

        ttk.Button(self.left_frame1, text="Clear", cursor="hand2",
                   width=10, style='TButton', command=self.clear_text). \
            grid(column=2, row=5, padx=5, sticky=E)

        ttk.Label(self.mainframe, text="Translation Language", style='TLabel'). \
            grid(column=2, row=1, sticky=W)

        self.right_frame = ttk.Frame(self.mainframe, padding=(5, 5, 5, 5),
                                     relief='sunken', borderwidth=5)
        self.right_frame.grid(column=2, columnspan=1, row=2, rowspan=5,
                              sticky=(N, W, E, S))

        language = ["English", "Spanish", "German", "Chinese"]
        # ISO 639-1 Language Codes
        # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes#ES
        self.langs = ["en", "es", "de", "zh"]

        self.l1 = IntVar()
        self.l1.set(0)
        self.lt1 = ttk.Checkbutton(self.right_frame, text=language[0],
                                   variable=self.l1, command=self.lang1,
                                   onvalue=1, offvalue=0). \
            grid(column=1, row=1, sticky=W)

        self.lang1()  # By default set target to English

        # Create Text Widget
        self.t = Text(self.mainframe, relief='sunken', wrap='word', width=40,
                      height=7, bg='maroon', fg='white', font=('Arial', 25))
        self.t.grid(column=1, columnspan=2, row=10, rowspan=1,
                    ipadx=5, padx=5, ipady=10, pady=10, sticky=(N, W, E, S))
        ys = ttk.Scrollbar(root, orient='vertical', command=self.t.yview)
        xs = ttk.Scrollbar(root, orient='horizontal', command=self.t.xview)
        self.t['yscrollcommand'] = ys.set
        self.t['xscrollcommand'] = xs.set

    def lang_translate(self):
        """Translates text into the target language.

        Target language must be an ISO 639-1 language code.
        See https://g.co/cloud/translate/v2/translate-reference#supported_languages
        """
        # Basic Translate
        translate_client = translate.Client()

        if isinstance(self.input_text, six.binary_type):
            self.input_text = self.input_text.decode("utf-8")

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
        result = translate_client.translate(self.input_text,
                                            target_language=self.target)

        print("Text: {}".format(result["input"]))
        self.translation = result["translatedText"]
        print("Translation: {}".format(result["translatedText"]))
        print("Detected source language: {}".format(result["detectedSourceLanguage"]))

        # self.t.insert(1.0, "Change this to the translated text")
        self.t.delete(1.0, "end")
        self.t.insert(1.0, self.translation)

    def lang_clear(self):
        self.l1.set(0)

    def lang1(self):
        self.lang_clear()
        self.l1.set(1)
        self.target = self.langs[0]

    def exit_app(self):
        self.guiWin_.destroy()

    def read_written_text(self):
        # Translate the text in the short entry box.
        # First ensure the box contains text
        print("\nRead Input Text for Translation")
        self.input_text = self.written_txt.get()
        # Check to ensure a target language was selected.
        if self.target == "":
            showinfo(title="Warning", message="Select Target Language")
        else:
            self.lang_translate()

    def clear_text(self):
        null


root = Tk()
my_app = TranslateGUI(root)
# Display GUI
root.mainloop()