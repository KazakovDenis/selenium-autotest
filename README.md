# Test task 
My test task for the vacancy of the **tester programmer**, which I passed in November 2019

## How to install
Create a virtual enviroment:
 ```sh
$ mkdir testtask
$ cd testtask
$ python3 -m venv venv
```
Clone this repository:
 ```sh
$ git clone https://github.com/KazakovDenis/TestTask1-Selenium
```
Install dependencies from requirements.txt (**used**: Selenium, Pytest):
 ```sh
$ pip install -r requirements.txt
```
Close Chrome Browser if you use it, download [Chrome driver][cd] and put it into /static directory.

## How to start tests:
*The 'headless' mode is commented to make tests visual.*

* To start tests use as follows:
 ```sh
$ pytest -vv test_tensor.py
```
* Wait for the script to complete
* Check out the result in the terminal and the file 'app.log'


   [cd]: <https://chromedriver.chromium.org/downloads>
