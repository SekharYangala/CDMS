<<<<<<< HEAD
from flask import Flask, jsonify, request
import mysql.connector
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('mysql://ipl_db_mn8l_user:aAH8bBAIppd8n61a688Vta5yCRTZUeWS@host:5432/ipl_db_mn8l')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Cricbase"
)
STAT_QUERIES = {
    "most_runs": """
        SELECT p.name, t.team_name, ps.total_runs AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.total_runs desc limit 15
    """,
    "highest_scores": """
        SELECT p.name, t.team_name, ps.highest_score AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.highest_score DESC LIMIT 15
    """,
    "best_batting_avg": """
        SELECT p.name, t.team_name, ps.batting_avg AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.batting_avg DESC LIMIT 15
    """,
    "most_centuries": """
        SELECT p.name, t.team_name, ps.centuries AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.centuries DESC LIMIT 15
    """,
    "most_fifties": """
        SELECT p.name, t.team_name, ps.fifties AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.fifties DESC LIMIT 15
    """,
    "most_sixes": """
        SELECT p.name, t.team_name, ps.sixes AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.sixes DESC LIMIT 15
    """,
    "most_fours": """
        SELECT p.name, t.team_name, ps.fours AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.fours DESC LIMIT 15
    """,
    "most_wickets": """
        SELECT p.name, t.team_name, ps.wickets AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.wickets DESC LIMIT 15
    """,
    "most_balls_bowled": """
    SELECT p.name, t.team_name, ps.balls_bowled AS stat_value 
    FROM players p 
    JOIN player_stats ps ON p.new_pid = ps.pid 
    JOIN teams t ON p.team_id = t.team_id 
    WHERE ps.balls_bowled > 0
    ORDER BY ps.balls_bowled DESC 
    LIMIT 15
    """,
    "five_wicket_hauls": """
        SELECT p.name, t.team_name, ps.five_wicket_hauls AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.five_wicket_hauls DESC LIMIT 15
    """,

    "Most_matches_played": """
    SELECT p.name, t.team_name, ps.matches_played AS stat_value 
    FROM players p 
    JOIN player_stats ps ON p.new_pid = ps.pid 
    JOIN teams t ON p.team_id = t.team_id 
    WHERE ps.matches_played > 0
    ORDER BY ps.matches_played DESC 
    LIMIT 15
    """,
    "best_economy_rate": """
    SELECT p.name, t.team_name, ps.economy_rate AS stat_value 
    FROM players p 
    JOIN player_stats ps ON p.new_pid = ps.pid 
    JOIN teams t ON p.team_id = t.team_id 
    WHERE ps.balls_bowled >= 120 AND ps.economy_rate > 0 
    ORDER BY ps.economy_rate ASC 
    LIMIT 15
"""

}

# ✅ Fetch All Teams
@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teams")
        teams = cursor.fetchall()
        cursor.close()
        return jsonify(teams)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Players with Filtering
@app.route('/players', methods=['GET'])
def get_players():
    try:
        team_id = request.args.get('team_id')
        search_query = request.args.get('search', '')

        query = """
            SELECT p.pid, p.name, p.age, r.type AS role, p.current_price
            FROM players p
            LEFT JOIN roles r ON p.role_id = r.role_id
        """
        params = []

        if team_id:
            query += " WHERE p.team_id = %s"
            params.append(team_id)

        if search_query:
            query += " AND p.name LIKE %s" if team_id else " WHERE p.name LIKE %s"
            params.append(f"%{search_query}%")

        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params)
        players = cursor.fetchall()
        cursor.close()
        return jsonify(players)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/team_stats', methods=['GET'])
