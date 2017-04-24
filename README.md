# Typeform To CSV
Simple little Typeform-to-CSV parser

## Getting Started:
It's as easy as 1, 2 ,3!

1. Clone the repo
```
$ git clone https://github/eyyu/TypeformToCSV.git
```
2. Go to Main.py and insert the typeform API key in line 25
3. Run the script!
```
$ ./Main.py
```  
## Troubleshooting:

#### Python3 Command Not Found
The script will default to running on Python 3, if you are running Python 2,
run the following instead:
```
$ python ./Main.py
```

#### ImportError: No module named requests
You are missing the requests module. Install it with
```
$ pip install requests
```
or, for Python 3:
```
$ pip3 install requests
```

#### Can't Run the Program?
You might not have permissions! Try:
```
$ chmod 755 Main.py
```


## To-Do:
- Add API key prompt
- Data validation
- Ensure Python 2.7 compatibility
- Cross Compatibility tests: Windows
