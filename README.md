# ops-toolkit

Small, readable formulas for shop-floor numbers: **hourly cost** and **OEE**.
Plain Python, no dependencies. Each function is a one-line formula you can check by hand.

Pequeñas fórmulas legibles para números de planta: **coste hora** y **OEE**. Python sin dependencias.

> The numbers in the examples are illustrative inputs, not results from any real company.
> Los números de los ejemplos son datos de ejemplo, no resultados de ninguna empresa real.

## What's inside / Qué hay

| File | What it does |
|---|---|
| `ops_toolkit.py` | Formulas + a small command line |
| `test_ops_toolkit.py` | Tests that check the formulas against hand calculations |
| `oee_shifts_example.csv` | Example shift log (3 made-up shifts) |
| `docs/formulas.md` | Every formula with a worked example you can check by hand |
| `docs/index.html` | Static bilingual (EN/ES) calculator page using the same formulas |
| `.github/workflows/ci.yml` | Tests on Python 3.9 and 3.12, plus a CLI smoke test |

## Hourly cost / Coste hora

```
productive hours / month = hours per week x 52 / 12 x productive share x people
hourly cost              = monthly costs / productive hours per month
minimum rate             = hourly cost x (1 + margin)
person or machine cost   = annual cost / useful hours per year
cost per piece           = (person + machine hourly cost) / 60 x cycle time (min)
```

```
python3 ops_toolkit.py cost --monthly-costs 14000 --productive-share 0.65 --rate 110
```

With those example inputs: 112.67 productive hours/month, 124.26 EUR/h break-even, 142.90 EUR/h with a 15% margin, and a rate of 110 is below cost.

Your productive share is yours to measure. Meetings, breaks, admin and travel are not billable time.

## OEE

```
planned production time = shift time - planned stops
run time                = planned production time - unplanned stops
availability            = run time / planned production time
performance             = total pieces / (run time x ideal rate per minute)
quality                 = good pieces / total pieces
OEE                     = availability x performance x quality
```

```
python3 ops_toolkit.py oee oee_shifts_example.csv
```

It prints each shift and the unplanned minutes lost by reason, largest first.

Use a measured ideal rate (time a good cycle with a stopwatch), not the catalogue figure. OEE measures the process, not the operator.

## Calculator page

`docs/index.html` is a single static file with no dependencies. Open it in a browser, or serve the `docs/` folder with GitHub Pages.

## Run the tests

```
python3 -c "import test_ops_toolkit as t; [getattr(t, n)() for n in dir(t) if n.startswith('test_')]"
```

(or `pytest` if you have it). See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Excel versions

If you prefer a spreadsheet, e2b offers free bilingual Excel calculators with a guide:
https://e2building.com/plantillas/calculadora-oee/ and https://e2building.com/plantillas/calculadora-coste-hora/

## Author

Javier González Martínez - industrial operations and Industry 4.0. [e2b](https://e2building.com)
