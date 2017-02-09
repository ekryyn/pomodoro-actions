from setuptools import setup, find_packages


setup(
    name='gnome-pomodoro-tracker',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['tinydb', 'click'],
    entry_points=open('entrypoints.ini').read(),
)
