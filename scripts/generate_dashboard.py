import os
import json
import re
import shutil

# ==================== SVG TEMPLATES ====================

TYPING_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="500" height="80" viewBox="0 0 500 80">
  <style>
    :root {
      --bg: #0d1117;
      --border: #30363d;
      --accent: #818cf8;
      --text-primary: #f0f6fc;
      --text-secondary: #8b949e;
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #f6f8fa;
        --border: #d1d5db;
        --accent: #4f46e5;
        --text-primary: #1f2937;
        --text-secondary: #4b5563;
      }
    }
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&amp;display=swap');
    .panel {
      fill: var(--bg);
      stroke: var(--border);
      stroke-width: 1.5;
      rx: 8;
    }
    .dot-red { fill: #ff5f56; }
    .dot-yellow { fill: #ffbd2e; }
    .dot-green { fill: #27c93f; }
    
    text {
      font-family: 'Fira Code', monospace;
      font-size: 14px;
      fill: var(--text-primary);
    }
    .terminal-title {
      font-size: 11px;
      fill: var(--text-secondary);
      text-anchor: middle;
    }
    .prompt {
      fill: var(--accent);
      font-weight: bold;
    }
    .cursor {
      fill: var(--accent);
      animation: blink 0.8s infinite steps(2);
    }
    .text-line {
      opacity: 0;
      animation: type-sequence 18s infinite steps(1);
    }
    .line-1 { animation-delay: 0s; }
    .line-2 { animation-delay: 3s; }
    .line-3 { animation-delay: 6s; }
    .line-4 { animation-delay: 9s; }
    .line-5 { animation-delay: 12s; }
    .line-6 { animation-delay: 15s; }
    @keyframes blink {
      0%, 100% { opacity: 0; }
      50% { opacity: 1; }
    }
    @keyframes type-sequence {
      0%, 16.66% { opacity: 1; }
      16.67%, 100% { opacity: 0; }
    }
  </style>
  <rect class="panel" width="498" height="78" x="1" y="1" />
  <circle cx="20" cy="20" r="4" class="dot-red" />
  <circle cx="32" cy="20" r="4" class="dot-yellow" />
  <circle cx="44" cy="20" r="4" class="dot-green" />
  <text class="terminal-title" x="250" y="24">shafiq@command-center:~</text>
  <text class="prompt" x="20" y="55">&gt;</text>
  <g transform="translate(38, 55)">
    <text class="text-line line-1" x="0" y="0">Full Stack Developer</text>
    <text class="text-line line-2" x="0" y="0">Java | Spring Boot | React</text>
    <text class="text-line line-3" x="0" y="0">Building scalable web applications</text>
    <text class="text-line line-4" x="0" y="0">Solving algorithmic problems</text>
    <text class="text-line line-5" x="0" y="0">DSA &amp; LeetCode enthusiast</text>
    <text class="text-line line-6" x="0" y="0">Open to Internship Opportunities 🚀</text>
    <rect class="cursor" x="290" y="-12" width="8" height="14">
      <animate attributeName="x" 
               values="168;219;286;236;210;303" 
               dur="18s" 
               repeatCount="indefinite" 
               calcMode="discrete"/>
    </rect>
  </g>
</svg>"""

LEETCODE_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="500" height="190" viewBox="0 0 500 190">
  <style>
    :root {
      --bg: #0d1117;
      --border: #30363d;
      --text-main: #f0f6fc;
      --text-muted: #8b949e;
      --accent: #818cf8;
      --card-bg: #161b22;
      --bar-bg: #21262d;
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #ffffff;
        --border: #d1d5db;
        --text-main: #1f2937;
        --text-muted: #4b5563;
        --accent: #4f46e5;
        --card-bg: #f6f8fa;
        --bar-bg: #e5e7eb;
      }
    }
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;display=swap');
    .card {
      fill: var(--bg);
      stroke: var(--border);
      stroke-width: 1.5;
      rx: 8;
    }
    .title {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      fill: var(--text-main);
      letter-spacing: 0.5px;
    }
    .subtitle {
      font-family: 'Outfit', sans-serif;
      font-weight: 400;
      font-size: 11px;
      fill: var(--text-muted);
    }
    .num {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 28px;
      fill: var(--text-main);
    }
    .label {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 11px;
      fill: var(--text-muted);
    }
    .val {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 12px;
      fill: var(--text-main);
      text-anchor: end;
    }
    .progress-bg {
      fill: var(--bar-bg);
      rx: 2;
    }
    .progress-easy { fill: #2ea44f; rx: 2; }
    .progress-medium { fill: #dbab09; rx: 2; }
    .progress-hard { fill: #d93535; rx: 2; }
    .divider {
      stroke: var(--border);
      stroke-width: 1;
    }
    .badge-container {
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1;
      rx: 6;
    }
    .stat-box {
      fill: var(--card-bg);
      stroke: var(--border);
      stroke-width: 1;
      rx: 6;
    }
  </style>
  <rect class="card" width="498" height="188" x="1" y="1"/>
  
  <!-- Header -->
  <text class="title" x="25" y="32">🧠 LEETCODE METRICS</text>
  <text class="subtitle" x="475" y="32" text-anchor="end">Practice Dashboard</text>
  
  <line class="divider" x1="25" y1="44" x2="475" y2="44" />
  
  <!-- Solved Problems Column -->
  <g transform="translate(25, 55)">
    <text class="num" x="0" y="30">{{all}}</text>
    <text class="label" x="0" y="44">PROBLEMS SOLVED</text>
    
    <!-- Easy -->
    <g transform="translate(0, 58)">
      <text class="label" x="0" y="10">Easy</text>
      <text class="val" x="180" y="10">{{easy}}</text>
      <rect class="progress-bg" x="0" y="16" width="180" height="4" />
      <rect class="progress-easy" x="0" y="16" width="{{easy_w}}" height="4" />
    </g>
    
    <!-- Medium -->
    <g transform="translate(0, 86)">
      <text class="label" x="0" y="10">Medium</text>
      <text class="val" x="180" y="10">{{medium}}</text>
      <rect class="progress-bg" x="0" y="16" width="180" height="4" />
      <rect class="progress-medium" x="0" y="16" width="{{medium_w}}" height="4" />
    </g>
    
    <!-- Hard -->
    <g transform="translate(0, 114)">
      <text class="label" x="0" y="10">Hard</text>
      <text class="val" x="180" y="10">{{hard}}</text>
      <rect class="progress-bg" x="0" y="16" width="180" height="4" />
      <rect class="progress-hard" x="0" y="16" width="{{hard_w}}" height="4" />
    </g>
  </g>
  
  <line class="divider" x1="240" y1="55" x2="240" y2="175" />
  
  <!-- Contest & Badges Column -->
  <g transform="translate(260, 55)">
    <!-- Contest rating / ranking box -->
    <g transform="translate(0, 0)">
      {{contest_block}}
    </g>
    
    <!-- Badges box -->
    <g transform="translate(0, 68)">
      <rect class="badge-container" width="215" height="52" />
      <text class="label" x="15" y="18">BADGES</text>
      <!-- Dynamic Badge Icons -->
      {{badges_icons}}
    </g>
  </g>
</svg>"""

PROJECT_CARD_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="340" height="120" viewBox="0 0 340 120">
  <style>
    :root {
      --bg: #0d1117;
      --border: #30363d;
      --text-main: #f0f6fc;
      --text-muted: #8b949e;
      --accent: #818cf8;
      --lang-dot: #8b949e;
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #ffffff;
        --border: #d1d5db;
        --text-main: #1f2937;
        --text-muted: #4b5563;
        --accent: #4f46e5;
      }
    }
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;display=swap');
    .card {
      fill: var(--bg);
      stroke: var(--border);
      stroke-width: 1.5;
      rx: 8;
    }
    .title {
      font-family: 'Outfit', sans-serif;
      font-weight: 700;
      font-size: 14px;
      fill: var(--accent);
    }
    .desc {
      font-family: 'Outfit', sans-serif;
      font-weight: 400;
      font-size: 11px;
      fill: var(--text-muted);
    }
    .meta {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 10px;
      fill: var(--text-muted);
    }
    .lang-circle {
      fill: var(--lang-dot);
    }
  </style>
  <rect class="card" width="338" height="118" x="1" y="1"/>
  
  <!-- Repo icon (simplified book/repo logo) -->
  <path d="M 22 22 L 22 34 A 2 2 0 0 0 24 36 L 34 36 L 34 24 L 24 24 A 2 2 0 0 0 22 22 Z" fill="none" stroke="var(--accent)" stroke-width="1.5" />
  <path d="M 24 24 L 34 24" stroke="var(--accent)" stroke-width="1.5" />
  <circle cx="27" cy="29" r="0.8" fill="var(--accent)" />
  
  <!-- Title -->
  <text class="title" x="46" y="32">{{name}}</text>
  
  <!-- Description (split/wrapped) -->
  <text class="desc" x="22" y="58">{{desc1}}</text>
  <text class="desc" x="22" y="73">{{desc2}}</text>
  
  <!-- Footer Meta -->
  <g transform="translate(22, 98)">
    <!-- Language Dot -->
    <circle class="lang-circle" cx="5" cy="-3" r="4" fill="{{lang_color}}" />
    <text class="meta" x="15" y="0">{{language}}</text>
    
    <!-- Stars -->
    <g transform="translate({{stars_x}}, 0)">
      <!-- Star Icon -->
      <path d="M 0,-7 L 1.8,-3 L 5.5,-3 L 2.5,0 L 3.5,4 L 0,2 L -3.5,4 L -2.5,0 L -5.5,-3 L -1.8,-3 Z" fill="var(--text-muted)" />
      <text class="meta" x="9" y="0">{{stars}}</text>
    </g>
    
    <!-- Forks -->
    <g transform="translate({{forks_x}}, 0)">
      <!-- Fork Icon -->
      <circle cx="-3" cy="-7" r="1.2" fill="none" stroke="var(--text-muted)" stroke-width="1" />
      <circle cx="3" cy="-7" r="1.2" fill="none" stroke="var(--text-muted)" stroke-width="1" />
      <circle cx="0" cy="1" r="1.2" fill="none" stroke="var(--text-muted)" stroke-width="1" />
      <path d="M -3,-5 L -3,-3 A 1.5 1.5 0 0 0 -1.5,-1.5 L 1.5,-1.5 A 1.5 1.5 0 0 0 3,-3 L 3,-5" fill="none" stroke="var(--text-muted)" stroke-width="1" />
      <path d="M 0,-1.5 L 0,0" stroke="var(--text-muted)" stroke-width="1" />
      <text class="meta" x="9" y="0">{{forks}}</text>
    </g>
  </g>
</svg>"""

LOADING_CARD_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="340" height="120" viewBox="0 0 340 120">
  <style>
    :root {
      --bg: #0d1117;
      --border: #30363d;
      --text-muted: #8b949e;
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #ffffff;
        --border: #d1d5db;
        --text-muted: #4b5563;
      }
    }
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&amp;display=swap');
    .card {
      fill: var(--bg);
      stroke: var(--border);
      stroke-width: 1.5;
      stroke-dasharray: 4 4;
      rx: 8;
    }
    .text {
      font-family: 'Outfit', sans-serif;
      font-weight: 600;
      font-size: 13px;
      fill: var(--text-muted);
      text-anchor: middle;
    }
  </style>
  <rect class="card" width="338" height="118" x="1" y="1"/>
  <text class="text" x="170" y="65">🚀 More Projects Loading...</text>
</svg>"""

# ==================== LANGUAGE COLORS ====================

LANG_COLORS = {
    "java": "#b07219",
    "javascript": "#f1e05a",
    "typescript": "#3178c6",
    "html": "#e34c26",
    "css": "#563d7c",
    "python": "#3572A5",
    "go": "#00add8",
    "rust": "#dea584",
    "c++": "#f34b7d",
    "c#": "#178600",
    "c": "#555555",
    "ruby": "#701516",
    "swift": "#f05138",
    "php": "#4f5d95",
    "markdown": "#777777",
    "shell": "#89e051"
}

def get_lang_color(lang):
    if not lang:
        return "#8b949e"
    return LANG_COLORS.get(lang.lower(), "#8b949e")

# ==================== DESCRIPTION WRAPPER ====================

def split_description(text, max_len=40):
    if not text:
        return "", ""
    words = text.split()
    line1 = ""
    line2 = ""
    
    i = 0
    # Build first line
    while i < len(words) and len(line1) + len(words[i]) + 1 <= max_len:
        line1 += (" " if line1 else "") + words[i]
        i += 1
        
    # Build second line
    while i < len(words) and len(line2) + len(words[i]) + 1 <= max_len:
        line2 += (" " if line2 else "") + words[i]
        i += 1
        
    # Ellipsis if truncated
    if i < len(words):
        if len(line2) + 3 <= max_len:
            line2 += "..."
        else:
            line2 = line2[:max_len-3] + "..."
            
    return line1, line2

# ==================== MAIN COMPILATION ====================

def clean_old_svgs(svg_dir):
    """
    Cleans up obsolete cyberpunk SVGs and resets directory
    """
    obsolete_files = [
        "project-50-dashboard.svg",
        "workout-progress.svg",
        "bike-progress.svg"
    ]
    for f in obsolete_files:
        path = os.path.join(svg_dir, f)
        if os.path.exists(path):
            os.remove(path)
            print(f"Removed obsolete: {f}")
            
    # Clean project cards directory if it exists, recreate it
    cards_dir = os.path.join(svg_dir, "project-cards")
    if os.path.exists(cards_dir):
        # We can delete all files inside but keep the folder
        for item in os.listdir(cards_dir):
            item_path = os.path.join(cards_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
    else:
        os.makedirs(cards_dir, exist_ok=True)

def main():
    script_dir = os.path.dirname(__file__)
    stats_path = os.path.join(script_dir, "stats.json")
    
    if not os.path.exists(stats_path):
        print("stats.json not found, running fetch_stats.py to generate...")
        from fetch_stats import main as run_fetch
        run_fetch()
        
    with open(stats_path, "r", encoding="utf-8") as f:
        stats = json.load(f)
        
    svg_dir = os.path.join(script_dir, "..", "svg")
    os.makedirs(svg_dir, exist_ok=True)
    
    # 1. Clean obsolete SVGs
    clean_old_svgs(svg_dir)
    
    print("Generating minimalist adaptive dashboards...")
    
    # 2. Generate typing.svg
    with open(os.path.join(svg_dir, "typing.svg"), "w", encoding="utf-8") as f:
        f.write(TYPING_TEMPLATE)
    print("Created typing.svg")
        
    # 3. Generate leetcode-dashboard.svg
    lc = stats["leetcode"]
    lc_svg = LEETCODE_TEMPLATE
    
    # Max difficulty counts from LeetCode questions (mock or actual metadata, let's use approx counts)
    lc_svg = lc_svg.replace("{{all}}", str(lc["all"]))
    lc_svg = lc_svg.replace("{{easy}}", f"{lc['easy']} / 952")
    lc_svg = lc_svg.replace("{{easy_w}}", str(int((lc["easy"] / 952) * 180)))
    
    lc_svg = lc_svg.replace("{{medium}}", f"{lc['medium']} / 2079")
    lc_svg = lc_svg.replace("{{medium_w}}", str(int((lc["medium"] / 2079) * 180)))
    
    lc_svg = lc_svg.replace("{{hard}}", f"{lc['hard']} / 950")
    lc_svg = lc_svg.replace("{{hard_w}}", str(int((lc["hard"] / 950) * 180)))
    
    # Contest rating block
    rating = lc.get("contest_rating", 0)
    if rating > 0:
        contest_block = f"""<rect class="stat-box" width="215" height="60" />
      <text class="label" x="15" y="22">CONTEST RATING</text>
      <text class="num" x="15" y="48" font-size="22" fill="var(--accent)">{rating}</text>
      <text class="label" x="200" y="22" text-anchor="end">TOP {lc.get("contest_top_percentage", 0.0)}%</text>
      <text class="label" x="200" y="45" text-anchor="end" font-size="10">Rank: #{lc.get("contest_ranking", 0):,}</text>"""
    else:
        contest_block = f"""<rect class="stat-box" width="215" height="60" />
      <text class="label" x="15" y="22">GLOBAL RANKING</text>
      <text class="num" x="15" y="48" font-size="20" fill="var(--accent)">#{lc.get("ranking", 0):,}</text>
      <text class="label" x="200" y="22" text-anchor="end">REPUTATION</text>
      <text class="num" x="200" y="48" font-size="16" text-anchor="end" fill="var(--text-main)">{lc.get("reputation", 0)}</text>"""
      
    lc_svg = lc_svg.replace("{{contest_block}}", contest_block)
    
    # Badges rendering
    badges_str = ""
    badges = lc.get("badges", [])
    for idx, b in enumerate(badges[:4]):
        bx = 15 + idx * 45
        by = 24
        # We render a small image embed for the badge icon
        badges_str += f'<image href="{b["icon"]}" x="{bx}" y="{by}" width="24" height="24" />\n      '
    if not badges:
        badges_str = '<text class="subtitle" x="15" y="34" font-size="11" fill="var(--text-muted)">No badges unlocked yet</text>'
        
    lc_svg = lc_svg.replace("{{badges_icons}}", badges_str.strip())
    
    with open(os.path.join(svg_dir, "leetcode-dashboard.svg"), "w", encoding="utf-8") as f:
        f.write(lc_svg)
    print("Created leetcode-dashboard.svg")
        
    # 4. Generate dynamic project cards
    repos = stats.get("repos", [])
    # Filter out profile readme repo named shafiq-11
    filtered_repos = [r for r in repos if r["name"].lower() != "shafiq-11"]
    if not filtered_repos:
        filtered_repos = repos
        
    cards_dir = os.path.join(svg_dir, "project-cards")
    
    featured_project_svgs = []
    
    for repo in filtered_repos[:5]: # Take top 5
        name = repo["name"]
        desc = repo["description"]
        lang = repo["language"]
        stars = repo["stars"]
        forks = repo["forks"]
        
        desc1, desc2 = split_description(desc, 50)
        
        card_content = PROJECT_CARD_TEMPLATE
        card_content = card_content.replace("{{name}}", name)
        card_content = card_content.replace("{{desc1}}", desc1)
        card_content = card_content.replace("{{desc2}}", desc2)
        card_content = card_content.replace("{{language}}", lang)
        card_content = card_content.replace("{{lang_color}}", get_lang_color(lang))
        card_content = card_content.replace("{{stars}}", str(stars))
        card_content = card_content.replace("{{forks}}", str(forks))
        
        # Meta spacings
        lang_len = len(lang)
        stars_x = 20 + max(lang_len * 7, 50)
        forks_x = stars_x + 20 + max(len(str(stars)) * 7, 25)
        
        card_content = card_content.replace("{{stars_x}}", str(stars_x))
        card_content = card_content.replace("{{forks_x}}", str(forks_x))
        
        filename = f"{name}.svg"
        card_path = os.path.join(cards_dir, filename)
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(card_content)
        print(f"Created project card: {filename}")
        
        featured_project_svgs.append({
            "name": name,
            "url": repo["url"],
            "svg_path": f"svg/project-cards/{filename}"
        })
        
    # Generate the placeholder loading card
    loading_card_path = os.path.join(cards_dir, "more-projects.svg")
    with open(loading_card_path, "w", encoding="utf-8") as f:
        f.write(LOADING_CARD_TEMPLATE)
    print("Created project card placeholder: more-projects.svg")
    
    # 5. Update README.md with the generated project cards
    update_readme_projects(featured_project_svgs)

def update_readme_projects(projects):
    """
    Updates the Featured Projects block inside README.md dynamically
    """
    readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
    if not os.path.exists(readme_path):
        print("README.md not found, skipping projects replacement.")
        return
        
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Format project cards in a clean 2x3 or 2x2 layout
    table_rows = ""
    # We will build rows of 2 columns
    for i in range(0, len(projects), 2):
        col1 = projects[i]
        col2 = projects[i+1] if i+1 < len(projects) else None
        
        cell1 = f"""    <td width="50%" valign="top">
      <a href="{col1["url"]}">
        <img src="{col1["svg_path"]}" alt="{col1["name"]}" width="100%"/>
      </a>
    </td>"""
        
        if col2:
            cell2 = f"""    <td width="50%" valign="top">
      <a href="{col2["url"]}">
        <img src="{col2["svg_path"]}" alt="{col2["name"]}" width="100%"/>
      </a>
    </td>"""
        else:
            # Render the more-projects.svg placeholder
            cell2 = f"""    <td width="50%" valign="top">
      <img src="svg/project-cards/more-projects.svg" alt="More Projects" width="100%"/>
    </td>"""
            
        table_rows += f"""  <tr>
{cell1}
{cell2}
  </tr>\n"""

    # If the total number of projects is even, we append the placeholder row at the end
    if len(projects) % 2 == 0:
        table_rows += """  <tr>
    <td width="50%" valign="top">
      <img src="svg/project-cards/more-projects.svg" alt="More Projects" width="100%"/>
    </td>
    <td width="50%" valign="top">
      <!-- Empty Spacer -->
    </td>
  </tr>\n"""

    projects_replacement = f"""<!-- PROJECTS_START -->
<table border="0" cellpadding="0" cellspacing="0" width="100%">
{table_rows.rstrip()}
</table>
<!-- PROJECTS_END -->"""

    # Replace PROJECTS block in README.md
    pattern = r"<!-- PROJECTS_START -->.*?<!-- PROJECTS_END -->"
    if re.search(pattern, content, re.DOTALL):
        updated_content = re.sub(pattern, projects_replacement, content, flags=re.DOTALL)
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Successfully updated project list in README.md")
    else:
        print("PROJECTS markers not found in README.md, skipping inline replacement.")

if __name__ == "__main__":
    main()
