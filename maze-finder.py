import tkinter as tk
from collections import deque

step = ["Down", "Up", "Right", "Left"]
dir = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def BFS(graph, s_x, s_y, g_x, g_y):
    global found
    found = False
    queue = deque()
    queue.append((s_x, s_y, 0))
    while queue:
        s_x, s_y, depth = queue.popleft()
        for i, (x, y) in enumerate(dir):
            n_x = s_x + x
            n_y = s_y + y
            if (n_x in range(len(graph)) and n_y in range(len(graph)) and graph[n_x][n_y] == 1):
                if n_x == g_x and n_y == g_y:
                    found = True
                    return depth + 1
                graph[n_x][n_y] = 0
                queue.append((n_x, n_y, depth + 1))
    return -1

def draw_grid(canvas, grid_size):
    cell_size = 30
    for i in range(grid_size):
        for j in range(grid_size):
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, outline="black")

def draw_obstacles(canvas, obstacles, grid_size):
    cell_size = 30
    for i in range(0,len(obstacles),2):
        x = obstacles[i]; y = obstacles[i+1]
        canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill="black")

def draw_path(canvas, path, grid_size):
    cell_size = 30
    for node in path:
        x, y = node
        canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill="blue")

def submit():
    grid_size = int(grid_entry.get())
    obstacles = list(map(int,obstacle_entry.get().split()))
    source = list(map(int, source_entry.get().split()))
    goal = list(map(int, goal_entry.get().split()))
    
    # Initialize canvas
    canvas.delete("all")
    canvas.config(width=grid_size * 30, height=grid_size * 30)
    draw_grid(canvas, grid_size)
    draw_obstacles(canvas, obstacles, grid_size)
    
    # Run BFS
    graph = [[1] * grid_size for _ in range(grid_size)]
    for i in range(0,len(obstacles),2):
        graph[obstacles[i]][obstacles[i+1]] = 0
    path_length = BFS(graph, source[0], source[1], goal[0], goal[1])
    if path_length != -1:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"Goal found!\nNumber of moves required: {path_length}\n")
        text_area.config(state=tk.DISABLED)
        # Calculate and draw path
        path = [(goal[0], goal[1])]
        x, y = source
        while (x, y) != goal:
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if nx >= 0 and ny >= 0 and nx < grid_size and ny < grid_size and graph[nx][ny] == graph[x][y] - 1:
                    path.append((nx, ny))
                    x, y = nx, ny
                    break
        draw_path(canvas, path, grid_size)
    else:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "Goal can't be reached from the source!\n")
        text_area.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Advanced BFS Pathfinding")

# Grid size input
grid_label = tk.Label(root, text="Enter the size of the grid:")
grid_label.grid(row=0, column=0, sticky="w")
grid_entry = tk.Entry(root)
grid_entry.grid(row=0, column=1, padx=5, pady=5)

# Obstacles input
obstacle_label = tk.Label(root, text="Enter obstacles (x y):")
obstacle_label.grid(row=1, column=0, sticky="w")
obstacle_entry = tk.Entry(root)
obstacle_entry.grid(row=1, column=1, padx=5, pady=5)

# Source and Goal inputs
source_label = tk.Label(root, text="Enter source co-ordinates (x y):")
source_label.grid(row=2, column=0, sticky="w")
source_entry = tk.Entry(root)
source_entry.grid(row=2, column=1, padx=5, pady=5)

goal_label = tk.Label(root, text="Enter goal co-ordinates (x y):")
goal_label.grid(row=3, column=0, sticky="w")
goal_entry = tk.Entry(root)
goal_entry.grid(row=3, column=1, padx=5, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=4, columnspan=2, pady=10)

# Canvas for visualization
canvas = tk.Canvas(root, width=300, height=300)
canvas.grid(row=5, columnspan=2, pady=10)
# Output text area
text_area = tk.Text(root, height=5, width=40)
text_area.grid(row=6, columnspan=2, pady=10)
text_area.config(state=tk.DISABLED)

root.mainloop()