def get_team_stats():
    try:
        team_name = request.args.get('team_name', '')  # Match the frontend parameter

        if not team_name:
            return jsonify({"error": "Team name is required"}), 400

        query = """
            SELECT 
                p.team_name,
                SUM(p.no_of_wins) AS total_wins,
                SUM(p.no_of_matches) AS total_matches,
                t.no_of_cups,
                t.home_ground,
                ROUND((SUM(p.no_of_wins) / SUM(p.no_of_matches)) * 100, 2) AS win_percentage
            FROM 
                pointstable p
            JOIN 
                teams t ON p.team_name = t.team_name
            WHERE 
                p.team_name LIKE %s
            GROUP BY 
                p.team_name, t.no_of_cups;
        """

        search_term = f"%{team_name}%"
        print(f"🔍 Searching for team: {search_term}")  # Debugging log
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (search_term,))
        result = cursor.fetchall()
        cursor.close()

        print(f"📊 Query Result: {result}")  # Debugging log

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/player_stats', methods=['GET'])
def get_player_stats():
    try:
        player_name = request.args.get('name', '').strip()
        print(f"🔍 Received Player Name: {player_name}")  # Debug input

        if not player_name:
            return jsonify({"error": "Player name cannot be empty"}), 400

        query = """
            SELECT 
                p.name AS player_name,
                p.role_id,
                ps.matches_played,
                ps.total_runs,
                ps.wickets,
                ps.batting_avg,
                ps.bowling_avg,
                ps.fours,
                ps.sixes,
                ps.highest_score,
                ps.economy_rate,
                ps.runs_conceded,
                ps.bowling_strike,
                ps.balls_bowled,
                ps.fifties,
                ps.centuries,
                ps.no_of_stumpings,
                ps.four_wicket_haul,
                ps.five_wicket_hauls
            FROM players AS p
            JOIN player_stats AS ps ON ps.pid = p.new_pid  -- ✅ FIX: Match new_pid with pid
            WHERE p.name LIKE %s;
        """

        print(f"📄 Executing Query: {query}")  # Debug query
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (f"%{player_name}%",))
        result = cursor.fetchall()
        cursor.close()

        print(f"📊 Query Result: {result}")  # Debug fetched data
        
        return jsonify(result)  # Return JSON response

    except Exception as e:
        print(f"❌ Error: {e}")  # Debug errors
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Points Table for a Given Year
@app.route('/points_table', methods=['GET'])
def get_points_table():
    try:
        year = request.args.get('year')

        if not year:
            return jsonify({"error": "Year parameter is required"}), 400

        query = """
            SELECT * FROM pointstable 
            WHERE syear = %s 
            ORDER BY position ASC;
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (year,))
        points_table = cursor.fetchall()
        cursor.close()

        return jsonify(points_table)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Playoff Teams for a Given Year (Top 4 Teams)
@app.route('/playoffs', methods=['GET'])
def get_playoff_teams():
    try:
        year = request.args.get('year')

        if not year:
            return jsonify({"error": "Year parameter is required"}), 400

        query = """
            SELECT * FROM pointstable 
            WHERE syear = %s 
            ORDER BY position ASC 
            LIMIT 4;
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (year,))
        playoff_teams = cursor.fetchall()
        cursor.close()

        return jsonify(playoff_teams)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/stats', methods=['GET'])
