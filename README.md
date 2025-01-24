# rho examples

This repository contains example projects and demos for the Rho platform. The examples demonstrate different use cases or features, providing inspiration and guidance. 

For mor information about Rho, please visit [the webpage](https://rho.store) or the [documentation](https://docs.rho.store).

## running the examples
Start by cloning this repository and installing the dependencies:

```bash
git clone https://github.com/rho-store/rho-examples.git
cd rho-examples
```

We recommend using UV-package to manage your python environment. To install it, run:

```bash
pip install uv
```

Then, create a virtual environment and activate it:
```bash
uv venv
source venv/bin/activate
```

Install the dependencies:

```bash 
uv pip install -r requirements.txt
```

The select which example you want to run. 

### weatherapp
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rho-weatherapp.streamlit.app/)

A small demo app that demonstrates using rho as a simple backend for a streamlit app. 

run: 
```bash
streamlit run weatherapp/app.py
```
