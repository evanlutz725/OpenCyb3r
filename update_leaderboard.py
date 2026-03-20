import requests
import os
import re

# Use GitHub Secrets for repo details
OWNER = os.getenv("REPO_OWNER")
REPO = os.getenv("REPO_NAME")

def get_contributors(owner, repo):
    """Fetch contributors from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contributors = response.json()
        leaderboard = [
            {
                "username": contributor["login"],
                "contributions": contributor["contributions"],
                "avatar_url": contributor["avatar_url"]
            }
            for contributor in contributors
        ]
        return sorted(leaderboard, key=lambda x: x["contributions"], reverse=True)
    else:
        print(f"Failed to fetch contributors: {response.status_code}")
        return []

def generate_html(leaderboard):
    """Generate leaderboard.html for GitHub Pages with a darker cyber theme."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OpenCyb3r Leaderboard</title>
        <style>
            body {{
                background: linear-gradient(-45deg, #0a0f1b, #1a2a3a, #004466, #006666);
                background-size: 400% 400%;
                animation: gradient 15s ease infinite;
                font-family: Arial, sans-serif;
                text-align: center;
                color: white;
                margin: 0;
                padding: 20px;
                overflow: hidden;
            }}

            @keyframes gradient {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}

            h1 {{
                font-size: 2.5rem;
                font-weight: bold;
                text-shadow: 0 0 10px #00ffea, 0 0 20px #00ffea, 0 0 30px #00ffea;
            }}

            table {{
                width: 80%;
                margin: 20px auto;
                border-collapse: collapse;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border: 2px solid #00ffea;
                box-shadow: 0 0 10px #00ffea;
            }}

            th, td {{
                padding: 10px;
                border: 1px solid white;
            }}

            tr:hover {{
                background-color: rgba(0, 255, 234, 0.2);
                transition: 0.3s ease-in-out;
            }}

            .avatar {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 10px;
                vertical-align: middle;
                border: 2px solid #00ffea;
                box-shadow: 0 0 10px #00ffea;
            }}

            .particle {{
                position: absolute;
                width: 5px;
                height: 5px;
                background-color: rgba(0, 255, 234, 0.8);
                border-radius: 50%;
                opacity: 0.6;
                animation: moveParticle 10s linear infinite;
            }}

            @keyframes moveParticle {{
                from {{
                    transform: translate(0, 0);
                }}
                to {{
                    transform: translate(100vw, 100vh);
                }}
            }}
        </style>
    </head>
    <body>
        <h1>OpenCyb3r Leaderboard</h1>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Contributor</th>
                    <th>Contributions</th>
                </tr>
            </thead>
            <tbody>
    """.format(REPO)

    for rank, contributor in enumerate(leaderboard, start=1):
        html += """
                <tr>
                    <td>{}</td>
                    <td><img src="{}" class="avatar"> {}</td>
                    <td>{}</td>
                </tr>
        """.format(rank, contributor["avatar_url"], contributor["username"], contributor["contributions"])

    html += """
            </tbody>
        </table>

        <script>
            function createParticle() {{
                const particle = document.createElement("div");
                particle.classList.add("particle");
                document.body.appendChild(particle);

                particle.style.left = Math.random() * 100 + "vw";
                particle.style.top = Math.random() * 100 + "vh";
                particle.style.animationDuration = Math.random() * 10 + 5 + "s";

                setTimeout(() => {{
                    particle.remove();
                }}, 15000);
            }}

            setInterval(createParticle, 500);
        </script>

    </body>
    </html>
    """

    return html

def save_html_to_file(html, filename="leaderboard.html"):
    """Save HTML to file."""
    with open(filename, "w") as file:
        file.write(html)

def update_readme(leaderboard):
    """Update README.md with the Top 5 contributors while preserving other content."""
    top_5 = leaderboard[:5]
    leaderboard_section = f"\n<!-- LEADERBOARD START -->\n"
    leaderboard_section += "| Rank | Contributor | Contributions |\n"
    leaderboard_section += "|------|-------------|----------------|\n"

    for rank, contributor in enumerate(top_5, start=1):
        leaderboard_section += (
            f"| {rank} | <img src='{contributor['avatar_url']}' width='20' height='20'> {contributor['username']} | {contributor['contributions']} |\n"
        )
    leaderboard_section += "\n<!-- LEADERBOARD END -->\n"

    try:
        with open("README.md", "r") as file:
            content = file.read()

        # Preserve content outside leaderboard section
        if "<!-- LEADERBOARD START -->" in content and "<!-- LEADERBOARD END -->" in content:
            updated_content = re.sub(
                r"<!-- LEADERBOARD START -->.*?<!-- LEADERBOARD END -->",
                leaderboard_section,
                content,
                flags=re.DOTALL
            )
        else:
            updated_content = content.strip() + "\n\n" + leaderboard_section

        with open("README.md", "w") as file:
            file.write(updated_content)

        print("✅ README.md updated successfully.")
    except FileNotFoundError:
        print("⚠️ README.md not found, creating a new one.")
        with open("README.md", "w") as file:
            file.write(leaderboard_section)

if __name__ == "__main__":
    print(f"Generating leaderboard for {OWNER}/{REPO}...")
    leaderboard = get_contributors(OWNER, REPO)

    if leaderboard:
        save_html_to_file(generate_html(leaderboard))
        update_readme(leaderboard)
        print("✅ Leaderboard updated successfully.")
    else:
        print("❌ No contributors found or failed to retrieve data.")
