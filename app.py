from flask  import Flask,request
from flask.json  import jsonify
from flask_caching import Cache

from queries import getAll, getAllCategories, getAllCountries, getCountryData,category_dic,country_id_lst,category_id_lst
app = Flask(__name__)
#initialize the cache and set it's port
cache = Cache(config={"CACHE_TYPE":'RedisCache','CACHE_REDIS_HOST':'127.0.0.1','CACHE_REDIS_PORT':'6379'})
cache.init_app(app)


#route for intro :)
@app.route('/',methods=['GET'])
def index():
    return jsonify({'success' : 'This is the assignment API, Which provides data about greenhouse gas emissions'})

#route for  listing all countries with their unique country_id
#also the cache with remain in memory for 1 hour 
@app.route('/listcountries', methods = ['GET'])
@cache.cached(timeout = 600,query_string=True)
def listCountries():
    return getAllCountries()

#route for  listing all categories with their unique category_id
@app.route('/listcategories', methods=['GET'])
@cache.cached(timeout = 600,query_string=True)
def listCategories():
    return getAllCategories()

#route for returning all the country data
@app.route('/countries', methods=['GET'])
@cache.cached(timeout = 600,query_string=True)
def countries():
    return getAll()

#route for accessing country based data using unique country id with startYear,endYear and categories as params
@app.route('/country', methods=['GET'])
@cache.cached(timeout = 600,query_string=True)
def country():
    arguments = request.args.to_dict()
    #check for valid country id:
    if arguments['id'] not in country_id_lst :
        raise ValueError('Invalid ID, please check ID or check /listcountries')
    
    #if params is empty or not present in the request, it implies that user wants data for all the categories in the database
    if "params" not in arguments.keys() or arguments['params'] == '':
        cat_ids = category_id_lst
    
    else:
        params = arguments['params'].split(',')
        cat_ids = []
        for val in params:
        #check for valid categories 
            try:
                if category_dic[val]:
                    cat_ids.append(category_dic[val])
            except Exception as e:
                raise ValueError("Invalid values for params, please check categories or check /listcategories")
            
    
    #checks for start and end years
    if (int(arguments['startYear']) < 1990 or int(arguments['startYear']) > 2014) or (int(arguments['endYear']) < 1990 or int(arguments['endYear']) > 2014):
        raise ValueError("Please check year values Data is only present for the years between 1990 and 2014")

    
    if (int(arguments['startYear']) > int(arguments['endYear']) ) :
        raise ValueError("startYear must be earlier or equal to endYear")



    if arguments['id'] is not None :
        country_data = getCountryData(arguments['id'],int(arguments['startYear']),int(arguments['endYear']),tuple(cat_ids))
    
    return  country_data

#for handling routes that don't exists ie; 404s
@app.errorhandler(404)
def routeDoesNotExist(e):
    return jsonify({'error' : "These aren't the routes you're looking for. - Obi-Wan"})

@app.errorhandler(405)
def methodNotAllowed(e):
    return jsonify({'error': 'The method is now allowed for this URL'})

@app.errorhandler(ValueError)
def returnError(e):
    return jsonify({'error' : str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
# route for index
# tells about the api

# route for countries
# returns all the countries with ids, names, and other values

# route for country/id
# temporal queries
# based on the id provided for the country 
# return values between start and end of year, or return values for years
# parametirc queries (categories are parameters) 
# return all the values for the parameter between start and end year.