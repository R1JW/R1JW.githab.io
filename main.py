from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse, JSONResponse
from scipy.integrate import odeint

app = FastAPI()

# Функция, выражающая систему уравнений
def system_equations(u, t, c):
    [p0_t, p1_t, p2_t, p3_t, p4_t, p5_t, p6_t, p7_t, p8_t, p9_t, p10_t, p11_t, p12_t, p13_t, p14_t, p15_t] = u

    dp0_dt = (
        - p0_t * (c['l1'] + c['l2'] + c['l3'] + c['l4'])
        + c['u1'] * p1_t
        + c['u2'] * p2_t
        + c['u3'] * p3_t
        + c['u4'] * p4_t
    )

    dp1_dt = (
        - p1_t * (c['u1'] + c['l2'] + c['l3'] + c['l4'])
        + c['l1'] * p0_t
        + c['u2'] * p5_t
        + c['u3'] * p6_t
        + c['u4'] * p7_t
    )

    dp2_dt = (
        - p2_t * (c['u2'] + c['l1'] + c['l3'] + c['l4'])
        + c['l2'] * p0_t
        + c['u1'] * p5_t
        + c['u3'] * p8_t
        + c['u4'] * p9_t
    )

    dp3_dt = (
        - p3_t * (c['u3'] + c['l1'] + c['l2'] + c['l4'])
        + c['l3'] * p0_t
        + c['u1'] * p6_t
        + c['u2'] * p8_t
        + c['u4'] * p10_t
    )

    dp4_dt = (
        - p4_t * (c['u4'] + c['l1'] + c['l2'] + c['l3'])
        + c['l4'] * p0_t
        + c['u1'] * p7_t
        + c['u2'] * p9_t
        + c['u3'] * p10_t
    )

    dp5_dt = (
        - p5_t * (c['u2'] + c['u1'] + c['l3'] + c['l4'])
        + c['l2'] * p1_t
        + c['l1'] * p2_t
        + c['u4'] * p12_t
        + c['u3'] * p11_t
    )

    dp6_dt = (
        - p6_t * (c['u3'] + c['u1'] + c['l2'] + c['l4'])
        + c['l3'] * p1_t
        + c['l1'] * p3_t
        + c['u2'] * p11_t
        + c['u4'] * p13_t
    )

    dp7_dt = (
        - p7_t * (c['u4'] + c['u1'] + c['l2'] + c['l3'])
        + c['l4'] * p1_t
        + c['l1'] * p4_t
        + c['u2'] * p12_t
        + c['u3'] * p13_t
    )

    dp8_dt = (
        - p8_t * (c['u3'] + c['u2'] + c['l1'] + c['l4'])
        + c['l3'] * p2_t
        + c['l2'] * p3_t
        + c['u1'] * p11_t
        + c['u4'] * p14_t
    )

    dp9_dt = (
        - p9_t * (c['u2'] + c['u4'] + c['l3'] + c['l1'])
        + c['l2'] * p4_t
        + c['l4'] * p2_t
        + c['u3'] * p14_t
        + c['u1'] * p12_t
    )

    dp10_dt = (
        - p10_t * (c['u3'] + c['u4'] + c['l1'] + c['l2'])
        + c['l3'] * p4_t
        + c['l4'] * p3_t
        + c['u1'] * p13_t
        + c['u2'] * p14_t
    )

    dp11_dt = (
        - p11_t * (c['u3'] + c['u2'] + c['u1'] + c['l4'])
        + c['l3'] * p5_t
        + c['l2'] * p6_t
        + c['l1'] * p8_t
        + c['u4'] * p15_t
    )

    dp12_dt = (
        - p12_t * (c['u4'] + c['u2'] + c['u1'] + c['l3'])
        + c['l4'] * p5_t
        + c['l2'] * p7_t
        + c['l1'] * p9_t
        + c['u3'] * p15_t
    )

    dp13_dt = (
        - p13_t * (c['u4'] + c['u3'] + c['u1'] + c['l2'])
        + c['l4'] * p6_t
        + c['l3'] * p7_t
        + c['l1'] * p10_t
        + c['u2'] * p15_t
    )

    dp14_dt = (
        - p14_t * (c['u4'] + c['u3'] + c['u2'] + c['l1'])
        + c['l4'] * p8_t
        + c['l3'] * p9_t
        + c['l2'] * p10_t
        + c['u1'] * p15_t
    )

    dp15_dt = (
        - p15_t * (c['u4'] + c['u3'] + c['u2'] + c['u1'])
        + c['l1'] * p14_t
        + c['l2'] * p13_t
        + c['l3'] * p12_t
        + c['l4'] * p11_t
    )

    return [dp0_dt, dp1_dt, dp2_dt, dp3_dt, dp4_dt, dp5_dt, dp6_dt, dp7_dt, dp8_dt, dp9_dt, dp10_dt, dp11_dt, dp12_dt, dp13_dt, dp14_dt, dp15_dt]

# Маршрут для отображения HTML-страницы
@app.get("/lab4")
async def main4():
    return FileResponse("web/web-4.html")

# Маршрут для выполнения расчетов
@app.post("/api/lab4/calculate")
async def calculate(data = Body()):
    try:
        t0 = data['p0']
        t_end = data['t']
        dt = t_end / 20
        t_span = [round(i * dt, 2) for i in range(21)]
        t_span.append(t_end)

        c = data['c']

        solution, info = odeint(system_equations, list(t0.values()), t_span, args=(c,), full_output=True)

        if info["message"] != "Integration successful.":
            raise HTTPException(status_code=500)

        solution_list = [list(elem) for elem in solution]

        return JSONResponse(content={"solution": solution_list, "time": t_span})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))