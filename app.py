from multiprocessing.dummy import connection
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import random
import pickle

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

    connection.execute("""
        CREATE TABLE IF NOT EXISTS campaign_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER NOT NULL,
            participants INTEGER DEFAULT 0,
            emails_delivered INTEGER DEFAULT 0,
            emails_opened INTEGER DEFAULT 0,
            links_clicked INTEGER DEFAULT 0,
            reported INTEGER DEFAULT 0,
            awareness_score REAL DEFAULT 0,
            FOREIGN KEY (simulation_id) REFERENCES simulations(id)
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
    ai_result = request.args.get("ai_result")

    connection = get_db_connection()

    # Total number of simulations
    total_simulations = connection.execute("""
        SELECT COUNT(*) FROM simulations
    """).fetchone()[0]

    # Total participants
    total_participants = connection.execute("""
        SELECT COALESCE(SUM(participants), 0)
        FROM campaign_metrics
    """).fetchone()[0]

    # Total delivered emails
    total_delivered = connection.execute("""
        SELECT COALESCE(SUM(emails_delivered), 0)
        FROM campaign_metrics
    """).fetchone()[0]

    # Total opened emails
    total_opened = connection.execute("""
        SELECT COALESCE(SUM(emails_opened), 0)
        FROM campaign_metrics
    """).fetchone()[0]

    # Total clicked links
    total_clicked = connection.execute("""
        SELECT COALESCE(SUM(links_clicked), 0)
        FROM campaign_metrics
    """).fetchone()[0]

    # Total reported emails
    total_reported = connection.execute("""
        SELECT COALESCE(SUM(reported), 0)
        FROM campaign_metrics
    """).fetchone()[0]

    # Phishing click rate
    if total_delivered > 0:
        click_rate = (total_clicked / total_delivered) * 100
    else:
        click_rate = 0

    # Average awareness score
    awareness_score = connection.execute("""
        SELECT COALESCE(AVG(awareness_score), 0)
        FROM campaign_metrics
    """).fetchone()[0]

            # Risk Distribution
    high_risk = connection.execute("""
        SELECT COUNT(*)
        FROM simulations s
        LEFT JOIN campaign_metrics cm
            ON s.id = cm.simulation_id
        WHERE cm.participants > 0
        AND (cm.links_clicked * 100.0 / cm.participants) >= 50
    """).fetchone()[0]

    medium_risk = connection.execute("""
        SELECT COUNT(*)
        FROM simulations s
        LEFT JOIN campaign_metrics cm
            ON s.id = cm.simulation_id
        WHERE cm.participants > 0
        AND (cm.links_clicked * 100.0 / cm.participants) >= 25
        AND (cm.links_clicked * 100.0 / cm.participants) < 50
    """).fetchone()[0]

    low_risk = connection.execute("""
        SELECT COUNT(*)
        FROM simulations s
        LEFT JOIN campaign_metrics cm
            ON s.id = cm.simulation_id
        WHERE cm.participants IS NULL
        OR cm.participants = 0
        OR (cm.links_clicked * 100.0 / cm.participants) < 25
    """).fetchone()[0]

    # Recent Simulations
    recent_simulations = connection.execute("""
        SELECT *
        FROM simulations
        ORDER BY id DESC
        LIMIT 5
    """).fetchall()

    connection.close()

    return render_template(
        "index.html",
        total_simulations=total_simulations,
        total_participants=total_participants,
        click_rate=click_rate,
        awareness_score=awareness_score,
        total_delivered=total_delivered,
        total_opened=total_opened,
        total_clicked=total_clicked,
        total_reported=total_reported,
        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,
        recent_simulations=recent_simulations,
        ai_result=ai_result
    )

# AI Email Analyzer
@app.route("/analyze_email", methods=["POST"])
def analyze_email():
    email_text = request.form.get("email_text", "").strip()

    if not email_text:
        return redirect(url_for("home"))

    with open("ai/phishing_model.pkl", "rb") as file:
        model = pickle.load(file)

    with open("ai/tfidf_vectorizer.pkl", "rb") as file:
        vectorizer = pickle.load(file)

    email_vector = vectorizer.transform([email_text])
    prediction = model.predict(email_vector)[0]

    return redirect(
        url_for(
            "home",
            ai_result=prediction
        )
    )


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

    # Get campaign details
    simulation = connection.execute(
        "SELECT * FROM simulations WHERE id = ?",
        (simulation_id,)
    ).fetchone()

    if simulation is None:
        connection.close()
        return "Simulation not found", 404

    # Get campaign metrics
    metrics = connection.execute(
        """
        SELECT *
        FROM campaign_metrics
        WHERE simulation_id = ?
        """,
        (simulation_id,)
    ).fetchone()

    # Create simulated metrics if this campaign has none
    if metrics is None:

        participants = 100
        emails_delivered = 100
        emails_opened = 72
        links_clicked = 30
        reported = 42
        awareness_score = 70.0

        connection.execute(
            """
            INSERT INTO campaign_metrics
            (
                simulation_id,
                participants,
                emails_delivered,
                emails_opened,
                links_clicked,
                reported,
                awareness_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                simulation_id,
                participants,
                emails_delivered,
                emails_opened,
                links_clicked,
                reported,
                awareness_score
            )
        )

        connection.commit()

        # Fetch the newly created metrics
        metrics = connection.execute(
            """
            SELECT *
            FROM campaign_metrics
            WHERE simulation_id = ?
            """,
            (simulation_id,)
        ).fetchone()

    connection.close()

    return render_template(
        "simulation_details.html",
        simulation=simulation,
        metrics=metrics
    )


