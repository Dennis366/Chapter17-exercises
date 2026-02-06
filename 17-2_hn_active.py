from operator import itemgetter
import requests
from plotly.graph_objs import Bar
from plotly import offline


url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status code: {r.status_code}")


submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    
    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict.get('descendants', 0),
        }
        submission_dicts.append(submission_dict)
    except KeyError:
        print(f"Skipping promotional post id: {submission_id}")


submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)


for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")


titles = []
comments = []
for submission_dict in submission_dicts:
    title = submission_dict['title']
    link = submission_dict['hn_link']
    
    titles.append(f"<a href='{link}'>{title}</a>")
    comments.append(submission_dict['comments'])


data = [{
    'type': 'bar',
    'x': titles,
    'y': comments,
    'hovertext': titles,
    'marker': {
        'color': 'rgb(60,100,150)',
        'line': {'width': 1.5, 'color': 'rgb(25,25,25)'}
    },
    'opacity': 0.6,
}]


my_layout = {
    'title': {
        'text': 'Most Active Discussions on Hacker News',
        'font': {'size': 24}
    },
    'xaxis': {
        'title': {
            'text': 'Submission',
            'font': {'size': 14}
        },
        'tickfont': {'size': 10},
    },
    'yaxis': {
        'title': {
            'text': 'Comments',
            'font': {'size': 14}
        },
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hn_active_discussions.html')
