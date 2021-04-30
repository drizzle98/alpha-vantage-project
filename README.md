# alpha-vantage-project

![GitHub watchers](https://img.shields.io/github/watchers/drizzle98/alpha-vantage-project?style=social) ![GitHub Repo stars](https://img.shields.io/github/stars/drizzle98/alpha-vantage-project?style=social) ![GitHub forks](https://img.shields.io/github/forks/drizzle98/alpha-vantage-project?style=social)

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=flat-square&logo=Jupyter)](https://jupyter.org/try) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square)](https://www.python.org/) ![repo size](https://img.shields.io/github/repo-size/drizzle98/alpha-vantage-project?style=flat-square)


We are aimed to create a simple and practical tool for beginners to check stock. The goal is to find patterns in this time-series financial dataset, and make it easier for our viewers to query and compare stock market data. 

### Modify REQUIRED in several scripts!!!
In app.py,update_stock.py modify the sql_engine configurations and alpha_vantage API keys

### MySQL required in your system!!! And make sure it is active!!!

### Usage

```bash
git clone https://github.com/drizzle98/alpha-vantage-project
```
Go to your cloned directory
```bash
cd ../github/alpha-vantage-project
```
Install the required packages
```bash
pip install -r requirements.txt
```

```bash
export FLASK_APP=app.py
```
```bash
export FLASK_ENV=development
```
```bash
flask run
```
Enter the following host into your browser
```
http://0.0.0.0:3000/
```
