from utils import read_file_as_grid
import shapely


def get_polygons(data):
    polygons = {}
    for row in range(len(data)):
        for col in range(len(data[0])):
            crop = data[row][col]
            polygons.setdefault(crop, [])
            polygons[crop].append(shapely.Polygon(((row, col), (row, col + 1), (row + 1, col + 1), (row + 1, col))))

    for p in polygons:
        polygons[p] = shapely.unary_union(polygons[p])

    return polygons

def part1(input_path):
    data = read_file_as_grid(input_path)
    polygons = get_polygons(data)

    total = 0

    for polygon in polygons.values():
        if isinstance(polygon, shapely.MultiPolygon):
            for poly in polygon.geoms:
                total += (poly.area * poly.length)
        else:
            total += (polygon.area * polygon.length)
    
    print(total)


def polygon_sides_from_coords(coords):
    simplified = shapely.simplify(coords, tolerance=0)

    # one pair of coords is always duplicated (the joining of the ring)
    sides = len(simplified.coords) - 1
    # if the ring starts part way down a side, there will be an extra (odd number)
    # of coordinates
    if sides % 2 != 0:
        sides -= 1
    return sides


def polygon_sides(polygon):
    components = [polygon.exterior, *[p for p in polygon.interiors]]
    return sum(polygon_sides_from_coords(component) for component in components)


def part2(input_path):
    data = read_file_as_grid(input_path)
    polygons = get_polygons(data)

    total = 0

    for polygon in polygons.values():
        if isinstance(polygon, shapely.MultiPolygon):
            for poly in polygon.geoms:
                total += (poly.area * polygon_sides(poly))
        else:
            total += (polygon.area * polygon_sides(polygon))
    
    print(total)
