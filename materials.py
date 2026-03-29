"""
Material Recommendation Engine — Y (Intelligence Layer)
Part of the AI-based Structural Intelligence System.

Material Database with Cost-Strength Tradeoff Analysis.
Returns ranked material options per structural element.
"""

MATERIAL_DATABASE = {
    "AAC Blocks": {
        "cost": 85,
        "strength": 70,
        "durability": 75,
        "weight": "light",
        "description": "Autoclaved Aerated Concrete - lightweight, good insulation"
    },
    "Red Brick": {
        "cost": 60,
        "strength": 50,
        "durability": 70,
        "weight": "medium",
        "description": "Traditional clay brick - cost-effective, proven performance"
    },
    "RCC": {
        "cost": 95,
        "strength": 100,
        "durability": 90,
        "weight": "heavy",
        "description": "Reinforced Cement Concrete - highest strength for load-bearing"
    },
    "Steel Frame": {
        "cost": 100,
        "strength": 95,
        "durability": 85,
        "weight": "medium",
        "description": "Steel structural frame - excellent for long spans"
    },
    "Hollow Concrete Block": {
        "cost": 70,
        "strength": 60,
        "durability": 65,
        "weight": "light",
        "description": "Concrete hollow block - faster construction, moderate cost"
    },
    "Fly Ash Brick": {
        "cost": 55,
        "strength": 55,
        "durability": 60,
        "weight": "medium",
        "description": "Industrial waste brick - eco-friendly, economical"
    },
    "Precast Concrete Panel": {
        "cost": 90,
        "strength": 85,
        "durability": 80,
        "weight": "heavy",
        "description": "Pre-cast panels - quick installation, consistent quality"
    }
}


MATERIAL_RULES = [
    (lambda w: w.get("load_bearing", False) and w.get("length", 0) > 5, ["RCC", "Steel Frame", "Precast Concrete Panel"]),
    (lambda w: w.get("load_bearing", False), ["RCC", "Hollow Concrete Block", "Red Brick"]),
    (lambda w: w.get("length", 0) > 5, ["Steel Frame", "Precast Concrete Panel", "AAC Blocks"]),
]

DEFAULT_MATERIALS = ["Red Brick", "Fly Ash Brick", "Hollow Concrete Block"]


def recommend_material(wall: dict) -> list:
    """Recommend ranked construction materials for a wall.

    Parameters
    ----------
    wall : dict
        Keys: ``load_bearing`` (bool), ``length`` (float/int), etc.

    Returns
    -------
    list
        List of 2-3 recommended materials in ranked order, each as dict with name and scores
    """
    candidates = None
    
    for predicate, materials in MATERIAL_RULES:
        if predicate(wall):
            candidates = materials
            break
    
    if not candidates:
        candidates = DEFAULT_MATERIALS
    
    ranked = []
    for mat_name in candidates[:3]:
        if mat_name in MATERIAL_DATABASE:
            mat_data = MATERIAL_DATABASE[mat_name]
            tradeoff = calculate_tradeoff(wall, mat_name)
            ranked.append({
                "name": mat_name,
                "cost": mat_data["cost"],
                "strength": mat_data["strength"],
                "durability": mat_data["durability"],
                "tradeoff_score": tradeoff,
                "description": mat_data["description"]
            })
    
    ranked.sort(key=lambda x: x["tradeoff_score"], reverse=True)
    
    return ranked[:3]


def calculate_tradeoff(wall: dict, material: str) -> float:
    """Calculate cost-strength tradeoff score for wall-material combination.
    
    Higher score = better value (higher strength per cost)
    
    Parameters
    ----------
    wall : dict
        Wall properties
    material : str
        Material name from MATERIAL_DATABASE
    
    Returns
    -------
    float
        Tradeoff score (higher is better)
    """
    if material not in MATERIAL_DATABASE:
        return 0.0
    
    mat = MATERIAL_DATABASE[material]
    cost = mat["cost"]
    strength = mat["strength"]
    durability = mat["durability"]
    
    base_score = (strength * 0.5 + durability * 0.3) / cost * 100
    
    length = wall.get("length", 0)
    is_load_bearing = wall.get("load_bearing", False)
    
    if is_load_bearing and material == "RCC":
        base_score *= 1.3
    elif is_load_bearing and material == "Steel Frame":
        base_score *= 1.15
    elif is_load_bearing and strength < 70:
        base_score *= 0.7
    
    if length > 5 and material == "Steel Frame":
        base_score *= 1.2
    elif length > 5 and material == "RCC":
        base_score *= 1.1
    elif length > 5 and cost > 90:
        base_score *= 0.9
    
    return round(base_score, 2)


def calculate_risk_score(wall: dict, material: str) -> int:
    """Calculate a 0-100 risk score for a wall based on properties & material."""
    score = 10
    length = wall.get("length", 0)
    
    score += min(length * 2, 40)
    
    if wall.get("load_bearing", False):
        score += 40
        if material in MATERIAL_DATABASE:
            strength = MATERIAL_DATABASE[material]["strength"]
            if strength >= 90:
                score -= 25
            elif strength >= 70:
                score -= 15
    else:
        score += 10
        if material in MATERIAL_DATABASE:
            strength = MATERIAL_DATABASE[material]["strength"]
            if strength >= 80:
                score -= 15
    
    return max(0, min(int(score), 100))


def get_top_material(wall: dict) -> str:
    """Get the single top recommendation for backward compatibility."""
    recommendations = recommend_material(wall)
    return recommendations[0]["name"] if recommendations else "Red Brick"


if __name__ == "__main__":
    tests = [
        {"load_bearing": True, "length": 8},
        {"load_bearing": True, "length": 3},
        {"load_bearing": False, "length": 7},
        {"load_bearing": False, "length": 3},
    ]
    
    for wall in tests:
        print(f"Wall: {wall}")
        recs = recommend_material(wall)
        for i, r in enumerate(recs, 1):
            print(f"  {i}. {r['name']} (score: {r['tradeoff_score']})")
        print()
