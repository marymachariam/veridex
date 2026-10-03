"""Run once to create PayPal billing plans. Copy the printed plan IDs into core/constants.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.constants import PLAN_PRICES_USD
from services.paypal_service import create_product_and_plan

if __name__ == "__main__":
    for plan_name, price in PLAN_PRICES_USD.items():
        plan_id = create_product_and_plan(plan_name.capitalize(), price)
        print(f"{plan_name}: {plan_id}")