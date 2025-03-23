# PyPico8

<style>
    .badge {
        color: #fff;
        font-family: Verdana, Geneva, DejaVu Sans, sans-serif;
        font-size: 11px;
        margin-bottom: 100px;
        padding: 2px 5px 3px 5px;
        text-align: middle;
        text-shadow: #1116 0px 1px;
    }

    .badge.name {
        background: linear-gradient(#666 0%, #333 100%);
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
    }

    .badge.value {
        background-color: grey;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }

    .badge.err {
        background-color: red;
    }

    .badge.ok {
        background-color: #97ca00;
    }

    .badge.warn {
        background-color: #fe7d37;
    }
</style>
<span class="badge">
    <span class="badge name">license</span><span class="badge value ok">MIT</span>
</span>
<span class="badge">
    <span class="badge name">coverage</span><span class="badge value ok">99%</span>
</span><br><br>

Run [PICO-8](https://www.lexaloffle.com/pico-8.php) demos in Python.

## Install on Windows

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

The src folder contains demos ported from Twitter/X etc.

## Use

```cmd
.venv\Scripts\activate
python src\snek.py
```
