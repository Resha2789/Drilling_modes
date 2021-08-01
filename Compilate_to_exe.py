import PyInstaller.__main__
import shutil

def install(name='Name'):

    src_data = f"D:\Programming\Python\Drilling_modes\Нужное"
    dst_data = f"Z:\Ракета\Нужное_2"
    try:
        shutil.rmtree(dst_data)
    except FileNotFoundError:
        print('Файл не найден!')

    shutil.copytree(src_data, dst_data, ignore=shutil.ignore_patterns('*.pyc', 'tmp*'))

    PyInstaller.__main__.run([
        "Main.py",
        "--noconsole",
        "--onefile",
        f"--icon=D:\Programming\Python\Drilling_modes\Нужное\\favicon_96.ico",
        f"--distpath=Z:\Ракета\\",
        f"-n={name}"
    ])

if __name__ == '__main__':
    install(name='Ракета')
