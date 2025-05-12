
# pyangi

# pyangi: python dasturchilari uchun kichik wsgi aplication

![Purpose](https://img.shields.io/badge/purpose-learning-green)
[![PyPI](https://img.shields.io/pypi/v/pyangi)](https://pypi.org/project/pyangi/)



pyangi amaliyot uchun qilingan gunicorn bilan run qilinadi 

## installation
```shell
   pip install pyangi
```

## How to use it
Basic usage
```python
from pyangi.app import Pyangi

app = Pyangi()


@app.route("/home")
def home(request, response):
    response.text = "hello from home page"



@app.route("/about")
def about(request, response):
    response.text = "hello from about page"

@app.route("/home/{name}")
def greetings(request, response, name):
    response.text = f"hello my friend {name}"

@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "this method get"

    def post(self, request, response):
        response.text = "Endpoint to create books"

```



>>>>>>> 5c5c8e2 (initial commit)
