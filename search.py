import googlemaps

# connect google maps with API key
gmaps = googlemaps.Client(key='googlemaps API key')

cities = ["臺北市","新北市","桃園市","臺中市","臺南市","高雄市","基隆市","新竹市","嘉義市","新竹縣","苗栗縣","彰化縣","南投縣","雲林縣","嘉義縣","屏東縣","宜蘭縣","花蓮縣","臺東縣","澎湖縣"]

def address_Proc(address):
    if address[address.find('台灣')+2:address.find('台灣')+5] in cities:
        return address[address.find('台灣')+2:address.find('台灣')+5]
    else:
        return ''

def search_Food(latlng,keyword,open_now,search,rating_sort=True,rating_total_sort=True,radius=2000,ratings_total=0,debug=False):
    """
    :param latlng: The latitude/longitude value for which you wish to obtain the closest, human-readable address.(loaction)
    :type latlng: string, dict, list, or tuple
    
    :param keyword: A term to be matched against all content that Google has indexed for this place.('eat','food','dinner','breakfast')
    :type keyword: string

    :param open_now: Return only those places that are open for business at the time the query is sent.
    :type open_now: bool

    :param search: Choose search mode. 1 == rank_by , 0 == radius
    :type search: int, bool

    :param rating_sort: Rating sort from high to low.(default == True , False sorted by user_ratings_total)
    :type rating_sort: bool

    :param rating_total_sort: Rating total sort from high to low.(default == True , False sorted by user_ratings_total)
    :type rating_total_sort: bool

    :param radius: Distance in meters within which to bias results.(default == 2000)
    :type radius: int

    :param ratings_total: User ratings total need > that value.(default == 0)
    :type ratings_total: int

    :param debug: Output debug information.(default == False)
    :type debug: bool

    :rtype: Search results list (default sorted by rating).
    """
    loc = gmaps.reverse_geocode(latlng=latlng)[0]['geometry']['location']
    if search:
        results = gmaps.places_nearby(keyword=keyword,location=loc,open_now=open_now,rank_by='distance',type='restaurant')['results']
        # param type: https://developers.google.com/maps/documentation/places/web-service/supported_types
    else:
        results = gmaps.places_nearby(keyword=keyword,location=loc,open_now=open_now,radius=radius,type='restaurant')['results']

    if rating_sort:
        results = sorted(results, key=lambda x: x['rating'], reverse=True)

    sortedResults = sorted(results,key=lambda d: d['user_ratings_total'],reverse=True) if rating_total_sort else sorted(results,key=lambda d: d['user_ratings_total'])

    for res in sortedResults:
        if res['user_ratings_total'] >= ratings_total:
            sortedResults = sortedResults[sortedResults.index(res):len(sortedResults)]
            break
    
    # output debug
    if debug:
        for res in sortedResults:
            print(f"[&search_Food Debug] 店名：{res['name']} 評價：{res['rating']} 評價數：{res['user_ratings_total']}")

    return sortedResults
        
if __name__ == '__main__':
    search_Food([23.704722143865812, 120.42705486242713],'food',True,1)
    # address_Proc('632台灣雲林縣虎尾鎮文理暨管理大樓')