def get_stats():
    category = request.args.get('category')

    if category not in STAT_QUERIES:
        return jsonify({"error": "Invalid category"}), 400

    query = STAT_QUERIES[category]

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@app.route('/teamvsteam', methods=['GET'])
def team_vs_team_stats():
    try:
        team1 = request.args.get('team1', '').strip()
        team2 = request.args.get('team2', '').strip()

        if not team1 or not team2:
            return jsonify({"error": "Both team1 and team2 are required"}), 400

        cursor = db.cursor(dictionary=True)

        query = """
            SELECT 
                COUNT(*) AS matches_played,
                SUM(CASE WHEN winteam_name = %s THEN 1 ELSE 0 END) AS team1_wins,
                SUM(CASE WHEN winteam_name = %s THEN 1 ELSE 0 END) AS team2_wins
            FROM matches
            WHERE (team1_name = %s AND team2_name = %s)
               OR (team1_name = %s AND team2_name = %s);
        """

        cursor.execute(query, (team1, team2, team1, team2, team2, team1))
        result = cursor.fetchone()
        cursor.close()

        return jsonify({
            "team1": team1,
            "team2": team2,
            "matches_played": result["matches_played"],
            f"{team1}_wins": result["team1_wins"],
            f"{team2}_wins": result["team2_wins"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add_match", methods=["POST"])
def add_match():
    try:
        data = request.json  # Get data from frontend
        match_no = data.get("match_no")
        season_year = data.get("season_year")
        team1_name = data.get("team1_name")
        team2_name = data.get("team2_name")
        winteam_name = data.get("winteam_name")
        u_id = data.get("u_id")
        stadium = data.get("stadium")

        # Validate input fields
        if not all([match_no, season_year, team1_name, team2_name, stadium]):
            return jsonify({"error": "Missing required fields"}), 400

        if str(season_year) != "2025":
            return jsonify({"error": "Only 2025 matches can be added"}), 400

        if team1_name == team2_name:
            return jsonify({"error": "Team 1 and Team 2 cannot be the same"}), 400
        cursor = db.cursor(dictionary=True)
        # Check if match_no and season_year combination already exists
        cursor.execute("SELECT * FROM matches WHERE match_no = %s AND season_year = %s", (match_no, season_year))
        existing_match = cursor.fetchone()

        if existing_match:
            return jsonify({"error": "This match number already exists for 2025"}), 400

        # Insert match into MySQL
        insert_query = """
            INSERT INTO matches (match_no, season_year, team1_name, team2_name, winteam_name, u_id, stadium) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (match_no, season_year, team1_name, team2_name, winteam_name, u_id, stadium)
        cursor.execute(insert_query, values)
        db.commit()

        return jsonify({"message": "Match added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/update_player_stats', methods=['POST'])
def update_player_stats():
    try:
        data = request.json  # Get JSON data from frontend
        player_name = data.get("player_name", "").strip()  # Strip spaces
        updated_stats = data.get("stats", {})

        print(f"📥 Received Player Name: '{player_name}'")  # Debugging log
        print(f"📊 Received Stats: {updated_stats}")  # Debugging log

        if not player_name:
            return jsonify({"error": "Player name is required"}), 400

        if not updated_stats:
            return jsonify({"error": "No stats provided to update"}), 400

        cursor = db.cursor(dictionary=True)

        # 🔍 Ensure player_name is properly formatted and exists
        query = "SELECT new_pid FROM players WHERE name LIKE %s"
        cursor.execute(query, (f"%{player_name}%",))  # Allow partial matching

        player = cursor.fetchone()

        if not player:
            print(f"❌ Player Not Found in DB: '{player_name}'")  # Debugging log
            return jsonify({"error": "Player not found"}), 404

        player_id = player["new_pid"]
        print(f" Player Found! ID: {player_id}")

        # 🔄 Construct UPDATE query dynamically
        update_query = "UPDATE player_stats SET "
        update_values = []

        for key, value in updated_stats.items():
            if value:  # Ensure we only update non-empty values
                update_query += f"{key} = %s, "
                update_values.append(value)

        # If no valid fields to update, return an error
        if not update_values:
            return jsonify({"error": "No valid stats to update"}), 400

        # Remove last comma and space, then add WHERE condition
        update_query = update_query.rstrip(", ") + " WHERE pid = %s"
        update_values.append(player_id)

        print(f"📝 Final Query: {update_query}")  # Debugging log
        print(f"📨 Values: {tuple(update_values)}")  # Debugging log

        cursor.execute(update_query, tuple(update_values))
        db.commit()

        return jsonify({"message": "Player stats updated successfully!"})

    except mysql.connector.Error as sql_error:
        print(f"⚠️ SQL Error: {sql_error}")
        return jsonify({"error": f"SQL Error: {str(sql_error)}"}), 500

    except Exception as e:
        print(f"🚨 Unexpected Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
=======
from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="Cricbase"
)
STAT_QUERIES = {
    "most_runs": """
        SELECT p.name, t.team_name, ps.total_runs AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.total_runs desc limit 15
    """,
    "highest_scores": """
        SELECT p.name, t.team_name, ps.highest_score AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.highest_score DESC LIMIT 15
    """,
    "best_batting_avg": """
        SELECT p.name, t.team_name, ps.batting_avg AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.batting_avg DESC LIMIT 15
    """,
    "most_centuries": """
        SELECT p.name, t.team_name, ps.centuries AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.centuries DESC LIMIT 15
    """,
    "most_fifties": """
        SELECT p.name, t.team_name, ps.fifties AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.fifties DESC LIMIT 15
    """,
    "most_sixes": """
        SELECT p.name, t.team_name, ps.sixes AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.sixes DESC LIMIT 15
    """,
    "most_fours": """
        SELECT p.name, t.team_name, ps.fours AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.fours DESC LIMIT 15
    """,
    "most_wickets": """
        SELECT p.name, t.team_name, ps.wickets AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.wickets DESC LIMIT 15
    """,
    "most_balls_bowled": """
    SELECT p.name, t.team_name, ps.balls_bowled AS stat_value 
    FROM players p 
    JOIN player_stats ps ON p.new_pid = ps.pid 
    JOIN teams t ON p.team_id = t.team_id 
    WHERE ps.balls_bowled > 0
    ORDER BY ps.balls_bowled DESC 
    LIMIT 15
    """,
    "five_wicket_hauls": """
        SELECT p.name, t.team_name, ps.five_wicket_hauls AS stat_value 
        FROM players p 
        JOIN player_stats ps ON p.new_pid = ps.pid 
        JOIN teams t ON p.team_id = t.team_id 
        ORDER BY ps.five_wicket_hauls DESC LIMIT 15
    """,

    "Most_matches_played": """
    SELECT p.name, t.team_name, ps.matches_played AS stat_value 
    FROM players p 
    JOIN player_stats ps ON p.new_pid = ps.pid 
    JOIN teams t ON p.team_id = t.team_id 
    WHERE ps.matches_played > 0
    ORDER BY ps.matches_played DESC 
    LIMIT 15
    """,
    "best_economy_rate": """
    SELECT p.name, t.team_name, ps.economy_rate AS stat_value 
    FROM players p 
    JOIN player_stats ps ON p.new_pid = ps.pid 
    JOIN teams t ON p.team_id = t.team_id 
    WHERE ps.balls_bowled >= 120 AND ps.economy_rate > 0 
    ORDER BY ps.economy_rate ASC 
    LIMIT 15
"""

}

# ✅ Fetch All Teams
@app.route('/teams', methods=['GET'])
def get_teams():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM teams")
        teams = cursor.fetchall()
        cursor.close()
        return jsonify(teams)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Players with Filtering
@app.route('/players', methods=['GET'])
def get_players():
    try:
        team_id = request.args.get('team_id')
        search_query = request.args.get('search', '')

        query = """
            SELECT p.pid, p.name, p.age, r.type AS role, p.current_price
            FROM players p
            LEFT JOIN roles r ON p.role_id = r.role_id
        """
        params = []

        if team_id:
            query += " WHERE p.team_id = %s"
            params.append(team_id)

        if search_query:
            query += " AND p.name LIKE %s" if team_id else " WHERE p.name LIKE %s"
            params.append(f"%{search_query}%")

        cursor = db.cursor(dictionary=True)
        cursor.execute(query, params)
        players = cursor.fetchall()
        cursor.close()
        return jsonify(players)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/team_stats', methods=['GET'])
def get_team_stats():
    try:
        team_name = request.args.get('team_name', '')  # Match the frontend parameter

        if not team_name:
            return jsonify({"error": "Team name is required"}), 400

        query = """
            SELECT 
                p.team_name,
                SUM(p.no_of_wins) AS total_wins,
                SUM(p.no_of_matches) AS total_matches,
                t.no_of_cups,
                t.home_ground,
                ROUND((SUM(p.no_of_wins) / SUM(p.no_of_matches)) * 100, 2) AS win_percentage
            FROM 
                pointstable p
            JOIN 
                teams t ON p.team_name = t.team_name
            WHERE 
                p.team_name LIKE %s
            GROUP BY 
                p.team_name, t.no_of_cups;
        """

        search_term = f"%{team_name}%"
        print(f"🔍 Searching for team: {search_term}")  # Debugging log
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (search_term,))
        result = cursor.fetchall()
        cursor.close()

        print(f"📊 Query Result: {result}")  # Debugging log

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/player_stats', methods=['GET'])
def get_player_stats():
    try:
        player_name = request.args.get('name', '').strip()
        print(f"🔍 Received Player Name: {player_name}")  # Debug input

        if not player_name:
            return jsonify({"error": "Player name cannot be empty"}), 400

        query = """
            SELECT 
                p.name AS player_name,
                p.role_id,
                ps.matches_played,
                ps.total_runs,
                ps.wickets,
                ps.batting_avg,
                ps.bowling_avg,
                ps.fours,
                ps.sixes,
                ps.highest_score,
                ps.economy_rate,
                ps.runs_conceded,
                ps.bowling_strike,
                ps.balls_bowled,
                ps.fifties,
                ps.centuries,
                ps.no_of_stumpings,
                ps.four_wicket_haul,
                ps.five_wicket_hauls
            FROM players AS p
            JOIN player_stats AS ps ON ps.pid = p.new_pid  -- ✅ FIX: Match new_pid with pid
            WHERE p.name LIKE %s;
        """

        print(f"📄 Executing Query: {query}")  # Debug query
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (f"%{player_name}%",))
        result = cursor.fetchall()
        cursor.close()

        print(f"📊 Query Result: {result}")  # Debug fetched data
        
        return jsonify(result)  # Return JSON response

    except Exception as e:
        print(f"❌ Error: {e}")  # Debug errors
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Points Table for a Given Year
@app.route('/points_table', methods=['GET'])
def get_points_table():
    try:
        year = request.args.get('year')

        if not year:
            return jsonify({"error": "Year parameter is required"}), 400

        query = """
            SELECT * FROM pointstable 
            WHERE syear = %s 
            ORDER BY position ASC;
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (year,))
        points_table = cursor.fetchall()
        cursor.close()

        return jsonify(points_table)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Playoff Teams for a Given Year (Top 4 Teams)
@app.route('/playoffs', methods=['GET'])
def get_playoff_teams():
    try:
        year = request.args.get('year')

        if not year:
            return jsonify({"error": "Year parameter is required"}), 400

        query = """
            SELECT * FROM pointstable 
            WHERE syear = %s 
            ORDER BY position ASC 
            LIMIT 4;
        """
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (year,))
        playoff_teams = cursor.fetchall()
        cursor.close()

        return jsonify(playoff_teams)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/stats', methods=['GET'])
def get_stats():
    category = request.args.get('category')

    if category not in STAT_QUERIES:
        return jsonify({"error": "Invalid category"}), 400

    query = STAT_QUERIES[category]

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)

    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    
