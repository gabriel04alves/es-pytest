from fastapi import FastAPI, HTTPException, Query

app = FastAPI()


@app.get("/")
def read_root():
    """Endpoint bem simples para manter um exemplo trivial."""
    return {"message": "Hello World!!!"}


@app.get("/square/{x}")
def square(x: int):
    """Retorna o quadrado de um inteiro.

    Rejeita valores muito grandes só para ilustrar erro de validação.
    """

    if abs(x) > 10_000:
        raise HTTPException(status_code=400, detail="x is too large")
    return {"result": x**2}


@app.get("/double/{x}")
def double(x: int, validated: bool = False):
    """Dobra um valor inteiro com uma lógica um pouco mais elaborada.

    - Quando `validated=True`, só aceita valores entre -100 e 100.
    """

    if validated and not (-100 <= x <= 100):
        raise HTTPException(
            status_code=422, detail="x out of allowed range (-100, 100)"
        )

    return {"result": x * 2}


@app.get("/stats/{numbers}")
def stats(numbers: str):
    """Calcula estatísticas simples sobre uma lista de inteiros.

    Exemplo: `/stats/1,2,3`
    """

    try:
        number_list = [int(n.strip()) for n in numbers.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid number format")

    if not number_list:
        raise HTTPException(status_code=400, detail="numbers must not be empty")

    total = sum(number_list)
    count = len(number_list)
    average = total / count

    return {
        "count": count,
        "total": total,
        "average": average,
        "min": min(number_list),
        "max": max(number_list),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
