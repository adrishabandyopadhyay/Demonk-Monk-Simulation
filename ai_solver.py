from collections import deque

TOTAL_MONKS = 3
TOTAL_DEMONS = 3

# Check if a state is valid
def is_valid(m_left, d_left):
    m_right = TOTAL_MONKS - m_left
    d_right = TOTAL_DEMONS - d_left

    # No negative or overflow
    if m_left < 0 or d_left < 0 or m_left > TOTAL_MONKS or d_left > TOTAL_DEMONS:
        return False

    # Left side rule
    if m_left > 0 and d_left > m_left:
        return False

    # Right side rule
    if m_right > 0 and d_right > m_right:
        return False

    return True


# Possible boat moves (monks, demons)
moves = [
    (1, 0),
    (2, 0),
    (0, 1),
    (0, 2),
    (1, 1)
]


def bfs():
    start = (3, 3, 0)   # (monks_left, demons_left, boat: 0=left, 1=right)
    goal = (0, 0, 1)

    queue = deque()
    queue.append((start, []))

    visited = set()

    while queue:
        (m_left, d_left, boat), path = queue.popleft()

        if (m_left, d_left, boat) == goal:
            return path + [(m_left, d_left, boat)]

        if (m_left, d_left, boat) in visited:
            continue

        visited.add((m_left, d_left, boat))

        for m, d in moves:
            if boat == 0:  # Boat on left → go right
                new_state = (m_left - m, d_left - d, 1)
            else:          # Boat on right → go left
                new_state = (m_left + m, d_left + d, 0)

            nm, nd, nb = new_state

            if is_valid(nm, nd):
                queue.append((new_state, path + [(m_left, d_left, boat)]))

    return None


# Function to get solution and distance
def get_solution():
    solution = bfs()
    if solution:
        distance = len(solution) - 1
        return solution, distance
    else:
        return None, 0

if __name__ == "__main__":
    sol, dist = get_solution()
    print("Distance:", dist)
    for step in sol:
        print(step)
