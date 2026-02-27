from flask import Flask, render_template, request, session
from ai_solver import get_solution

app = Flask(__name__)
app.secret_key = "secretkey"


# -------- Helper: check valid state --------
def is_valid(m, d):
    return (
        0 <= m <= 3 and
        0 <= d <= 3 and
        (m == 0 or m >= d) and
        ((3 - m) == 0 or (3 - m) >= (3 - d))
    )


# -------- Helper: check if user is stuck --------
def is_stuck(state):
    m, d, boat = state
    direction = -1 if boat == 0 else 1

    moves = [
        (1, 0),
        (2, 0),
        (0, 1),
        (0, 2),
        (1, 1)
    ]

    for mm, dd in moves:
        new_m = m + direction * mm
        new_d = d + direction * dd
        if is_valid(new_m, new_d):
            return False
    return True


@app.route("/", methods=["GET", "POST"])
def home():

    # -------- FIRST VISIT ONLY --------
    if "screen" not in session:
        session.clear()
        session["screen"] = "welcome"

    # -------- POST actions --------
    if request.method == "POST":
        action = request.form.get("action")

        # Welcome → Instructions
        if action == "start_game":
            session.clear()
            session["screen"] = "instructions"

        # Instructions → Game
        elif action == "next_instructions":
            session["screen"] = "game"
            session["state"] = (3, 3, 0)
            session["user_moves"] = 0
            session["hint"] = None
            session["error"] = None
            session["stuck"] = False

            solution, distance = get_solution()
            session["solution"] = solution
            session["distance"] = distance

        # -------- USER MOVE --------
        elif action == "move":
            state = session.get("state", (3, 3, 0))
            move_type = request.form.get("move_type")

            m, d, boat = state
            direction = -1 if boat == 0 else 1

            if move_type == "1M":
                m += direction
            elif move_type == "2M":
                m += 2 * direction
            elif move_type == "1D":
                d += direction
            elif move_type == "2D":
                d += 2 * direction
            elif move_type == "1M1D":
                m += direction
                d += direction

            boat = 1 - boat

            # Validate
            if is_valid(m, d):
                session["state"] = (m, d, boat)
                session["user_moves"] = session.get("user_moves", 0) + 1
                session["hint"] = None
                session["error"] = None
            else:
                session["error"] = "Invalid move! Demons outnumber monks."

            session["stuck"] = is_stuck(session.get("state"))

        # -------- AI HINT --------
        elif action == "hint":
            solution = session.get("solution")
            state = session.get("state")

            if solution and state in solution:
                idx = solution.index(state)
                if idx < len(solution) - 1:
                    next_state = solution[idx + 1]

                    m1, d1, b1 = state
                    m2, d2, b2 = next_state

                    monks = abs(m1 - m2)
                    demons = abs(d1 - d2)
                    direction = "Right" if b1 == 0 else "Left"

                    parts = []
                    if monks == 1:
                        parts.append("1 Monk")
                    elif monks == 2:
                        parts.append("2 Monks")

                    if demons == 1:
                        parts.append("1 Demon")
                    elif demons == 2:
                        parts.append("2 Demons")

                    session["hint"] = "Move " + " and ".join(parts) + f" to {direction}"

        # -------- Restart --------
        elif action == "restart":
            session.clear()
            session["screen"] = "welcome"

    # -------- Data for template --------
    screen = session.get("screen", "welcome")
    state = session.get("state")
    solution = session.get("solution")
    distance = session.get("distance")
    hint = session.get("hint")
    user_moves = session.get("user_moves", 0)
    error = session.get("error")
    stuck = session.get("stuck", False)

    goal_reached = state == (0, 0, 1)
    optimal = goal_reached and user_moves == distance
    confetti = goal_reached

    return render_template(
        "index.html",
        screen=screen,
        state=state,
        solution=solution,
        distance=distance,
        hint=hint,
        user_moves=user_moves,
        goal_reached=goal_reached,
        optimal=optimal,
        confetti=confetti,
        error=error,
        stuck=stuck
    )


if __name__ == "__main__":
    app.run(debug=True)