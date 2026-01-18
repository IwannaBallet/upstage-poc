#!/usr/bin/env python3
"""
AskUp Cost Calculator
======================
Calculate API costs at scale for Solar LLM-based equipment diagnosis.
"""

import json
from datetime import datetime

def calculate_costs(num_equipment, failures_per_month, api_cost_per_call=0.000165):
    """
    Calculate monthly and annual costs for AskUp implementation
    
    Args:
        num_equipment: Number of equipment units to monitor
        failures_per_month: Expected failures per equipment per month
        api_cost_per_call: Cost per Solar LLM API call
    
    Returns:
        Dictionary with cost breakdown
    """
    
    total_diagnoses_per_month = num_equipment * failures_per_month
    
    # API costs
    api_cost_monthly = total_diagnoses_per_month * api_cost_per_call
    api_cost_annual = api_cost_monthly * 12
    
    # SaaS subscription (tiered)
    if total_diagnoses_per_month <= 100:
        saas_cost_monthly = 500
    elif total_diagnoses_per_month <= 1000:
        saas_cost_monthly = 5000
    else:
        saas_cost_monthly = 10000  # Enterprise
    
    saas_cost_annual = saas_cost_monthly * 12
    
    # Infrastructure
    infrastructure_monthly = 1000  # Server, monitoring, etc.
    infrastructure_annual = infrastructure_monthly * 12
    
    # Total
    total_monthly = api_cost_monthly + saas_cost_monthly + infrastructure_monthly
    total_annual = total_monthly * 12
    
    # Cost per diagnosis
    cost_per_diagnosis = total_monthly / total_diagnoses_per_month if total_diagnoses_per_month > 0 else 0
    
    return {
        "equipment_count": num_equipment,
        "failures_per_month": failures_per_month,
        "diagnoses_per_month": total_diagnoses_per_month,
        "api_cost_monthly": round(api_cost_monthly, 2),
        "saas_cost_monthly": saas_cost_monthly,
        "infrastructure_monthly": infrastructure_monthly,
        "total_monthly": round(total_monthly, 2),
        "total_annual": round(total_annual, 2),
        "cost_per_diagnosis": round(cost_per_diagnosis, 4)
    }

def calculate_roi(num_equipment, failures_per_month, avg_downtime_hours=4, hourly_loss=10000):
    """
    Calculate ROI and savings
    
    Args:
        num_equipment: Number of equipment
        failures_per_month: Failures per equipment per month
        avg_downtime_hours: Average downtime per failure (before AskUp)
        hourly_loss: Cost per hour of downtime
    
    Returns:
        Dictionary with ROI metrics
    """
    
    # Get costs
    costs = calculate_costs(num_equipment, failures_per_month)
    
    # Failure impact without AskUp
    total_failures_monthly = costs["diagnoses_per_month"]
    
    # Before AskUp
    downtime_loss_before = total_failures_monthly * avg_downtime_hours * hourly_loss
    
    # With AskUp (assume 75% MTTR reduction)
    mttr_reduction = 0.75
    downtime_loss_after = downtime_loss_before * (1 - mttr_reduction)
    
    # Also prevent ~20% of failures with predictive maintenance
    prevented_failures_monthly = total_failures_monthly * 0.20
    prevented_loss_monthly = prevented_failures_monthly * avg_downtime_hours * hourly_loss
    
    # Total monthly benefit
    monthly_benefit = (downtime_loss_before - downtime_loss_after) + prevented_loss_monthly
    annual_benefit = monthly_benefit * 12
    
    # ROI
    total_annual_cost = costs["total_annual"]
    roi_percentage = ((annual_benefit - total_annual_cost) / total_annual_cost) * 100
    payback_days = (total_annual_cost / annual_benefit) * 365
    
    return {
        "monthly_diagnoses": costs["diagnoses_per_month"],
        "cost_per_diagnosis": costs["cost_per_diagnosis"],
        "monthly_cost": costs["total_monthly"],
        "annual_cost": costs["total_annual"],
        "downtime_loss_before": round(downtime_loss_before, 2),
        "downtime_loss_after": round(downtime_loss_after, 2),
        "prevented_failures_monthly": round(prevented_failures_monthly, 1),
        "prevented_loss_monthly": round(prevented_loss_monthly, 2),
        "monthly_benefit": round(monthly_benefit, 2),
        "annual_benefit": round(annual_benefit, 2),
        "net_benefit_annual": round(annual_benefit - total_annual_cost, 2),
        "roi_percentage": round(roi_percentage, 1),
        "payback_days": round(payback_days, 1)
    }

def print_cost_analysis():
    """Print cost analysis for different scales"""
    
    print("\n" + "="*90)
    print("💰 ASKUP COST CALCULATOR - Scale Analysis")
    print("="*90)
    
    scenarios = [
        {"name": "Small Factory", "equipment": 20, "failures_per_month": 1},
        {"name": "Medium Factory", "equipment": 100, "failures_per_month": 2},
        {"name": "Large Factory", "equipment": 500, "failures_per_month": 1.5},
        {"name": "Enterprise (Multi-site)", "equipment": 2000, "failures_per_month": 1},
    ]
    
    results = []
    
    for scenario in scenarios:
        roi = calculate_roi(
            scenario["equipment"],
            scenario["failures_per_month"]
        )
        results.append(roi)
        
        print(f"\n📍 {scenario['name']}")
        print(f"   Equipment Units: {scenario['equipment']}")
        print(f"   Expected Failures/Month: {scenario['failures_per_month']} per equipment")
        print(f"   Total Diagnoses/Month: {roi['monthly_diagnoses']:.0f}")
        print(f"   ─────────────────────────────────────────")
        print(f"   Monthly AskUp Cost:     ${roi['monthly_cost']:>12,.2f}")
        print(f"   Annual AskUp Cost:      ${roi['annual_cost']:>12,.2f}")
        print(f"   ─────────────────────────────────────────")
        print(f"   Monthly Benefit:        ${roi['monthly_benefit']:>12,.2f}")
        print(f"   Annual Benefit:         ${roi['annual_benefit']:>12,.2f}")
        print(f"   ─────────────────────────────────────────")
        print(f"   💸 NET ANNUAL BENEFIT:  ${roi['net_benefit_annual']:>12,.2f}")
        print(f"   📊 ROI:                 {roi['roi_percentage']:>12.0f}%")
        print(f"   ⏱️  Payback Period:      {roi['payback_days']:>12.1f} days")
    
    # Pricing tier recommendation
    print("\n" + "="*90)
    print("💳 RECOMMENDED PRICING TIERS")
    print("="*90)
    
    for scenario, roi in zip(scenarios, results):
        if roi['monthly_diagnoses'] <= 100:
            tier = "Starter ($500/month)"
        elif roi['monthly_diagnoses'] <= 1000:
            tier = "Professional ($5,000/month)"
        else:
            tier = "Enterprise (Custom)"
        
        print(f"{scenario['name']:<30} → {tier}")
    
    # Save to JSON
    output = {
        "timestamp": datetime.now().isoformat(),
        "scenarios": scenarios,
        "results": results,
        "key_findings": {
            "payback_period_days": round(min([r['payback_days'] for r in results]), 1),
            "avg_roi": round(sum([r['roi_percentage'] for r in results]) / len(results), 1),
            "cost_per_diagnosis": round(min([r['cost_per_diagnosis'] for r in results]), 4)
        }
    }
    
    with open("cost_analysis.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Cost analysis saved to cost_analysis.json")
    print("="*90 + "\n")

if __name__ == "__main__":
    print_cost_analysis()