# -----------------------------
# Simulate Campaign Activity
# -----------------------------
@app.route("/simulate/<int:simulation_id>")
def simulate_campaign(simulation_id):

    connection = get_db_connection()

    metrics = connection.execute(
        """
        SELECT * FROM campaign_metrics
        WHERE simulation_id = ?
        """,
        (simulation_id,)
    ).fetchone()

    if metrics is None:
        connection.close()
        return "Campaign metrics not found", 404

    # Generate safe simulated campaign activity
    participants = metrics["participants"]

    # Assign simulated participants if this is a new campaign
    if participants == 0:
        participants = random.randint(80, 150)

    # Simulate email delivery
    emails_delivered = random.randint(
        max(1, participants - 5),
        participants
    )

    # Simulate email opens
    emails_opened = round(emails_delivered * 0.78)

    # Simulate link clicks
    links_clicked = round(emails_opened * 0.40)

    # Simulate reported emails
    reported = round(emails_opened * 0.58)

    # Calculate awareness score
    # Higher reporting and lower clicking = better awareness
    awareness_score = round(
        (
            (reported / emails_opened) * 70
            + (1 - (links_clicked / emails_opened)) * 30
        ),
        1
    ) if emails_opened > 0 else 0

    # Update campaign metrics
    connection.execute(
        """
        UPDATE campaign_metrics
        SET
            participants = ?,
            emails_delivered = ?,
            emails_opened = ?,
            links_clicked = ?,
            reported = ?,
            awareness_score = ?
        WHERE simulation_id = ?
        """,
        (
            participants,
            emails_delivered,
            emails_opened,
            links_clicked,
            reported,
            awareness_score,
            simulation_id
        )
    )

    connection.commit()
    connection.close()

    return redirect(
        url_for(
            "simulation_details",
            simulation_id=simulation_id
        )
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

        cursor = connection.execute("""
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

        simulation_id = cursor.lastrowid

        connection.execute("""
            INSERT INTO campaign_metrics
            (simulation_id, participants, emails_delivered, emails_opened,
             links_clicked, reported, awareness_score)
            VALUES (?, 0, 0, 0, 0, 0, 0)
        """, (simulation_id,))

        connection.commit()
        connection.close()

        return redirect(url_for("simulations"))

    return render_template("create_simulation.html")


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)