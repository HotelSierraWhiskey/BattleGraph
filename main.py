from qtstrap import *
from main_window import MainWindow


def main():
    app = BaseApplication(['Battlegraph'])
    window = MainWindow()

    window.main_menu.file_submenu.quit_application.connect(app.quit)

    set_font_options(window, {'setPointSize': 12})
    window.setMinimumSize(400, 300)

    window.show() 
    app.exec_() 


if __name__ == "__main__":
    main()