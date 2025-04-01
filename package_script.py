import PyInstaller.__main__

PyInstaller.__main__.run([
    'xiaozi_gui.py',
    '--onefile',
    '--windowed',
    '--name=小紫爱抽卡',
    '--add-data=images/background.png;images',
    '--add-data=images/*.jpg;images',
    '--i=xiaozi.ico'
])
