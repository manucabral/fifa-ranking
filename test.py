import pyfifa

last_id = pyfifa.ranking_ids()[0]
ranking = pyfifa.Ranking(ranking_id=last_id)

items = ranking.items()

for item in items:
    print(item.rank, item.name, item.total_points)
