from typing import Dict, List, Optional


def diff_pricing(old_tiers: List[dict], new_tiers: List[dict]) -> List[dict]:
    """old_tiers/new_tiers: [{"tier_name": ..., "price_usd": ..., "billing_period": ...}]"""
    old_by_name = {t["tier_name"]: t for t in old_tiers}
    new_by_name = {t["tier_name"]: t for t in new_tiers}
    changes = []

    for name, new_tier in new_by_name.items():
        old_tier = old_by_name.get(name)
        if old_tier is None:
            changes.append({
                "change_type": "pricing",
                "summary": f"New pricing tier added: {name} "
                           f"({'$' + str(new_tier['price_usd']) if new_tier.get('price_usd') is not None else 'Contact sales'})",
                "old_value": None,
                "new_value": str(new_tier.get("price_usd")),
            })
        elif old_tier.get("price_usd") != new_tier.get("price_usd"):
            old_price = old_tier.get("price_usd")
            new_price = new_tier.get("price_usd")
            old_str = f"${old_price:,.0f}" if old_price is not None else "Contact sales"
            new_str = f"${new_price:,.0f}" if new_price is not None else "Contact sales"
            changes.append({
                "change_type": "pricing",
                "summary": f"{name} tier price changed from {old_str} to {new_str}",
                "old_value": str(old_price),
                "new_value": str(new_price),
            })

    for name in old_by_name:
        if name not in new_by_name:
            changes.append({
                "change_type": "pricing",
                "summary": f"Pricing tier removed: {name}",
                "old_value": name,
                "new_value": None,
            })

    return changes


def diff_features(old_features: List[str], new_features: List[str]) -> List[dict]:
    old_set, new_set = set(old_features), set(new_features)
    changes = []

    for added in sorted(new_set - old_set):
        changes.append({
            "change_type": "feature_added",
            "summary": f"New feature added: {added}",
            "old_value": None,
            "new_value": added,
        })

    for removed in sorted(old_set - new_set):
        changes.append({
            "change_type": "feature_removed",
            "summary": f"Feature no longer listed: {removed}",
            "old_value": removed,
            "new_value": None,
        })

    return changes


def diff_positioning(old_tagline: Optional[str], new_tagline: Optional[str]) -> List[dict]:
    if old_tagline and new_tagline and old_tagline.strip() != new_tagline.strip():
        return [{
            "change_type": "positioning",
            "summary": f'Tagline changed from "{old_tagline}" to "{new_tagline}"',
            "old_value": old_tagline,
            "new_value": new_tagline,
        }]
    return []