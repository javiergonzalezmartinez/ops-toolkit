"""ops-toolkit: small, readable formulas for shop-floor numbers.

Hourly cost (company, person, machine, cost per piece) and OEE.
Plain Python, no dependencies. Every function is a one-line formula you can
check by hand. Inputs are yours: the results are only as good as your data.
"""
from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass


# ---------- Hourly cost ----------

def productive_hours_per_month(hours_per_week: float, productive_share: float, people: int = 1) -> float:
    """Productive hours per month = weekly hours x 52 / 12 x productive share x people."""
    return hours_per_week * 52 / 12 * productive_share * people


def company_hourly_cost(monthly_costs: float, hours_per_week: float, productive_share: float, people: int = 1) -> float:
    """Break-even cost per productive hour = monthly costs / productive hours per month."""
    return monthly_costs / productive_hours_per_month(hours_per_week, productive_share, people)


def minimum_rate(hourly_cost: float, margin: float = 0.15) -> float:
    """Rate with a safety margin = hourly cost x (1 + margin)."""
    return hourly_cost * (1 + margin)


def rate_verdict(rate: float, hourly_cost: float, margin: float = 0.15) -> str:
    if rate < hourly_cost:
        return "below cost"
    if rate < minimum_rate(hourly_cost, margin):
        return "covers cost, no margin"
    return "covers cost and margin"


def resource_hourly_cost(annual_cost: float, useful_hours_per_year: float) -> float:
    """Hourly cost of one resource (person or machine) = annual cost / useful hours per year."""
    return annual_cost / useful_hours_per_year


def cost_per_piece(combined_hourly_cost: float, cycle_time_min: float) -> float:
    """Cost per piece = hourly cost / 60 x cycle time in minutes."""
    return combined_hourly_cost / 60 * cycle_time_min


# ---------- OEE ----------

@dataclass
class Shift:
    shift_min: float
    planned_stop_min: float
    unplanned_stop_min: float
    ideal_rate_per_min: float
    total_pieces: float
    defective_pieces: float

    @property
    def planned_production_min(self) -> float:
        return self.shift_min - self.planned_stop_min

    @property
    def run_min(self) -> float:
        return self.planned_production_min - self.unplanned_stop_min

    @property
    def availability(self) -> float:
        return self.run_min / self.planned_production_min

    @property
    def performance(self) -> float:
        return self.total_pieces / (self.run_min * self.ideal_rate_per_min)

    @property
    def quality(self) -> float:
        return (self.total_pieces - self.defective_pieces) / self.total_pieces

    @property
    def oee(self) -> float:
        return self.availability * self.performance * self.quality


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def _read_shifts(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield row["date"], row["line"], row.get("stop_reason", ""), Shift(
                float(row["shift_min"]),
                float(row["planned_stop_min"]),
                float(row["unplanned_stop_min"]),
                float(row["ideal_rate_per_min"]),
                float(row["total_pieces"]),
                float(row["defective_pieces"]),
            )


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Hourly cost and OEE helpers")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("cost", help="company hourly cost")
    c.add_argument("--monthly-costs", type=float, required=True)
    c.add_argument("--hours-per-week", type=float, default=40)
    c.add_argument("--productive-share", type=float, required=True, help="0-1, e.g. 0.65")
    c.add_argument("--people", type=int, default=1)
    c.add_argument("--margin", type=float, default=0.15)
    c.add_argument("--rate", type=float, help="your current rate, for the verdict")

    o = sub.add_parser("oee", help="OEE from a CSV of shifts (see oee_shifts_example.csv)")
    o.add_argument("csv")

    a = p.parse_args(argv)
    if a.cmd == "cost":
        cost = company_hourly_cost(a.monthly_costs, a.hours_per_week, a.productive_share, a.people)
        print(f"productive hours/month: {productive_hours_per_month(a.hours_per_week, a.productive_share, a.people):.2f}")
        print(f"hourly cost (break-even): {cost:.2f}")
        print(f"minimum rate with {a.margin:.0%} margin: {minimum_rate(cost, a.margin):.2f}")
        if a.rate is not None:
            print(f"verdict for rate {a.rate:.2f}: {rate_verdict(a.rate, cost, a.margin)}")
    else:
        rows = list(_read_shifts(a.csv))
        print("date,line,availability,performance,quality,oee")
        for d, line, _, s in rows:
            print(f"{d},{line},{_pct(s.availability)},{_pct(s.performance)},{_pct(s.quality)},{_pct(s.oee)}")
        lost: dict[str, float] = {}
        for _, _, reason, s in rows:
            if reason:
                lost[reason] = lost.get(reason, 0) + s.unplanned_stop_min
        if lost:
            print("\nunplanned minutes lost by reason (Pareto):")
            for r, m in sorted(lost.items(), key=lambda kv: -kv[1]):
                print(f"  {r}: {m:.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
