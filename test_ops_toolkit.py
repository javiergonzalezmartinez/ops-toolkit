import math
from ops_toolkit import *


def close(a, b, tol=0.01):
    return math.isclose(a, b, abs_tol=tol)


def test_company_cost():
    h = productive_hours_per_month(40, 0.65)
    assert close(h, 112.667, 0.001)
    cost = company_hourly_cost(14000, 40, 0.65)
    assert close(cost, 124.26)
    assert close(minimum_rate(cost, 0.15), 142.90)
    assert rate_verdict(110, cost) == "below cost"
    assert rate_verdict(130, cost) == "covers cost, no margin"
    assert rate_verdict(150, cost) == "covers cost and margin"


def test_machine_vs_person():
    person = resource_hourly_cost(32000, 1550)
    machine = resource_hourly_cost(72000, 3600)
    assert close(person, 20.65)
    assert close(machine, 20.00)
    assert close(cost_per_piece(person + machine, 2.5), 1.69)


def test_oee_by_hand():
    s = Shift(480, 30, 45, 8, 3000, 60)
    assert s.run_min == 405
    assert close(s.availability, 0.9, 1e-9)
    assert close(s.performance, 3000 / (405 * 8), 1e-9)
    assert close(s.quality, 0.98, 1e-9)
    assert close(s.oee, 0.9 * (3000 / 3240) * 0.98, 1e-9)
