from data import rooms, walls
from materials import recommend_material
from explain import explain


def main():
    print("=" * 60)
    print("  SANCTUM — Wall Material Recommendation Report")
    print("=" * 60)

    # Room summary
    print(f"\n  House Layout: {len(rooms)} rooms, {len(walls)} walls\n")
    for room in rooms:
        print(f"    • {room['name']:18s}  {room['width']}ft × {room['length']}ft")

    print("\n" + "-" * 60)
    print("  Wall-by-Wall Analysis")
    print("-" * 60)

    for i, wall in enumerate(walls, start=1):
        material = recommend_material(wall)
        reasoning = explain(wall, material)

        print(f"\n  Wall #{i}")
        print(f"    Type     : {wall['type'].replace('_', ' ').title()}")
        print(f"    Length   : {wall['length']} ft")
        print(f"    Material : {material}")
        print(f"    Reason   : {reasoning}")

    print("\n" + "=" * 60)
    print("  Report complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
