# pyfifa
A lightweight and easy-to-use wrapper that allows you to extract data from FIFA.com and more.

### Installation
From PyPI
> No available.
 
From source code (clone it)
```bash
git clone https://github.com/manucabral/pyfifa.git
```
From GithubCLI
```bash
gh repo clone manucabral/pyfifa
```

### Usage
Using the ranking.
```py
import pyfifa
ranking = pyfifa.Ranking()
for item in ranking.items():
  print(item.rank, item.name)
```

Extra: change lang and limit items.
```py
ranking = pyfifa.Ranking(lang="fr", limit=5)
```

Exporting (json or csv)
```py
ranking.export(extension="json", filename="ranking")
```

Fetching ranking ids.
```py
import pyfifa
for rankingId in pyfifa.ranking_ids():
    print("ID", rankingId.value, "Date", rankingId.date)
```
Fetching a certain ranking id.
```py
import pyfifa

rankingIds = pyfifa.ranking_ids()

# Get the first FIFA ranking id
lastRankingId = rankingIds[-1]

ranking = pyfifa.Ranking(id=lastRankingId)
```


### Constributions
All constributions, bug reports or fixes and ideas are welcome.
