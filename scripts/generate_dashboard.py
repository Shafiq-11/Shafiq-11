import os
import json
import re

# ==================== SVG TEMPLATES ====================

PROJECT_50_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="250" viewBox="0 0 400 250">
  <defs>
    <linearGradient id="blue-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff" />
      <stop offset="100%" stop-color="#7000ff" />
    </linearGradient>
    <linearGradient id="purple-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#bd00ff" />
      <stop offset="100%" stop-color="#ff0055" />
    </linearGradient>
    <linearGradient id="green-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00ff66" />
      <stop offset="100%" stop-color="#00f0ff" />
    </linearGradient>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c0d14" />
      <stop offset="100%" stop-color="#05060a" />
    </linearGradient>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;display=swap');
    .title {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 15px;
      fill: #ffffff;
      letter-spacing: 1px;
    }
    .subtitle {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 11px;
      fill: #ff0055;
    }
    .label {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 13px;
      fill: #a0a5c0;
    }
    .percent {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 13px;
      fill: #ffffff;
      text-anchor: end;
    }
    .card-border {
      stroke: #1c1f30;
      stroke-width: 1.5;
      fill: url(#bg-grad);
      rx: 12;
    }
    .progress-bg {
      fill: #141724;
      rx: 3;
    }
  </style>

  <rect class="card-border" width="398" height="248" x="1" y="1" />
  
  <!-- Header -->
  <text class="title" x="25" y="35">⚡ PROJECT 50 CONTROL PANEL</text>
  <text class="subtitle" x="375" y="35" text-anchor="end">DAY {{day}}/50</text>
  
  <line x1="25" y1="48" x2="375" y2="48" stroke="#1c1f30" stroke-width="1"/>

  <!-- Coding -->
  <g transform="translate(25, 60)">
    <text class="label" x="0" y="15">Coding</text>
    <text class="percent" x="350" y="15">{{coding}}%</text>
    <rect class="progress-bg" x="0" y="24" width="350" height="8" />
    <rect x="0" y="24" width="{{coding_w}}" height="8" rx="3" fill="url(#blue-grad)"/>
  </g>

  <!-- DSA -->
  <g transform="translate(25, 95)">
    <text class="label" x="0" y="15">DSA Practice</text>
    <text class="percent" x="350" y="15">{{dsa}}%</text>
    <rect class="progress-bg" x="0" y="24" width="350" height="8" />
    <rect x="0" y="24" width="{{dsa_w}}" height="8" rx="3" fill="url(#purple-grad)"/>
  </g>

  <!-- Gym -->
  <g transform="translate(25, 130)">
    <text class="label" x="0" y="15">Gym Consistency</text>
    <text class="percent" x="350" y="15">{{gym}}%</text>
    <rect class="progress-bg" x="0" y="24" width="350" height="8" />
    <rect x="0" y="24" width="{{gym_w}}" height="8" rx="3" fill="url(#green-grad)"/>
  </g>

  <!-- Projects -->
  <g transform="translate(25, 165)">
    <text class="label" x="0" y="15">Build Projects</text>
    <text class="percent" x="350" y="15">{{projects}}%</text>
    <rect class="progress-bg" x="0" y="24" width="350" height="8" />
    <rect x="0" y="24" width="{{projects_w}}" height="8" rx="3" fill="url(#blue-grad)"/>
  </g>

  <!-- Learning -->
  <g transform="translate(25, 200)">
    <text class="label" x="0" y="15">Continuous Learning</text>
    <text class="percent" x="350" y="15">{{learning}}%</text>
    <rect class="progress-bg" x="0" y="24" width="350" height="8" />
    <rect x="0" y="24" width="{{learning_w}}" height="8" rx="3" fill="url(#purple-grad)"/>
  </g>
</svg>"""

BIKE_PROGRESS_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="110" viewBox="0 0 400 110">
  <defs>
    <linearGradient id="path-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#bd00ff" />
      <stop offset="50%" stop-color="#00f0ff" />
      <stop offset="100%" stop-color="#00ff66" />
    </linearGradient>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c0d14" />
      <stop offset="100%" stop-color="#05060a" />
    </linearGradient>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;display=swap');
    .title {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 13px;
      fill: #ffffff;
      letter-spacing: 0.8px;
    }
    .desc {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 11px;
      fill: #a0a5c0;
    }
    .stat {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 11px;
      fill: #00f0ff;
    }
    .card-border {
      stroke: #1c1f30;
      stroke-width: 1.5;
      fill: url(#bg-grad);
      rx: 12;
    }
    .path-bg {
      stroke: #141724;
      stroke-width: 4;
      stroke-linecap: round;
    }
    .path-fill {
      stroke: url(#path-grad);
      stroke-width: 4;
      stroke-linecap: round;
    }
    .bike-icon {
      font-size: 16px;
    }
  </style>

  <rect class="card-border" width="398" height="108" x="1" y="1" />

  <!-- Header -->
  <text class="title" x="20" y="28">🏍 REBORN MOTORS PROGRESS TRACK</text>
  <text class="stat" x="380" y="28" text-anchor="end">{{distance}} / {{target}} KM</text>

  <!-- Track Line -->
  <g transform="translate(20, 50)">
    <line class="path-bg" x1="10" y1="15" x2="350" y2="15" />
    <line class="path-fill" x1="10" y1="15" x2="{{progress_x}}" y2="15" />
    
    <!-- Start Flag -->
    <text x="0" y="20" font-size="12">🏡</text>
    
    <!-- End Flag -->
    <text x="350" y="20" font-size="12">🏁</text>
    
    <!-- Bike Marker -->
    <g transform="translate({{bike_x}}, 0)">
      <text class="bike-icon" x="-10" y="13">🏍</text>
      <text x="-4" y="28" font-size="9" fill="#00ff66" font-family="'Outfit', sans-serif" font-weight="bold" text-anchor="middle">{{progress}}%</text>
    </g>
  </g>
  
  <text class="desc" x="20" y="98">Current Status: <tspan fill="#00ff66" font-weight="bold">{{status}}</tspan></text>
</svg>"""

WORKOUT_PROGRESS_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="400" height="110" viewBox="0 0 400 110">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0c0d14" />
      <stop offset="100%" stop-color="#05060a" />
    </linearGradient>
    <linearGradient id="bar-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff0055" />
      <stop offset="100%" stop-color="#bd00ff" />
    </linearGradient>
  </defs>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;display=swap');
    .title {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 13px;
      fill: #ffffff;
      letter-spacing: 0.8px;
    }
    .desc {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 11px;
      fill: #a0a5c0;
    }
    .stat {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 12px;
      fill: #ff0055;
    }
    .card-border {
      stroke: #1c1f30;
      stroke-width: 1.5;
      fill: url(#bg-grad);
      rx: 12;
    }
  </style>

  <rect class="card-border" width="398" height="108" x="1" y="1" />

  <!-- Header -->
  <text class="title" x="20" y="28">💪 WORKOUT CONSISTENCY RADAR</text>
  <text class="stat" x="380" y="28" text-anchor="end">{{consistency}}% CONSISTENT</text>

  <!-- Consistency blocks representing workouts -->
  <g transform="translate(20, 42)">
    <!-- 10 blocks representing consistency -->
    {{blocks}}
  </g>

  <!-- Additional Stats -->
  <text class="desc" x="20" y="96">Sessions: <tspan fill="#ff0055" font-weight="bold">{{sessions}} / month</tspan></text>
  <text class="desc" x="220" y="96">Current Streak: <tspan fill="#bd00ff" font-weight="bold">{{streak}} days</tspan></text>
</svg>"""

# ==================== MAIN COMPILATION ====================

def main():
    script_dir = os.path.dirname(__file__)
    stats_path = os.path.join(script_dir, "stats.json")
    
    # Check if stats.json exists, otherwise write default stats first
    if not os.path.exists(stats_path):
        print("stats.json not found, running fetch_stats.py to generate...")
        from fetch_stats import main as run_fetch
        run_fetch()
        
    with open(stats_path, "r", encoding="utf-8") as f:
        stats = json.load(f)
        
    # Create target directory for SVGs
    svg_dir = os.path.join(script_dir, "..", "svg")
    os.makedirs(svg_dir, exist_ok=True)
    
    print("Generating dynamic dashboards...")
    
    # 1. Project 50 Dashboard
    p50 = stats["project50"]
    p50_svg = PROJECT_50_TEMPLATE
    p50_svg = p50_svg.replace("{{day}}", str(p50["day"]))
    p50_svg = p50_svg.replace("{{coding}}", str(p50["coding"]))
    p50_svg = p50_svg.replace("{{coding_w}}", str(int(p50["coding"] * 3.5)))
    p50_svg = p50_svg.replace("{{dsa}}", str(p50["dsa"]))
    p50_svg = p50_svg.replace("{{dsa_w}}", str(int(p50["dsa"] * 3.5)))
    p50_svg = p50_svg.replace("{{gym}}", str(p50["gym"]))
    p50_svg = p50_svg.replace("{{gym_w}}", str(int(p50["gym"] * 3.5)))
    p50_svg = p50_svg.replace("{{projects}}", str(p50["projects"]))
    p50_svg = p50_svg.replace("{{projects_w}}", str(int(p50["projects"] * 3.5)))
    p50_svg = p50_svg.replace("{{learning}}", str(p50["learning"]))
    p50_svg = p50_svg.replace("{{learning_w}}", str(int(p50["learning"] * 3.5)))
    
    with open(os.path.join(svg_dir, "project-50-dashboard.svg"), "w", encoding="utf-8") as f:
        f.write(p50_svg)
    print("Created project-50-dashboard.svg")
        
    # 2. Bike Progress
    bike = stats["bike"]
    prog_x = 10 + int((bike["progress"] / 100.0) * 340)
    bike_x = 10 + int((bike["progress"] / 100.0) * 340)
    
    bike_svg = BIKE_PROGRESS_TEMPLATE
    bike_svg = bike_svg.replace("{{distance}}", str(bike["distance_completed"]))
    bike_svg = bike_svg.replace("{{target}}", str(bike["target_distance"]))
    bike_svg = bike_svg.replace("{{progress_x}}", str(prog_x))
    bike_svg = bike_svg.replace("{{bike_x}}", str(bike_x))
    bike_svg = bike_svg.replace("{{progress}}", str(bike["progress"]))
    bike_svg = bike_svg.replace("{{status}}", str(bike["status"]))
    
    with open(os.path.join(svg_dir, "bike-progress.svg"), "w", encoding="utf-8") as f:
        f.write(bike_svg)
    print("Created bike-progress.svg")
        
    # 3. Workout Progress
    workout = stats["workout"]
    consistency = workout["consistency"]
    
    # Build 10 blocks (32px wide, 20px high each, spaced by 4px)
    blocks_str = ""
    active_blocks = int(consistency / 10)
    for i in range(10):
        x = i * 36
        color = "url(#bar-grad)" if i < active_blocks else "#141724"
        blocks_str += f'<rect x="{x}" y="10" width="32" height="20" rx="4" fill="{color}"/>\n    '
        
    workout_svg = WORKOUT_PROGRESS_TEMPLATE
    workout_svg = workout_svg.replace("{{consistency}}", str(consistency))
    workout_svg = workout_svg.replace("{{blocks}}", blocks_str.strip())
    workout_svg = workout_svg.replace("{{sessions}}", str(workout["sessions_this_month"]))
    workout_svg = workout_svg.replace("{{streak}}", str(workout["current_streak"]))
    
    with open(os.path.join(svg_dir, "workout-progress.svg"), "w", encoding="utf-8") as f:
        f.write(workout_svg)
    print("Created workout-progress.svg")
    
    # 4. Update README.md stats dynamic block
    update_readme(stats)

def update_readme(stats):
    """
    Updates dynamic statistical indicators directly inside README.md if it exists.
    """
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    if not os.path.exists(readme_path):
        print("README.md not found, skipping inline README replacement. Will be populated on creation.")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Format developer dashboard items
    github = stats["github"]
    leetcode = stats["leetcode"]
    wakatime = stats["wakatime"]
    
    # Create Markdown table/block for stats replacement
    stats_replacement = f"""<!-- STATS_START -->
<table>
  <tr>
    <td width="50%">
      <h3>💻 Wakatime Coding Stats</h3>
      <ul>
        <li><strong>Weekly hours:</strong> {wakatime["total_hours"]}</li>
        <li><strong>Daily average:</strong> {wakatime["daily_average"]}</li>
        <li><strong>Top language:</strong> {wakatime["languages"][0]["name"]} ({wakatime["languages"][0]["percent"]}%)</li>
        <li><strong>Second language:</strong> {wakatime["languages"][1]["name"]} ({wakatime["languages"][1]["percent"]}%)</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🧠 LeetCode DSA Metrics</h3>
      <ul>
        <li><strong>Total Solved:</strong> {leetcode["all"]}</li>
        <li><strong>Easy:</strong> {leetcode["easy"]} 🟢</li>
        <li><strong>Medium:</strong> {leetcode["medium"]} 🟡</li>
        <li><strong>Hard:</strong> {leetcode["hard"]} 🔴</li>
      </ul>
    </td>
  </tr>
</table>
<!-- STATS_END -->"""

    # Use regex to find and replace STATS block
    pattern = r"<!-- STATS_START -->.*?<!-- STATS_END -->"
    if re.search(pattern, content, re.DOTALL):
        updated_content = re.sub(pattern, stats_replacement, content, flags=re.DOTALL)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Successfully updated statistics inside README.md")
    else:
        print("STATS markers not found in README.md, skipping inline replacement.")

if __name__ == "__main__":
    main()
