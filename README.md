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

# exporting
ranking.export(extension="json")
```


### Constributions
All constributions, bug reports or fixes and ideas are welcome.
