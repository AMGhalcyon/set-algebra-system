"""
MA 1008 MINI-PROJECT
Author : Anish M Gangavaram

SET ALGEBRA SYSTEM
"""
import turtle
import os 
import math
# File format:
# Each line -> Name:[(x1, y1), (x2, y2), (x3, y3)]
''' 
* is intersection
+ is union
- is difference
'''

#creating a dictionary
POLYGONS = {}

#USER INTERACTION------------
#creating polygons using user input(interactive)
def create_polygon():
    name = input("Enter name for the polygon (eg. A, B, C..): ").upper()
    if name in POLYGONS:
        confirm = input("Do you want to overwrite the existing polygon (Y/N)? ").upper()
        if confirm != "Y":
            print("Cancelling creation.....\n")
            return None, None
    
    while True:
        
        try :
            
            n = int(input("Enter number of vertices of polygon: "))
            if n < 3:
                print("Polygon has to be atleast 3 sided! Try again. \n")
                print()
                continue
            else:
                break
        except ValueError:
            print("Invalid input! Please enter a numeric value (3 or more). \n")
            
       
        
        
    print(f"\nEnter {n} vertices as x-y coordinates\n")
    
    vertices = []
    
    for i in range(1, n+1):
        while True:
            
            try: 
                x_coord = float(input(f"Enter point {i} x-coordinate: "))
                y_coord = float(input(f"Enter point {i} y-coordinate: "))
                print()
                coordinate = (x_coord, y_coord)
                vertices.append(coordinate)
                break
            except ValueError: 
                print("Invalid input! please enter numeric values.\n")
                
    POLYGONS[name] = vertices   
    
    print(f"Polygon {name} is created successfully!")
    print(f"Vertices: {vertices}\n")
    
    
    return name, vertices 



#DISPLAYING POLYGONS-----------
def draw_polygon(polygons, color="blue", fill_color = None):
    turtle.color(color)
    turtle.hideturtle()
    turtle.pensize(2)

    # Normalize input: could be [(x, y), ...] or [[(x, y), ...]]
    if not polygons:
        return

    # Case 1: if it's a single polygon [(x, y), ...]
    if isinstance(polygons[0], tuple) and len(polygons[0]) == 2:
        polygons = [polygons]  # wrap it inside a list

    # Case 2: if it's a list of polygons [[(x, y), ...], ...]
    elif not (isinstance(polygons[0], list) and isinstance(polygons[0][0], tuple)):
        raise ValueError

    for poly in polygons:
        if len(poly) < 2:
            continue
        turtle.penup()
        turtle.goto(poly[0][0], poly[0][1])
        turtle.pendown()
        
        if fill_color:
            if fill_color:
                turtle.fillcolor(fill_color)
                turtle.begin_fill()
            
        for x, y in poly[1:]:
            turtle.goto(x, y)
        turtle.goto(poly[0][0], poly[0][1])# close the loop
        
        if fill_color:
            turtle.end_fill()
        




    


#for drawing sub_edges
def draw_edges(edges, color='green'):
    
    if not edges:
        print("No edges to draw.")
        return

    turtle.color(color)
    turtle.pensize(2)
    turtle.speed(0)
    turtle.hideturtle()

    for (p1, p2) in edges:
        x1, y1 = p1
        x2, y2 = p2
        turtle.penup()
        turtle.goto(x1, y1)
        turtle.pendown()
        turtle.goto(x2, y2)
    turtle.penup()
#drawing all polygons registered
turtle.tracer(0,0) #disbale autoupdates for performance


