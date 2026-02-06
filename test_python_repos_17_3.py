import requests


def test_python_repos_api():
    
    url = "https://api.github.com/search/repositories?q=language:python+sort:stars+stars:>10000"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    
    assert r.status_code == 200, f"Expected status code 200, got {r.status_code}"

    
    response_dict = r.json()

    
    assert response_dict['total_count'] > 500, "Expected total_count > 500"

    
    repo_dicts = response_dict['items']
    assert len(repo_dicts) > 0, "Expected at least one repository in items"

    
    first_repo = repo_dicts[0]
    expected_keys = ['name', 'owner', 'stargazers_count', 'html_url', 'created_at', 'updated_at', 'description']
    for key in expected_keys:
        assert key in first_repo, f"Expected key '{key}' in repository dictionary"
