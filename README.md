# PyPico8

Run [PICO-8](https://www.lexaloffle.com/pico-8.php) demos in Python.

## Install

(On Windows)

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install .
```

The activate line is different in Bash etc: `source .venv/bin/activate`

For development, also `pip install .[dev]`

## Use

The src folder contains demos ported from Twitter/X etc.

(On Windows)

```cmd
.venv\Scripts\activate
python src\snek.py
```