def display_polygons(POLYGONS):
    turtle.hideturtle()
    turtle.clear()
    all_x, all_y = [], []

    for name, verts in POLYGONS.items():
        # Normalize shape data
        if not verts:
            continue

        # Case 1: single polygon with points [(x, y), ...]
        if isinstance(verts[0], tuple) and len(verts[0]) == 2:
            for x, y in verts:
                all_x.append(x)
                all_y.append(y)

        # Case 2: list of polygons [[(x, y), ...], [(x, y), ...]]
        elif isinstance(verts[0], list) and isinstance(verts[0][0], tuple):
            for sub_poly in verts:
                for x, y in sub_poly:
                    all_x.append(x)
                    all_y.append(y)

        # Case 3: list of edges [((x1, y1), (x2, y2)), ...]
        elif isinstance(verts[0], tuple) and len(verts[0]) == 2 and isinstance(verts[0][0], tuple):
            for (x1, y1), (x2, y2) in verts:
                all_x += [x1, x2]
                all_y += [y1, y2]
        else:
            raise ValueError

    # Auto-scale window
    if all_x and all_y:
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        padding = 1
        turtle.setworldcoordinates(min_x - padding, min_y - padding, max_x + padding, max_y + padding)

    # Draw all polygons
    colors = [
     "blue", "red", "orange", "purple", "cyan", "magenta", 
     "brown", "pink", "gold", "violet", "indigo" ]
    color_index = 0

    for name, verts in POLYGONS.items():
        if not verts:
            continue
        
       
        else:
            # Cycle through colors if there are more polygons than colors
            color = colors[color_index % len(colors)]
            color_index += 1

        draw_polygon(verts, color=color)
    turtle.update()
    print('All polygons are displayed...\n')
    

    
#FILE HANDLING-------------    
#Save all polygons to a text file  
def save_polygons(filename="polygons.txt"):
    
    if not POLYGONS:
        print("No polygons to save.\n")
        return

    try:
        file_path = get_file_path(filename)
        with open(file_path, "w") as f:
            for name, verts in POLYGONS.items():
                f.write(f"{name}:{verts}\n")
        print(f"All polygons saved successfully to '{filename}'!\n")
    except:
        print("Error saving polygons!")
        

#parsing the resultant list in a text file into an actual list in python
def parse_vertices(verts_str):
    verts = []
    # Remove the brackets and split into individual coordinate pairs
    verts_str = verts_str.strip()[1:-1]  # removes outer [ ]
    pairs = verts_str.split("),")

    for p in pairs:
        p = p.replace("(", "").replace(")", "").strip()
        if p:
            x_str, y_str = p.split(",")
            x = float(x_str.strip())
            y = float(y_str.strip())
            verts.append((x, y))
    return verts

''''function for text file in the same folder as python file, relative of its location. 
Should be in the same folder though'''

def get_file_path(filename="polygons.txt"):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))  # folder where script is saved
    return os.path.join(script_dir, filename)

#Load polygons from a text file.
def load_polygons(filename="polygons.txt"):
    
    global POLYGONS
    try:
        file_path = get_file_path(filename)
        with open(file_path, "r") as f:
            POLYGONS.clear()
            for line in f:
                name, verts_str = line.strip().split(":", 1)
                verts = parse_vertices(verts_str)
                POLYGONS[name] = verts
        print(f"Polygons loaded successfully from '{filename}'!\n")
        print("Loaded polygons: ")
        for name in POLYGONS:
            print(f"{name}: {POLYGONS[name]}\n")
    except FileNotFoundError:
        print(f"File '{filename}' not found.\n")
    except:
        print("Error loading polygons!\n")
        
#function to delete a polygon from dictionary and the text file
def delete_polygon():
    if not POLYGONS:
        print("No polygons available to delete.\n")
        return

    
    print("Polygons available:")
    for name in POLYGONS:
        print(f"  {name}")
    
    name_to_delete = input("Enter the name of the polygon to delete: ").upper()

    if name_to_delete not in POLYGONS:
        print(f"Polygon '{name_to_delete}' does not exist.\n")
        return
    
   
    confirm = input(f"Are you sure you want to delete polygon '{name_to_delete}'? (Y/N): ").upper()
    if confirm != "Y":
        print("Deletion cancelled.\n")
        return
    
    # deleting from dictionary
    POLYGONS.pop(name_to_delete)
    print(f"Polygon '{name_to_delete}' deleted from memory.\n")

    # updating file using updated dictionary
    file_path = get_file_path("polygons.txt")
    try:
        with open(file_path, "w") as f:
            for name, verts in POLYGONS.items():
                f.write(f"{name}:{verts}\n")
        print("File 'polygons.txt' updated successfully.\n")
    except:
        print("Error updating file!")


