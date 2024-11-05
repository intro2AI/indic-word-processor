#pyrcc5 test.qrc -o test_rc.py
#to make exe:
#pyinstaller.exe wordprocessor.spec  -- and then paste aksharmukha the folder
#pyinstaller.exe --onefile --windowed wordprocessor.py


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtGui,QtCore,QtWidgets
from aksharamukha import transliterate
import typing
import re

from utils.custom_textedit import *
from utils.rare_char_window import *

from docx import Document

from PyQt5.QtWidgets import QFileDialog
import os
import sys

# C:/Users/Kartik/miniconda3/envs/word_processor_new/python.exe c:/Users/Kartik/Desktop/word_processor/v8_08162024/wordprocessor.py
#import the images resource file
import test_rc

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

FONT_SIZES = [18, 36, 48, 64, 72, 96, 144, 288]
HTML_EXTENSIONS = ['.htm', '.html']

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None
        self.current_font_size =18
        self.transliteration_scheme = "ITRANS"
        self.radio_button_pressed = ''


        layout = QGridLayout()
        

        #ALL KEYS DISPLAY LABEL:
        self.label_trackAllKeys = QLabel("") #not displayed
        self.transliterated_text = QTextEdit("")
        self.transliterated_text.setFixedHeight(100)  # Set a fixed height for the transliterated text area
        self.transliterated_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        #initialize trransliterated text box
        _font = QFont('Sitika')
        _font.setPointSize(18)
        self.transliterated_text.setFont(_font)
        
        #initialize the main text box
        self.editor = TextEdit(self.label_trackAllKeys)
        _font = QFont('Shobhika')
        _font.setPointSize(18)
        self.editor.setFont(_font)
        
        # Setup the QTextEdit editor configuration
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.update_format)

        # showing on fonts of the selected script
        qfontdb = QFontDatabase()
        self.devanagari_fonts = QtGui.QFontDatabase.families(qfontdb, writingSystem=QFontDatabase.Devanagari)
        self.devanagari_fonts.append('Shobhika')
        #self.devanagari_fonts.append('Shobhika-Bold')
        self.vedic_fonts = ['Shobhika']
        self.latin_fonts = QtGui.QFontDatabase.families(qfontdb, writingSystem = QFontDatabase.Latin) 
        self.symbol_fonts = ['Ida-Left-To-Right'] #QtGui.QFontDatabase.families(qfontdb, writingSystem = QFontDatabase.Symbol)
        self.manipuri_fonts = ['NotoSansMeeteiMayek-Bold']
        
    
        # Adding the buttons
        self.sanskrit_button = QRadioButton('संस्कृत  ')
        self.sanskrit_button.setFont(QFont("Mangal", 10))  # Increase font size to 14
        self.sanskrit_button.clicked.connect(self.on_sanskrit_button_clicked)

        self.marathi_button = QRadioButton('मराठी  ')
        self.marathi_button.setFont(QFont("Mangal", 10))  # Increase font size to 14
        self.marathi_button.clicked.connect(self.on_marathi_button_clicked)

        self.hindi_button = QRadioButton('हिंदी  ')
        self.hindi_button.setFont(QFont("Mangal", 10))  # Increase font size to 14
        self.hindi_button.clicked.connect(self.on_hindi_button_clicked)

        self.english_button = QRadioButton('English  ')
        self.english_button.setFont(QFont("Mangal", 10))  # Increase font size to 14
        self.english_button.clicked.connect(self.on_english_button_clicked)

        self.vedic_button = QRadioButton('वैदिक  ')
        self.vedic_button.setFont(QFont("Mangal", 10))  # Increase font size to 14
        self.vedic_button.clicked.connect(self.on_vedic_button_clicked)

        self.indus_button = QRadioButton('Indus (testing)')
        self.indus_button.setFont(QFont("Mangal", 10))  # Increase font size to 14
        self.indus_button.clicked.connect(self.on_indus_button_clicked)

        self.manipuri_button = QRadioButton("Meity")
        self.manipuri_button.setFont(QFont("NotoSansMeeteiMayek-Bold", 10))  # Increase font size to 14
        self.manipuri_button.clicked.connect(self.on_manipuri_button_clicked)



                 # Create the combobox
        self.combobox = QComboBox(self)   
        # Add items to the combobox
        self.combobox.addItem("ITRANS")
        self.combobox.addItem("IAST")
        self.combobox.addItem("ISO")
        self.combobox.addItem("SLP1")
        self.combobox.addItem("Velthuis")
        # Connect the selection change event to a function
        self.combobox.currentIndexChanged.connect(self.selectionChanged)


        # Create a new horizontal layout for the buttons
        top_button_layout = QHBoxLayout()
        # Add the language buttons to the horizontal layout
        top_button_layout.addWidget(self.english_button)
        top_button_layout.addWidget(self.hindi_button)
        top_button_layout.addWidget(self.marathi_button)
        top_button_layout.addWidget(self.sanskrit_button)
        top_button_layout.addWidget(self.vedic_button)
        top_button_layout.addWidget(self.indus_button)
        top_button_layout.addWidget(self.manipuri_button)

        # Add some spacing
        top_button_layout.addStretch(0)
        # Create and add the Vedic Symbols button
        v_button = QPushButton("  Vedic Symbols  ", self)
        v_button.setFont(QFont("Mangal", 10))
        v_button.setGeometry(50, 50, 300, 30)
        v_button.clicked.connect(self.open_vedic_character_window)
        top_button_layout.addWidget(v_button)

        # Create and add the Rare Symbols button
        r_button = QPushButton("  Rare Symbols  ", self)
        r_button.setFont(QFont("Mangal", 10))
        r_button.setGeometry(50, 50, 300, 30)
        r_button.clicked.connect(self.open_rare_character_window)
        top_button_layout.addWidget(r_button)

        # Create a widget to hold the horizontal layout
        top_button_widget = QWidget()
        top_button_widget.setLayout(top_button_layout)

        # Add the widget containing the horizontal layout to the main layout
        layout.addWidget(top_button_widget, 0, 0, 1, 11)

        font__ = QFont()
        font__.setPointSize(11)  # Set the font size to 11 point
        # Create a new horizontal layout
        button_layout = QHBoxLayout()
        transliterate_button = QPushButton("🡇", self)
        transliterate_button.setGeometry(50, 50, 250, 30)
        transliterate_button.clicked.connect(self.transliterate)
        transliterate_button.setFont(font__)  # Set the font for the button
        button_layout.addWidget(transliterate_button)

        reverse_transliterate_button = QPushButton("🡅", self)
        reverse_transliterate_button.setGeometry(50, 50, 250, 30)
        reverse_transliterate_button.clicked.connect(self.reverse_transliterate)
        reverse_transliterate_button.setFont(font__)
        button_layout.addWidget(reverse_transliterate_button)

        button_layout.addWidget(self.combobox)

        font__ = QFont()
        font__.setPointSize(7)  # Set the font size to 11 points
        # Create the "Powered by Aksharamukha" label
        powered_label = QLabel("Powered by Aksharamukha", self)
        powered_label.setFont(font__)  # Use the same font as the buttons
        powered_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Align text to the right
        # Add the powered_label to the button_layout
        button_layout.addWidget(powered_label)
        # Add the button_layout to the main layout
        layout.addLayout(button_layout, 22, 4, 1, 4)


        layout.addWidget(self.editor,2,0,20,11)
        layout.addWidget(self.transliterated_text,23,0,2,11)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Uncomment to disable native menubar on Mac
        # self.menuBar().setNativeMenuBar(False)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join(':/images/blue-folder-open-document.svg')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join(':/images/disk.svg')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join(':/images/disk--pencil.svg')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join(':/images/printer.svg')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join(':/images/arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join(':/images/arrow-curve.svg')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join(':/images/scissors.svg')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join(':/images/document-copy.svg')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join(':/images/clipboard-paste-document-text.svg')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join(':/images/selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join(':/images/arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(30, 30))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts_manager = QFontComboBox()
        self.update_font = lambda font: (print(f"currentFontChanged signal emit lambda function: Font changed to: {font.family()}"), self.setCurrentFont(font))
        self.fonts_manager.currentFontChanged.connect(self.update_font)

        self.fontsize_box = QComboBox()
        self.fontsize_box.addItems([str(s) for s in FONT_SIZES])
        self.fontsize_box.currentIndexChanged[str].connect(lambda s: self.update_font_size(int(s)))
        self.update_font_size(self.current_font_size)

        format_toolbar.addWidget(self.fontsize_box)
        format_toolbar.addWidget(self.fonts_manager)

        self.bold_action = QAction(QIcon(os.path.join(':/images/edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        self.italic_action = QAction(QIcon(os.path.join(':/images/edit-italic.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        self.underline_action = QAction(QIcon(os.path.join(':/images/edit-underline.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        self.alignl_action = QAction(QIcon(os.path.join(':/images/edit-alignment.svg')), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)

        self.alignc_action = QAction(QIcon(os.path.join(':/images/edit-alignment-center.svg')), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        self.alignr_action = QAction(QIcon(os.path.join(':/images/edit-alignment-right.svg')), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)

        self.alignj_action = QAction(QIcon(os.path.join(':/images/edit-alignment-justify.svg')), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        format_menu.addSeparator()

        self.hindi_button.setChecked(True)
        self.on_hindi_button_clicked()



        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts_manager,
            self.fontsize_box,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

        # Initialize.
        self.update_format()
        self.update_title()
        self.show()

    def open_vedic_character_window(self):
        self.special_char_window = VedicCharacterWindow(self.editor)
        self.special_char_window.show()

    def open_rare_character_window(self):
        self.special_char_window = RareCharacterWindow(self.editor)
        self.special_char_window.show()

    def insert_special_character(self, char):
        cursor = self.editor.textCursor()
        cursor.insertText(char)

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is necessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def update_font_size(self, font_size):
        # Convert font_size to integer and store it
        print('updating font size')
        font_size = int(font_size)
        self.current_font_size = font_size

        font = self.editor.document().defaultFont()
        font.setPointSize(font_size)
        self.editor.document().setDefaultFont(font)

    def setCurrentFont(self, font=None):
        print('updating font inside lambda function..')
        # Set the new font as the default for the document
        font.setPointSize(self.current_font_size)
        self.editor.document().setDefaultFont(font)


    def strip_font_styles(self,html_text):
        # Remove font-family and font-size styles from HTML content
        html_text = re.sub(r'font-family:[^;]+;', '', html_text)
        html_text = re.sub(r'font-size:[^;]+;', '', html_text)
        return html_text
    

    def file_open(self):    
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "HTML documents (*.html);Text documents (*.txt);All files (*.*)")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            text = self.strip_font_styles(text)
            self.editor.document().setHtml(text)
            self.update_title()


    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        if self.path and splitext(self.path) in HTML_EXTENSIONS:
            text = self.editor.toHtml()
        else:
            print('saving as plain text')
            text = self.editor.toPlainText()

        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        options = QFileDialog.Options()
        file_filter = "HTML documents (*.html);;Text documents (*.txt);;All files (*.*)"
        default_extension = ".html"  # Set default extension
        
        path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save file", "", file_filter, options=options
        )

        if not path:
            # If dialog is cancelled, will return ''
            return

        if splitext(path) in HTML_EXTENSIONS:  # Use 'path' instead of 'self.path'
            text = self.editor.toHtml()
        else:
            print('saving as plain text')
            text = self.editor.toPlainText()

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - Indic FLAME" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )

    def on_sanskrit_button_clicked(self):
        self.editor.english_bypass =False 
        print("Sanskrit button clicked")
        from mappings.mappings_v1 import C,V,v,misc

        #TODO instead of changing the editor variables, change the editor itself, so that we easily change the rules too!

        self.editor.C = C #consonents
        self.editor.V = V #Independent Vowels
        self.editor.v = v #dependent vowels
        self.editor.misc = misc #nukta, halant, numbers and misc symbols
        
        if self.radio_button_pressed not in ['marathi','hindi','sanskrit']:
            self.fonts_manager.currentFontChanged.disconnect(self.update_font)
            self.fonts_manager.clear()
            self.fonts_manager.addItems(self.devanagari_fonts)
            self.fonts_manager.currentFontChanged.connect(self.update_font)
            self.find_and_select_font('Shobhika')

        self.radio_button_pressed = 'sanskrit'
        self.editor.current_script = 'sanskrit'

        

    def on_marathi_button_clicked(self):
        self.editor.english_bypass =False
        print("Marathi button clicked")
        from mappings.mappings_marathi_v1 import C,V,v,misc
        self.editor.C = C #consonents
        self.editor.V = V #Independent Vowels
        self.editor.v = v #dependent vowels
        self.editor.misc = misc #nukta, halant, numbers and misc symbols

        if self.radio_button_pressed not in ['marathi','hindi','sanskrit']:
            self.fonts_manager.currentFontChanged.disconnect(self.update_font)
            self.fonts_manager.clear()
            self.fonts_manager.addItems(self.devanagari_fonts)
            self.fonts_manager.currentFontChanged.connect(self.update_font)
            self.find_and_select_font('Shobhika')

        self.radio_button_pressed = 'marathi'
        self.editor.current_script = 'marathi'

            
    def on_hindi_button_clicked(self):
        self.editor.english_bypass =False
        print("Hindi button clicked")
        from mappings.mappings_v1 import C,V,v,misc
        self.editor.C = C #consonents
        self.editor.V = V #Independent Vowels
        self.editor.v = v #dependent vowels
        self.editor.misc = misc #nukta, halant, numbers and misc symbols

        if self.radio_button_pressed not in ['marathi','hindi','sanskrit']:
            self.fonts_manager.currentFontChanged.disconnect(self.update_font)
            self.fonts_manager.clear()
            self.fonts_manager.addItems(self.devanagari_fonts)
            self.fonts_manager.currentFontChanged.connect(self.update_font)
            self.find_and_select_font('Shobhika')

        self.radio_button_pressed = 'hindi'
        self.editor.current_script = 'hindi'

        

    def on_vedic_button_clicked(self):
        self.editor.english_bypass =False
        print("Vedic button clicked")
        from mappings.mappings_v1 import C,V,v,misc
        self.editor.C = C #consonents
        self.editor.V = V #Independent Vowels
        self.editor.v = v #dependent vowels
        self.editor.misc = misc #nukta, halant, numbers and misc symbols
    
        #self.fonts_manager.currentFontChanged.disconnect(self.update_font)
        self.fonts_manager.clear()
        self.fonts_manager.addItems(self.vedic_fonts)
        #self.fonts_manager.currentFontChanged.connect(self.update_font)
        self.find_and_select_font('Shobhika')

        self.radio_button_pressed = 'vedic'
        self.editor.current_script = 'vedic'
        


    def on_english_button_clicked(self):
        self.editor.english_bypass =True
        print("English button clicked")

        self.fonts_manager.currentFontChanged.disconnect(self.update_font)
        self.fonts_manager.clear()
        self.fonts_manager.addItems(self.latin_fonts)
        self.fonts_manager.currentFontChanged.connect(self.update_font)
        self.find_and_select_font('Verdana')

        self.radio_button_pressed = 'english'
        self.editor.current_script = 'english'

        


    def on_indus_button_clicked(self):
        self.editor.english_bypass =False
        print("Indus button clicked")
        from mappings.mappings_indus import C,V,v,misc
        self.editor.C = C #consonents
        self.editor.V = V #Independent Vowels
        self.editor.v = v #dependent vowels
        self.editor.misc = misc #nukta, halant, numbers and misc symbols

        

        #self.fonts_manager.currentFontChanged.disconnect(self.update_font)
        self.fonts_manager.clear()
        self.fonts_manager.addItems(self.symbol_fonts)
        #self.fonts_manager.currentFontChanged.connect(self.update_font)
        self.find_and_select_font('Ida-Left-To-Right')

        self.radio_button_pressed = 'indus'
        self.editor.current_script = 'indus'


    def on_manipuri_button_clicked(self):
        self.editor.english_bypass =False
        print("Manipuri button clicked")
        from mappings.mappings_manipuri import C,V,v,misc
        self.editor.C = C #consonents
        self.editor.V = V #Independent Vowels
        self.editor.v = v #dependent vowels
        self.editor.misc = misc #nukta, halant, numbers and misc symbols


        self.fonts_manager.currentFontChanged.disconnect(self.update_font)
        self.fonts_manager.clear()
        self.fonts_manager.addItems(self.manipuri_fonts)
        self.fonts_manager.currentFontChanged.connect(self.update_font)
        
        #TODO why does this work when we first load Nirmala UI first??
        nirmala_font = QFont("Nirmala UI")
        # Find the index of Nirmala in the font combo box
        nirmala_index = self.fonts_manager.findText("Nirmala UI")
        if nirmala_index != -1:
            # If Nirmala is found, set it as the current font
            print('found font nirmala')
            self.fonts_manager.setCurrentIndex(nirmala_index)

        else:
            # If Nirmala is not found in the combo box, we can still emit the signal manually
            print('emitting signal')
            self.fonts_manager.currentFontChanged.emit(nirmala_font)

        self.find_and_select_font('NotoSansMeeteiMayek-Bold')
        
    
        self.radio_button_pressed = 'manipuri'
        self.editor.current_script = 'manipuri'

        
    def find_and_select_font(self, font_name):
        """
        Finds and selects a font in self.fonts_manager.
        
        Args:
        font_name (str): The name of the font to find and select.
        
        Returns:
        bool: True if the font was found and selected, False otherwise.
        """
        # Method 1: Using findText() and setCurrentIndex()
        index = self.fonts_manager.findText(font_name)
        if index >= 0:
            self.fonts_manager.setCurrentIndex(index)
            print(f"Font '{font_name}' found and selected.")
            return True
        
        # Method 2: Using setCurrentText()
        # This will select the font if it exists, or do nothing if it doesn't
        current_text = self.fonts_manager.currentText()
        self.fonts_manager.setCurrentText(font_name)
        
        # Check if the font was actually selected
        if self.fonts_manager.currentText() != current_text:
            print(f"Font '{font_name}' found and selected METHOD 2.")
            return True
        
        # If we get here, the font was not found
        print(f"Font '{font_name}' not found in the font manager.")
        return False
    
    def transliterate(self): 
        transliterated_text = transliterate.process('Devanagari', self.transliteration_scheme, self.editor.toPlainText())
        print(transliterated_text)
        self.transliterated_text.setText(transliterated_text)


    def reverse_transliterate(self): 
        _text = transliterate.process(self.transliteration_scheme,'Devanagari', self.transliterated_text.toPlainText())
        self.label_trackAllKeys.setText('   ')#str
        self.makeNextVowelDependent = False
        self.use2CharsVowelNext = True
        self.editor.setText(_text)
        # Display transliterated text

    def selectionChanged(self, index):
        previous_scheme = self.transliteration_scheme
        self.transliteration_scheme = self.combobox.currentText()
        if previous_scheme!=self.transliteration_scheme:
            transliterated_text = transliterate.process(previous_scheme, self.transliteration_scheme, self.transliterated_text.toPlainText())
            self.transliterated_text.setText(transliterated_text)

        print(f"Selected option: {self.combobox.currentText()} at index {index}")

    def set_system_style(self):
        # Get the application instance
        app = QApplication.instance()

        # Set the style to match the system
        app.setStyle("Fusion")

        # Enable automatic palette colors based on the system theme
        app.setAttribute(Qt.AA_UseHighDpiPixmaps)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)

        # Get the system palette
        palette = app.palette()

        # Apply the system palette to the application
        app.setPalette(palette)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Alt:
    #         event.ignore()  # Ignore Alt key press


    # def keyReleaseEvent(self, event):
    #     if event.key() == Qt.Key_Alt:
    #         event.ignore()  # Ignore Alt key release


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(':/images/logo.png')))


    _id = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/mangal.ttf"))
    _id1 = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/Shobhika-Bold.otf"))
    _id2 = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/Shobhika-Regular.otf"))
    _id3 = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/ida-left-to-right-pre-release-0-9-1.otf"))
    _id4 = QtGui.QFontDatabase.addApplicationFont(resource_path("fonts/NotoSansMeeteiMayek-Bold.ttf"))

    print(resource_path("fonts/mangal.ttf"))
    if _id1 != -1:
        print("Font registered successfully.")
    else:
        print("Failed to register font.")

    print(resource_path("fonts/Shobhika-Bold.otf"))
    if _id2 != -1:
        print("Font registered successfully.")
    else:
        print("Failed to register font.")

    if _id != -1:
        print("Font registered successfully.")
    else:
        print("Failed to register font.")
    
    print(resource_path("fonts/ida-left-to-right-pre-release-0-9-1.otf"))
    if _id3 != -1:
        print("Font registered successfully.")
    else:
        print("Failed to register font.")

    print(resource_path("fonts/NotoSansMeeteiMayek-Bold.ttf"))
    if _id4 != -1:
        print("Font registered successfully.")
    else:
        print("Failed to register font.")

    font_families = QtGui.QFontDatabase().families()
    
    # Print font families along with their writing systems
    for font_family in font_families:
        writing_systems = QFontDatabase().writingSystems(font_family)
        print(f"Font Family: {font_family}, Writing Systems: {writing_systems}")
    

    app.setApplicationName("Indic FLAME")

    window = MainWindow()
    window.resize(1080, 720)
    app.exec_()