@app.route('/teamvsteam', methods=['GET'])
def team_vs_team_stats():
    try:
        team1 = request.args.get('team1', '').strip()
        team2 = request.args.get('team2', '').strip()

        if not team1 or not team2:
            return jsonify({"error": "Both team1 and team2 are required"}), 400

        cursor = db.cursor(dictionary=True)

        query = """
            SELECT 
                COUNT(*) AS matches_played,
                SUM(CASE WHEN winteam_name = %s THEN 1 ELSE 0 END) AS team1_wins,
                SUM(CASE WHEN winteam_name = %s THEN 1 ELSE 0 END) AS team2_wins
            FROM matches
            WHERE (team1_name = %s AND team2_name = %s)
               OR (team1_name = %s AND team2_name = %s);
        """

        cursor.execute(query, (team1, team2, team1, team2, team2, team1))
        result = cursor.fetchone()
        cursor.close()

        return jsonify({
            "team1": team1,
            "team2": team2,
            "matches_played": result["matches_played"],
            f"{team1}_wins": result["team1_wins"],
            f"{team2}_wins": result["team2_wins"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add_match", methods=["POST"])
def add_match():
    try:
        data = request.json  # Get data from frontend
        match_no = data.get("match_no")
        season_year = data.get("season_year")
        team1_name = data.get("team1_name")
        team2_name = data.get("team2_name")
        winteam_name = data.get("winteam_name")
        u_id = data.get("u_id")
        stadium = data.get("stadium")

        # Validate input fields
        if not all([match_no, season_year, team1_name, team2_name, stadium]):
            return jsonify({"error": "Missing required fields"}), 400

        if str(season_year) != "2025":
            return jsonify({"error": "Only 2025 matches can be added"}), 400

        if team1_name == team2_name:
            return jsonify({"error": "Team 1 and Team 2 cannot be the same"}), 400
        cursor = db.cursor(dictionary=True)
        # Check if match_no and season_year combination already exists
        cursor.execute("SELECT * FROM matches WHERE match_no = %s AND season_year = %s", (match_no, season_year))
        existing_match = cursor.fetchone()

        if existing_match:
            return jsonify({"error": "This match number already exists for 2025"}), 400

        # Insert match into MySQL
        insert_query = """
            INSERT INTO matches (match_no, season_year, team1_name, team2_name, winteam_name, u_id, stadium) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (match_no, season_year, team1_name, team2_name, winteam_name, u_id, stadium)
        cursor.execute(insert_query, values)
        db.commit()

        return jsonify({"message": "Match added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/update_player_stats', methods=['POST'])
def update_player_stats():
    try:
        data = request.json  # Get JSON data from frontend
        player_name = data.get("player_name", "").strip()  # Strip spaces
        updated_stats = data.get("stats", {})

        print(f"📥 Received Player Name: '{player_name}'")  # Debugging log
        print(f"📊 Received Stats: {updated_stats}")  # Debugging log

        if not player_name:
            return jsonify({"error": "Player name is required"}), 400

        if not updated_stats:
            return jsonify({"error": "No stats provided to update"}), 400

        cursor = db.cursor(dictionary=True)

        # 🔍 Ensure player_name is properly formatted and exists
        query = "SELECT new_pid FROM players WHERE name LIKE %s"
        cursor.execute(query, (f"%{player_name}%",))  # Allow partial matching

        player = cursor.fetchone()

        if not player:
            print(f"❌ Player Not Found in DB: '{player_name}'")  # Debugging log
            return jsonify({"error": "Player not found"}), 404

        player_id = player["new_pid"]
        print(f" Player Found! ID: {player_id}")

        # 🔄 Construct UPDATE query dynamically
        update_query = "UPDATE player_stats SET "
        update_values = []

        for key, value in updated_stats.items():
            if value:  # Ensure we only update non-empty values
                update_query += f"{key} = %s, "
                update_values.append(value)

        # If no valid fields to update, return an error
        if not update_values:
            return jsonify({"error": "No valid stats to update"}), 400

        # Remove last comma and space, then add WHERE condition
        update_query = update_query.rstrip(", ") + " WHERE pid = %s"
        update_values.append(player_id)

        print(f"📝 Final Query: {update_query}")  # Debugging log
        print(f"📨 Values: {tuple(update_values)}")  # Debugging log

        cursor.execute(update_query, tuple(update_values))
        db.commit()

        return jsonify({"message": "Player stats updated successfully!"})

    except mysql.connector.Error as sql_error:
        print(f"⚠️ SQL Error: {sql_error}")
        return jsonify({"error": f"SQL Error: {str(sql_error)}"}), 500

    except Exception as e:
        print(f"🚨 Unexpected Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
>>>>>>> 428c8bdaee0fdf276b8897c3c7eae19a60144c26
    app.run(debug=True, port=5000)