#HELPER FUNCTIONS--------

#finding the intersection of the edges
def intersection_of_edges(edge1, edge2):
    (x1, y1), (x2,y2) = edge1
    (x3,y3), (x4,y4) = edge2
    
    denominator = ((x1-x2)*(y3-y4))-((y1-y2)*(x3-x4))
    
    if denominator == 0:
        return None #parallel lines or coincident 
    
    intersection_x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denominator
    intersection_y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denominator
    
    # Check if intersection lies within both segments
    if (min(x1, x2) - 1e-9 <= intersection_x <= max(x1, x2) + 1e-9 and
      min(y1, y2) - 1e-9 <= intersection_y <= max(y1, y2) + 1e-9 and
      min(x3, x4) - 1e-9 <= intersection_x <= max(x3, x4) + 1e-9 and
      min(y3, y4) - 1e-9 <= intersection_y <= max(y3, y4) + 1e-9):
        
        return (intersection_x, intersection_y)

    return None


#splitting the edges that intersect and making two new lists of all the edges of the two polygons
#used GenAI for optimising code, logic and writing done by me 
def edges_split(A, B):
    

    def polygon_to_edges(polygon):
        if not polygon:
            return []
        
        if isinstance(polygon[0][0], (int, float)):
            
            return [(polygon[i], polygon[(i+1) % len(polygon)]) for i in range(len(polygon))]
        elif isinstance(polygon[0], tuple) and len(polygon[0]) == 2:
            
            return [(polygon[i], polygon[(i+1) % len(polygon)]) for i in range(len(polygon))]
        elif isinstance(polygon[0], list) and isinstance(polygon[0][0], tuple):
           
            edges = []
            for subpolygon in polygon:
                edges.extend([(subpolygon[i], subpolygon[(i+1) % len(subpolygon)]) for i in range(len(subpolygon))])
            return edges
        else:
            raise ValueError

    A_edges = polygon_to_edges(A)
    B_edges = polygon_to_edges(B)

    def distance_sorting(item):
        return item[0]

    def split_edges(edges_to_split, other_edges):   #other_edges are the edges of another polygon that are splitting the current polygon's edges you are wokring on
        new_edges = []
        for edge in edges_to_split:
            if not (isinstance(edge, tuple) and len(edge) == 2):
                raise ValueError
            p1, p2 = edge
            intersections = []
            for other_edge in other_edges:
                intersection_p = intersection_of_edges(edge, other_edge)
                if intersection_p:
                    distance = math.hypot(intersection_p[0] - p1[0], intersection_p[1] - p1[1])
                    intersections.append((distance, intersection_p))
            intersections.sort(key=distance_sorting)
            points = [p1] + [intersection_p for _, intersection_p in intersections] + [p2]  #all points will be added
            for i in range(len(points) - 1):
                if points[i] != points[i + 1]:  #create new edges
                    new_edges.append((points[i], points[i + 1]))
        return new_edges

    A_split = split_edges(A_edges, B_edges)
    B_split = split_edges(B_edges, A_edges)

    return A_split, B_split


#All edges are converted to tuples of two (x, y) points
def normalize_edges(edges):
    
    normalized = []
    for e in edges:
        # if flat list of 4 numbers
        if isinstance(e, list) and len(e) == 4 and all(isinstance(n, (int,float)) for n in e):
            normalized.append(((e[0], e[1]), (e[2], e[3])))
        # if already tuple of points
        elif isinstance(e, tuple) and len(e) == 2 and all(isinstance(p, tuple) and len(p)==2 for p in e):
            normalized.append(e)
        else:  #just in case
            raise ValueError
    return normalized

