import heapq
from config import GRID_WIDTH, GRID_HEIGHT

def heuristic(a, b):
  (x1, y1) = a
  (x2, y2) = b
  dx = abs(x1 - x2)
  dy = abs(y1 - y2)
  return dx + dy + (dx * dy) / (GRID_WIDTH + GRID_HEIGHT)

def a_star_search(rows, start, goal):
  frontier = []
  heapq.heappush(frontier, (0, start))
  came_from = {}
  cost_so_far = {}
  came_from[start] = None
  cost_so_far[start] = 0
  
  while frontier:
    current = heapq.heappop(frontier)[1]
    
    if current == goal:
      break
    
    for next in neighbors(current, rows):
      new_cost = cost_so_far[current] + cost(current, next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
        cost_so_far[next] = new_cost
        priority = new_cost + heuristic(goal, next)
        heapq.heappush(frontier, (priority, next))
        came_from[next] = current
  
  return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
  current = goal
  path = []
  while current != start:
      path.append(current)
      current = came_from[current]
  path.append(start)
  path.reverse()
  return path

def neighbors(cell, rows):
  (x, y) = cell
  neighbors = [
    (x, y-1),    # Top
    (x-1, y),    # Left
    (x+1, y),    # Right
    (x, y+1),    # Bottom
  ]
  diagonals = [
    (x-1, y-1),  # Top-left
    (x+1, y-1),  # Top-right
    (x-1, y+1),  # Bottom-left
    (x+1, y+1)   # Bottom-right
  ]

  valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and rows[ny][nx] == 0]

  for dx, dy in diagonals:
    if 0 <= dx < GRID_WIDTH and 0 <= dy < GRID_HEIGHT and rows[dy][dx] == 0:
      # Check if the path to the diagonal neighbor is blocked
      if not (rows[y][dx] == 1 and rows[dy][x] == 1):
        valid_neighbors.append((dx, dy))

  return valid_neighbors

# def cost(current, next):
#   return 1  # Assuming all movements have the same cost

def cost(a, b):
  (x1, y1) = a
  (x2, y2) = b
  if x1 != x2 and y1 != y2:
    return 1.414  # Cost of moving diagonally
  else:
    return 1  # Cost of moving horizontally or vertically