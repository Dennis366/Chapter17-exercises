import requests
from plotly.graph_objs import Bar, Layout
from plotly import offline


url = "https://api.github.com/search/repositories"
url += "?q=language:python+sort:stars+stars:>10000"

headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
print(f"Status code: {r.status_code}")


response_dict = r.json()


print(f"Total repositories: {response_dict['total_count']}")
print(f"Complete results: {not response_dict['incomplete_results']}")


repo_dicts = response_dict['items']
print(f"Repositories returned: {len(repo_dicts)}")


repo_names = []
stars = []
forks = []
open_issues = []
repo_urls = []

for repo in repo_dicts:
    repo_names.append(repo['name'])
    stars.append(repo['stargazers_count'])
    forks.append(repo['forks_count'])
    open_issues.append(repo['open_issues_count'])
    repo_urls.append(repo['html_url'])


hover_texts = [f"Forks: {f}, Open Issues: {i}" for f, i in zip(forks, open_issues)]


data = [{
    'type': 'bar',
    'x': stars,
    'y': repo_names,
    'orientation': 'h',  
    'text': hover_texts,
    'marker': {
        'color': stars,
        'colorscale': 'Viridis',
        'reversescale': True,
        'line': {'width': 1, 'color': 'black'}
    }
}]

layout = Layout(
    title='Top Python Repositories on GitHub',
    xaxis={'title': 'Stars'},
    yaxis={'title': 'Repository'},
    margin={'l': 250, 'r': 20, 't': 50, 'b': 50},
)

fig = {'data': data, 'layout': layout}
offline.plot(fig, filename='python_repos_custom.html')