#Return a single list of (x, y) coordinate tuples
def flatten_polygon(polygon):
    
    if not polygon:
        return []
    # if already flat
    if isinstance(polygon[0], tuple) and len(polygon[0]) == 2 and isinstance(polygon[0][0], (int, float)):
        return polygon
    # if list of polygons
    flat = []
    for subpolygon in polygon:
        if isinstance(subpolygon, tuple) and len(subpolygon) == 2:
            flat.append(subpolygon)
        elif isinstance(subpolygon, list):
            flat.extend(flatten_polygon(subpolygon))
        else: # for debugging purposes
            raise ValueError
    return flat

#Ray-casting algorithm for a flattened list of vertices 
#used gen AI help for this (only help)
#projects a ray to the right 
def point_in_polygon(point, polygon):
    
    polygon = flatten_polygon(polygon)
    x, y = point
    inside = False
    n = len(polygon)
    if n < 3:
        return False
    j = n - 1
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[j]
        # Check ray intersection
        if ((y1 > y) != (y2 > y)) and \
           (x < (x2 - x1) * (y - y1) / ((y2 - y1) + 1e-12) + x1):
            inside = not inside
        j = i
    return inside

#Classifies edges of a polygon relative of the other's 
def classify_edges(sub_edges, other_polygon):
    
    other_polygon = flatten_polygon(other_polygon)
    inside_edges = []
    outside_edges = []

    for edge in sub_edges:
        if not (isinstance(edge, tuple) and len(edge) == 2):  #just in case, for debugging
            raise ValueError

        midpoint = ((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2)
        if point_in_polygon(midpoint, other_polygon):
            inside_edges.append(edge)
        else:
            outside_edges.append(edge)

    return inside_edges, outside_edges

#converts a list of edges to vertices
def edges_to_vertices(edges):    #working fine 
    if not edges:
        return []
    
    vertices = [edges[0][0], edges[0][1]]
    edges_left = edges[1:]

    while edges_left:
        extended = False
        for i, (p1, p2) in enumerate(edges_left):
            if vertices[-1] == p1:
                vertices.append(p2)
                edges_left.pop(i)
                extended = True
                break
            elif vertices[-1] == p2:
                vertices.append(p1)
                edges_left.pop(i)
                extended = True
                break
            elif vertices[0] == p2:
                vertices = [p1] + vertices
                edges_left.pop(i)
                extended = True
                break
            elif vertices[0] == p1:
                vertices = [p2] + vertices
                edges_left.pop(i)
                extended = True
                break
        if not extended:   #for debuggin purposes
            raise ValueError

    # Ensure the polygon is closed (optional)
    if vertices[0] != vertices[-1]:
        vertices.append(vertices[0])

    return vertices

#validates an expression and returns the list of elements of user input
#Used GenAI for only understanding flow, logic is mine
def validate_expression():
    
    valid_operators = {'*', '+', '-', '(', ')'}

    while True:
        expression = input("Enter a set algebra expression (e.g., A * ( B + C )): ").strip()
        if not expression:
            print("Expression cannot be empty. Try again.\n")
            continue

        elements = expression.split()
        if not elements:
            print("Expression cannot be empty. Try again.\n")
            continue
        
        
        if not (elements[0].isalpha() or elements[0] == '('):
            print(f"Expression cannot start with '{elements[0]}'. It must start with a polygon or '('.\n")
            continue

        if not (elements[-1].isalpha() or elements[-1] == ')'):
            print(f"Expression cannot end with '{elements[-1]}'. It must end with a polygon or ')'.\n")
            continue

        last_element = None
        balance = 0
        error_found = False

        for element in elements:
            # Invalid character
            if element not in valid_operators and not element.isalpha():
                print(f"Invalid element '{element}' detected. Only polygon names and operators (*, +, -, (, )) are allowed.\n")
                error_found = True
                break

            
            if element.isalpha() and element not in POLYGONS:
                print(f"Polygon '{element}' does not exist. Available polygons: {', '.join(POLYGONS.keys())}\n")
                error_found = True
                break

           
            if last_element:
                if last_element.isalpha():
                    
                    if element.isalpha() or element == '(':
                        print(f"Missing operator between '{last_element}' and '{element}'\n")
                        error_found = True
                        break
                elif last_element in {'*', '+', '-'}:
                   
                    if element in {'*', '+', '-', ')'}:
                        print(f"Invalid sequence: '{last_element} {element}'\n")
                        error_found = True
                        break
                elif last_element == '(':
                    
                    if element in {'*', '+', '-', ')'}:
                        print(f"Invalid sequence: '{last_element} {element}'\n")
                        error_found = True
                        break
                elif last_element == ')':
                   
                    if element.isalpha() or element == '(':
                        print(f"Missing operator between '{last_element}' and '{element}'\n")
                        error_found = True
                        break

            # Parentheses balance
            if element == '(':
                balance += 1
            elif element == ')':
                balance -= 1
                if balance < 0:
                    print("Mismatched parentheses detected.\n")
                    error_found = True
                    break

            last_element = element

        if balance != 0:
            print("Mismatched parentheses detected.\n")
            error_found = True

        if not error_found:
            print("Expression is valid!\n")
            return elements  


#core algorithm, evaluates the elements returned after validating
def evaluate_expression(elements, POLYGONS):
    if not elements:
        return []

    if len(elements) == 1:
        return POLYGONS[elements[0]]

    # handles parentheses operations
    while '(' in elements:
        open_index = max(i for i, t in enumerate(elements) if t == '(')
        close_index = next(i for i, t in enumerate(elements[open_index:]) if t == ')') + open_index
        
        inner_result = evaluate_expression(elements[open_index+1:close_index], POLYGONS)
        
        elements = elements[:open_index] + [inner_result] + elements[close_index+1:]

    i = 1
    while i < len(elements)-1:
        if elements[i] in ['*', '+', '-']:
            
            a = elements[i-1] if isinstance(elements[i-1], list) else POLYGONS[elements[i-1]]
            b = elements[i+1] if isinstance(elements[i+1], list) else POLYGONS[elements[i+1]]

            # Perform operation
            if elements[i] == '*':
                result = operation_result_to_vertices(intersection_polygons(a, b))
            elif elements[i] == '+':
                result = operation_result_to_vertices(union_polygons(a, b))
            elif elements[i] == '-':
                result = operation_result_to_vertices(difference_polygons(a, b))

            
            elements = elements[:i-1] + [result] + elements[i+2:]
            i = 0  # reset to start
        i += 1

    #elements[0] holds final polygon
    return elements[0]



#because the operation function returns a list of edges
def operation_result_to_vertices(edges):
    if not edges:
        return []

    polygons = edges_to_polygons(edges)
    return polygons  # Each polygon is a list of vertices

#Returns a list of polygons from a set of edges, grouping connected edges. Hence giving disjoint polygons too
def edges_to_polygons(edges):
   
    edges_left = edges[:]
    polygons = []

    while edges_left:
        # Start a new polygon
        e = edges_left.pop(0)
        polygon = [e[0], e[1]]

        polygon_extended = True
        while polygon_extended:
            polygon_extended = False
            for i, (p1, p2) in enumerate(edges_left):
                if polygon[-1] == p1:
                    polygon.append(p2)
                    edges_left.pop(i)
                    polygon_extended = True
                    break
                elif polygon[-1] == p2:
                    polygon.append(p1)
                    edges_left.pop(i)
                    polygon_extended = True
                    break
                elif polygon[0] == p2:
                    polygon = [p1] + polygon
                    edges_left.pop(i)
                    polygon_extended = True
                    break
                elif polygon[0] == p1:
                    polygon = [p2] + polygon
                    edges_left.pop(i)
                    polygon_extended = True
                    break

        # Close polygon if not already
        if polygon[0] == polygon[-1]:
            polygon.pop(-1)

        polygons.append(polygon)

    return polygons



    

#SET ALGEBRA FUNCTIONS
def intersection_polygons(A, B):
   


    splitA, splitB = edges_split(A, B)

    A_inside_B, A_outside_B = classify_edges(splitA, B)
    B_inside_A, B_outside_A = classify_edges(splitB, A)


    intersection_edges = A_inside_B + B_inside_A

    return intersection_edges

def union_polygons(A, B):
    splitA, splitB = edges_split(A, B)

    # Step 2: classify each sub-edge of both polygons
    A_inside_B, A_outside_B = classify_edges(splitA, B)
    B_inside_A, B_outside_A = classify_edges(splitB, A)

    # Step 3: For union, we want edges that are outside as well as inside
    # but not the ones that are completely outside both polygons.
    union_edges =   A_outside_B + B_outside_A
    
    return union_edges


def difference_polygons(A, B):
    splitA, splitB = edges_split(A, B)
    # Step 2: classify each sub-edge of both polygons
    A_inside_B, A_outside_B = classify_edges(splitA, B)
    B_inside_A, B_outside_A = classify_edges(splitB, A)

    # Step 3: For union, we want edges that are outside as well as inside
    # but not the ones that are completely outside both polygons.
    
    difference_edges = A_outside_B + B_inside_A
    
    return difference_edges
    
#parent function of set operations
def perform_algebra():
    if len(POLYGONS) < 2:
        print("Need at least two polygons.\n")
        return

    print("Available polygons:", ", ".join(POLYGONS.keys()))
    print()
    
    elements = validate_expression()
    result_vertices = evaluate_expression(elements, POLYGONS)

    if not result_vertices:
        print("Resultant polygon is empty.\n")
        return

    # Normalize structure: ensure list of polygons (each polygon = list of (x,y))
    if isinstance(result_vertices[0][0], (int, float)):
        result_vertices = [result_vertices]  # single polygon
    elif isinstance(result_vertices[0], list) and isinstance(result_vertices[0][0], tuple):
        pass  # already correct
    else:
        raise ValueError("Unexpected result_vertices structure.")

    # Print vertex counts for clarity
    print("\nResulting vertices:")
    for i, poly in enumerate(result_vertices, 1):
        if len(poly) >= 3:
            
            print(f"  Polygon {i}: {len(poly)} vertices -> {poly}")

    # Create a temporary dictionary only for display
    display_dict = {name: POLYGONS[name] for name in POLYGONS if name in elements}

    # Draw stored polygons first
    turtle.clear()
    display_polygons(display_dict)

    # Draw the temporary green polygon on top
    draw_polygon(result_vertices, color="green", fill_color = 'lightgreen')
    turtle.update()

    # Ask user if they want to save it
    choice = input("Add this resultant polygon to dictionary? (Y/N): ").upper()
    if choice == "Y":
        new_name = input("Enter name for the new polygon: ").upper()
        if new_name in POLYGONS:
            user_choice = input(f"Overwrite existing polygon {new_name} (Y/N)? ").upper()
            if user_choice != "Y":
                print("Result not saved!\n")
                return
        POLYGONS[new_name] = result_vertices
        print(f"Polygon '{new_name}' added successfully!\n")
    else:
        print("Result not saved.\n")


#MAIN MENU------------  
#main menu function for user interaction (options)
def main_menu():
    while True:
        print("SET ALGEBRA SYSTEM")
        print("-"*40)
        print("1. Create a new polygon")
        print("2. Display stored polygons")
        print("3. Save polygons to file")
        print("4. Load existing polygons from file")
        print("5. Delete a polygon")
        print("6. Perform Set Algebra")
        print("7. Exit Program")
        print("-"*40)
        choice = input("Enter your choice (1-7): ")
        if choice == "1":
            create_polygon()
        elif choice == "2":
            display_polygons(POLYGONS)
        elif choice == "3":
            save_polygons()
        elif choice == "4":
            load_polygons()
        elif choice == "5":
            delete_polygon()
        elif choice == "6":
            perform_algebra()
       
        elif choice == "7":
            print()
            print("Exiting program.....\n")
            print("Goodbye!\n")
            print()
            break
        else:
            print("Invaid choice. Please select an appropriate option! \n")


main_menu()
















            
            
            
    
    