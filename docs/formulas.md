# Formulas

All inputs are yours. The results are only as good as the data you enter.

## Hourly cost

| Quantity | Formula |
|---|---|
| Productive hours per month | hours per week x 52 / 12 x productive share x people |
| Hourly cost (break-even) | monthly costs / productive hours per month |
| Minimum rate | hourly cost x (1 + margin) |
| Person or machine hourly cost | annual cost / useful hours per year |
| Cost per piece | combined hourly cost / 60 x cycle time in minutes |

Worked example (illustrative inputs): 14 000 per month, 40 h per week, 65% productive, one person.
Productive hours = 40 x 52 / 12 x 0.65 = 112.67. Hourly cost = 14 000 / 112.67 = 124.26. With a 15% margin the minimum rate is 142.90.

Person 32 000 / 1 550 h = 20.65 per hour. Machine 72 000 / 3 600 h = 20.00 per hour. Combined 40.65. A 2.5 minute cycle gives 40.65 / 60 x 2.5 = 1.69 per piece.

## OEE

| Quantity | Formula |
|---|---|
| Planned production time | shift time - planned stops |
| Run time | planned production time - unplanned stops |
| Availability | run time / planned production time |
| Performance | total pieces / (run time x ideal rate per minute) |
| Quality | good pieces / total pieces |
| OEE | availability x performance x quality |

Worked example: shift 480 min, planned stops 30, unplanned stops 45, ideal rate 8 per minute, 3 000 pieces, 60 defective.
Planned production time 450. Run time 405. Availability 405 / 450 = 0.900. Performance 3 000 / (405 x 8) = 0.926. Quality 2 940 / 3 000 = 0.980. OEE = 0.900 x 0.926 x 0.980 = 0.817.

## Notes on inputs

- Use a measured ideal rate. Time a good cycle once instead of using the catalogue figure.
- Performance above 100% means the ideal rate or the counts are wrong. Check them.
- OEE describes the process, not the operator.
