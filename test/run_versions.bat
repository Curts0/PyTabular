@echo on
pyenv shell 3.8.9 & python3 -m pytest &
pyenv shell 3.9.13 & python3 -m pytest &
pyenv shell 3.10.6 & python3 -m pytest &
pyenv shell 3.11.9 & python3 -m pytest &
pyenv shell 3.12.6 & python3 -m pytest &
pause & pause