from uszipcode import SearchEngine
search = SearchEngine(simple_zipcode=False)
zipcode = search.by_state("Florida",returns=1000)
for curZip in zipcode:
    print(curZip.polygon)