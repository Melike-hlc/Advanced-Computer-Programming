from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {
        "item_id": item_id
        }

#1.Hello World Example

@app.get("/hello", tags=["Yeni Görevler"])
def hello_world():
    return {"message": "Hello World"}


#2.Square of a Number

@app.get("/square/{number}", tags=["Yeni Görevler"])
def square_number(number: float):
    return {"number": number, "square": number ** 2}


#3.String Length

@app.get("/string-length", tags=["Yeni Görevler"])
def string_length(text: str):
    return {"text": text, "length": len(text)}


#4.Sum of Two Numbers

@app.get("/sum", tags=["Yeni Görevler"])
def sum_of_two_numbers(num1: float, num2: float):
    return {"num1": num1, "num2": num2, "sum": num1 + num2}


#5.Check Prime Number

@app.get("/check-prime/{number}", tags=["Yeni Görevler"])
def check_prime(number: int):
    if number < 2:
        is_prime = False
    else:
        is_prime = True
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                is_prime = False
                break
    return {"number": number, "is_prime": is_prime}