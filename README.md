# alpha-vantage-project


# Modify REQUIRED in several scripts!!!
In app.py,update_stock.py modify the sql_engine configurations and alpha_vantage API keys

# MySQL required in your system!!! And make sure it is active!!!

# Usage

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
