# Set Algebra System

A command-line tool that applies **set theory to 2D polygons**. Define polygons on a coordinate plane, combine them using union, intersection, and difference, which can be written in algebraic expressions like 'A + (B \* C)'. Then you can watch the result rendered live with Python's 'turtle' graphics module.

Built for the **MA1008 Mini Project (NTU)**, applying discrete mathematics (set algebra) to computational geometry.



```

A + (B + C) -> intersect A with the union of B and C
A - B       -> subtract B from A
A + B + C   -> union of three polygons

```

## Features

- **Interactive Polygon builder** - define any polygon by name and vertex coordinates
- **Set algebra engine** - union ('+'), intersection ('\*'), and difference ('-'), with parentheses and operator precedence
- **Live visualisation** - polygons and results are drawn with 'turtle', auto-scaled to fit the canvas
- **Multi-polygon / disjoint results** - operations that produce more than one separate shape (e.g. a difference that splits a polygon into two) are handled and drawn correctly
- **Persistence** - save the current set of polygons to a text file and reload them later
- **Expression validation** - checks for balanced parentheses, valid operators, and undefined polygon names before evaluating

## How it works

1. **Edge splitting** (`edges_split`) — every edge of polygon A is intersected against every edge of polygon B (and vice versa), so both polygons are broken into sub-edges at every crossing point.
2. **Classification** (`classify_edges`) — each sub-edge's midpoint is tested with a ray-casting **point-in-polygon** check to determine whether it lies inside or outside the other polygon.
3. **Recombination** — depending on the operation, the "inside" and "outside" sub-edge sets are combined differently:
   - **Intersection** = (A's edges inside B) + (B's edges inside A)
   - **Union** = (A's edges outside B) + (B's edges outside A)
   - **Difference (A − B)** = (A's edges outside B) + (B's edges inside A)
4. **Edge → polygon reconstruction** (`edges_to_polygons`) — the resulting sub-edges are walked and stitched back into one or more closed polygons, which correctly handles results that split into disjoint shapes.

Compound expressions (`A * (B + C)`) are parsed into tokens, validated for syntax, and evaluated recursively, resolving parenthesized sub-expressions first.
 
> Two routines — the edge-splitting loop and the parenthesis-parsing flow — were refined with GenAI assistance for optimization/clarity; the underlying logic and algorithm design are original.

## Getting started
 
### Prerequisites
 
- Python 3.x
- No external packages — only the standard library (`turtle`, `os`, `math`)
### Run it
 
```bash
git clone https://github.com/AMGhalcyon/set-algebra-system.git
cd set-algebra-system/source
python ma_1008_mini_project.py
```
 
A `turtle` graphics window will open alongside the terminal menu.
 
## Usage
 
On launch, you'll see the main menu:
 
```
SET ALGEBRA SYSTEM
----------------------------------------
1. Create a new polygon
2. Display stored polygons
3. Save polygons to file
4. Load existing polygons from file
5. Delete a polygon
6. Perform Set Algebra
7. Exit Program
----------------------------------------
```

**Typical workflow:**
 
1. **Create** two or more polygons (`1`), entering a name and vertex coordinates for each.
2. **Display** them (`2`) to see them drawn on the canvas.
3. **Perform Set Algebra** (`6`), entering an expression such as:
```
   A * B
   A + B
   A - B
   A * (B + C)
```
   The result is drawn in green on top of the source polygons, and you'll be prompted to save it as a new named polygon.
4. **Save** (`3`) / **Load** (`4`) polygons to/from `polygons.txt` to persist a session.
 
### Expression syntax
 
| Symbol | Operation    |
|--------|--------------|
| `+`    | Union        |
| `*`    | Intersection |
| `-`    | Difference   |
| `( )`  | Grouping     |
 

### File format
 
Polygons are saved to `polygons.txt` (created next to the script) as one line per polygon:
 
```
A:[(0.0, 0.0), (4.0, 0.0), (4.0, 4.0), (0.0, 4.0)]
B:[(2.0, 2.0), (6.0, 2.0), (6.0, 6.0), (2.0, 6.0)]
```

## Concepts applied
 
- **Set theory**: union, intersection, difference as first-class polygon operators
- **Discrete mathematics**: expression parsing/validation as a token-sequence grammar
- **Computational geometry**: line-segment intersection, ray-casting point-in-polygon tests, edge-based polygon clipping
## Known limitations
 
- Designed for **simple (non-self-intersecting) polygons**; results for self-intersecting or highly concave inputs aren't guaranteed to be geometrically correct.
- No dedicated handling for polygons that share edges exactly (coincident/parallel overlapping edges are treated as non-intersecting).
- Coordinates and results are floating-point; near-boundary cases rely on a small epsilon tolerance (`1e-9`) for intersection tests.
## Author
 
**Anish M Gangavaram**