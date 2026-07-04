# Setup Instructions - The Shafiq Dashboard

This profile dashboard is built with automation scripts that fetch your live metrics (GitHub contributions, WakaTime coding times, and LeetCode problems solved) and generate custom glowing cyberpunk SVGs for your profile.

To set up this dashboard on your GitHub profile, follow the steps below.

---

## 🚀 Step 1: Create a Personal GitHub Repository

1. Create a new public repository on GitHub named exactly after your username (e.g. `Shafiq-11`).
2. Clone it locally, copy all the files from this project into it, and push them to your `main` branch.

---

## 🔑 Step 2: Configure Repository Secrets

To enable the automated stats-fetching script, go to your repository's **Settings > Secrets and variables > Actions** and add the following secrets:

1. **`LEETCODE_USERNAME`**: 
   - **Value**: Your LeetCode username (e.g., `shafiq_11`). This allows the script to fetch your solved problems count.
2. **`WAKATIME_API_KEY`**: 
   - **Value**: Your WakaTime API key (retrieve it from [WakaTime Account Settings](https://wakatime.com/settings/api-key)).
3. **`GITHUB_TOKEN`**:
   - *Note*: This is automatically provided by GitHub Actions to push the generated SVGs back to your repository. You don't need to manually add it. However, ensure that the workflow has write permissions (go to **Settings > Actions > General > Workflow permissions** and select **"Read and write permissions"**).

---

## 🛠️ Step 3: Local Testing

To run the fetcher and compiler locally:

1. Install the `requests` library:
   ```bash
   pip install requests
   ```
2. Run the stats gatherer:
   ```bash
   python scripts/fetch_stats.py
   ```
3. Compile the dashboards:
   ```bash
   python scripts/generate_dashboard.py
   ```
This will fetch current stats, generate SVGs in the `svg/` folder, and automatically rewrite the stats block in your `README.md`.

---

## 📊 Customizing Progress Targets

To edit your Project 50 status, gym targets, or motorcycle odometer tracking, edit the default dictionary values in `scripts/fetch_stats.py` inside the `main()` function:

- **Project 50 values**:
  ```python
  "project50": {
      "coding": 92,      # Progress percent (0-100)
      "dsa": 86,         # Progress percent (0-100)
      "gym": 100,        # Progress percent (0-100)
      "projects": 90,    # Progress percent (0-100)
      "learning": 95,    # Progress percent (0-100)
      "day": 45          # Current day number
  }
  ```
- **Bike metrics**:
  ```python
  "bike": {
      "progress": 78,
      "distance_completed": 780,
      "target_distance": 1000,
      "status": "Cruising"
  }
  ```
The `scripts/generate_dashboard.py` script will automatically recalculate coordinates, scale the progress bars, and update the graphics upon the next run!
