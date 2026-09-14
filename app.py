from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database location
DATABASE = os.path.join("data", "phishguard.db")


# -----------------------------
# Database Helper
# -----------------------------
def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------
# Initialize Database
# -----------------------------
def init_db():
    os.makedirs("data", exist_ok=True)

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            target_group TEXT,
            description TEXT,
            template TEXT,
            start_date TEXT,
            duration TEXT
        )
    """)

    connection.commit()
    connection.close()


# Initialize database when application starts
init_db()


# -----------------------------
# Dashboard
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Simulations Page
# -----------------------------
@app.route("/simulations")
def simulations():

    connection = get_db_connection()

    simulations_data = connection.execute("""
        SELECT * FROM simulations
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return render_template(
        "simulations.html",
        simulations=simulations_data
    )

# Simulation Details
@app.route("/simulation/<int:simulation_id>")
def simulation_details(simulation_id):

    connection = get_db_connection()

    simulation = connection.execute(
        "SELECT * FROM simulations WHERE id = ?",
        (simulation_id,)
    ).fetchone()

    connection.close()

    if simulation is None:
        return "Simulation not found", 404

    return render_template(
        "simulation_details.html",
        simulation=simulation
    )


# -----------------------------
# Create Simulation
# -----------------------------
@app.route("/create_simulation", methods=["GET", "POST"])
def create_simulation():

    if request.method == "POST":

        name = request.form.get(
            "campaign-name",
            "Untitled Campaign"
        )

        target_group = request.form.get(
            "target-group",
            "Not specified"
        )

        description = request.form.get(
            "description",
            ""
        )

        template = request.form.get(
            "template",
            "Not specified"
        )

        start_date = request.form.get(
            "start-date",
            ""
        )

        duration = request.form.get(
            "duration",
            "7 Days"
        )

        connection = get_db_connection()

        connection.execute("""
            INSERT INTO simulations
            (name, target_group, description, template, start_date, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            target_group,
            description,
            template,
            start_date,
            duration
        ))

        connection.commit()
        connection.close()

        return redirect(url_for("simulations"))

    return render_template("create_simulation.html")


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)