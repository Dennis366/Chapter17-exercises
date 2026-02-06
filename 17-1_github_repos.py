import requests
import plotly.graph_objects as go

languages = ['javascript', 'ruby', 'c', 'java', 'perl', 'haskell', 'go']


top_repos = []

for language in languages:
    print(f"\n--- Top repositories for {language.upper()} ---")

    url = f"https://api.github.com/search/repositories?q=language:{language}+stars:>10000&sort=stars"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    print(f"Status code: {r.status_code}")

    response_dict = r.json()
    repo_dicts = response_dict['items']
    print(f"Repositories returned: {len(repo_dicts)}")

    for repo_dict in repo_dicts[:5]:
        print(f"Name: {repo_dict['name']}")
        print(f"Owner: {repo_dict['owner']['login']}")
        print(f"Stars: {repo_dict['stargazers_count']}")
        print(f"Repository: {repo_dict['html_url']}")
        print(f"Created: {repo_dict['created_at']}")
        print(f"Updated: {repo_dict['updated_at']}")
        print(f"Description: {repo_dict['description'] or 'No description'}")
        print("-" * 40)

    
    top_repos.append({
        'language': language.capitalize(),
        'name': repo_dicts[0]['name'],
        'stars': repo_dicts[0]['stargazers_count']
    })


repo_labels = [f"{repo['language']}: {repo['name']}" for repo in top_repos]
stars = [repo['stars'] for repo in top_repos]


fig = go.Figure(data=[go.Bar(x=repo_labels, y=stars, text=stars, textposition='auto')])
fig.update_layout(
    title="Top GitHub Repositories per Language",
    xaxis_title="Language : Repository",
    yaxis_title="Stars",
    xaxis_tickangle=-45
)


fig.write_html("top_repos_chart.html")
print("\nChart saved as top_repos_chart.html")

