"""
Engineering Reasoning Engine — Y (Intelligence Layer)
Part of the AI-based Structural Intelligence System.

LLM-powered dynamic explanations with cost-strength tradeoff analysis.
"""

import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import google.genai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


SYSTEM_PROMPT = """You are a senior structural engineer explaining construction material choices.
Provide clear, professional engineering justifications that focus on:
1. Cost-strength tradeoff analysis
2. Structural requirements (load-bearing vs partition)
3. Span considerations
4. Durability and long-term performance

Explain why the ranked materials were recommended in that order.
Be concise but technically accurate."""


def explain(wall: dict, materials: list) -> str:
    """Generate an engineering explanation for material recommendations.

    Parameters
    ----------
    wall : dict
        Wall properties (load_bearing, length, etc.)
    materials : list
        List of recommended materials with their scores (from materials.py)

    Returns
    -------
    str
        A professional structural-engineering justification
    """
    wall_type = "load-bearing" if wall.get("load_bearing", False) else "partition"
    length = wall.get("length", 0)
    
    if not materials or len(materials) == 0:
        return get_fallback_explanation(wall, "Red Brick")
    
    top_material = materials[0]["name"]
    
    try:
        return generate_llm_explanation(wall, materials)
    except Exception as e:
        print(f"LLM explanation failed: {e}")
        return get_fallback_explanation(wall, top_material)


def generate_llm_explanation(wall: dict, materials: list) -> str:
    """Use LLM to generate dynamic explanation."""
    wall_type = "load-bearing" if wall.get("load_bearing", False) else "partition"
    length = wall.get("length", 0)
    
    materials_info = "\n".join([
        f"{i+1}. {m['name']} - Cost: {m['cost']}, Strength: {m['strength']}, "
        f"Durability: {m['durability']}, Tradeoff Score: {m['tradeoff_score']}"
        for i, m in enumerate(materials)
    ])
    
    user_prompt = f"""Generate a professional engineering explanation for material selection.

Wall Properties:
- Type: {wall_type}
- Length/Span: {length}m
- Load-bearing: {wall.get('load_bearing', False)}

Ranked Material Options:
{materials_info}

Requirements:
1. Explain why the top recommendation is best for this specific wall
2. Compare the top 2-3 options in terms of cost vs strength tradeoff
3. Mention any structural concerns
4. Keep it concise (2-3 sentences)"""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=user_prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
    
    if OPENAI_AVAILABLE:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
    
    raise ValueError("No LLM API key available")


def get_fallback_explanation(wall: dict, material: str) -> str:
    """Generate explanation without LLM (rule-based fallback)."""
    wall_type = "load-bearing" if wall.get("load_bearing", False) else "partition"
    length = wall.get("length", 0)
    
    if material == "RCC" and length > 5:
        return (
            f"This {wall_type} wall spans {length}m and carries structural load. "
            f"RCC provides the compressive strength to bear upper-floor loads across a {length}m span. "
            f"Red brick would risk cracking under sustained axial stress at this length."
        )
    
    if material == "RCC":
        return (
            f"This {wall_type} wall is designated as load-bearing. "
            f"RCC is required to safely transfer compressive loads from the structure above. "
            f"Brick masonry lacks the tensile reinforcement needed for load-bearing applications."
        )
    
    if material == "Steel Frame":
        return (
            f"This {wall_type} wall spans {length}m, exceeding standard masonry limits. "
            f"A steel frame provides the rigidity and lateral stability needed for large-span partitions. "
            f"Red brick alone would require additional intermediate supports."
        )
    
    return (
        f"This {wall_type} wall spans {length}m — within standard masonry limits. "
        f"{material} is the most cost-effective choice for this application. "
        f"It offers good balance of strength, durability, and economy."
    )


def explain_single(wall: dict, material: str) -> str:
    """Backward-compatible single material explanation."""
    return explain(wall, [{"name": material, "cost": 0, "strength": 0, "durability": 0, "tradeoff_score": 0}])


if __name__ == "__main__":
    test_cases = [
        ({"load_bearing": True, "length": 8}, [
            {"name": "RCC", "cost": 95, "strength": 100, "durability": 90, "tradeoff_score": 85.5},
            {"name": "Steel Frame", "cost": 100, "strength": 95, "durability": 85, "tradeoff_score": 72.0},
            {"name": "Precast Concrete Panel", "cost": 90, "strength": 85, "durability": 80, "tradeoff_score": 68.9}
        ]),
        ({"load_bearing": False, "length": 3}, [
            {"name": "Red Brick", "cost": 60, "strength": 50, "durability": 70, "tradeoff_score": 55.0},
            {"name": "Fly Ash Brick", "cost": 55, "strength": 55, "durability": 60, "tradeoff_score": 54.5},
            {"name": "Hollow Concrete Block", "cost": 70, "strength": 60, "durability": 65, "tradeoff_score": 47.8}
        ]),
    ]
    
    for wall, materials in test_cases:
        print(f"Wall: {wall}")
        print(f"Explanation: {explain(wall, materials)}\n")
