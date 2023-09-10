
import pandas as pd

def get_coordinates_for_suburb(suburb):
    df = pd.read_csv("Housing_Price_Melbourne/Ml_Suburb_Coordination.csv")  
    
    suburb_row = df[df['Suburb'] == suburb]
    
    if not suburb_row.empty:
        latitude = suburb_row['Lattitude'].values[0]
        longitude = suburb_row['Longtitude'].values[0]
        return latitude, longitude
    else:
        return 0, 0  # Default to (0, 0) if suburb not found

region_options = ['Northern Metropolitan', 'Western Metropolitan', 'Southern Metropolitan',
 'Eastern Metropolitan', 'South-Eastern Metropolitan', 'Eastern Victoria', 'Northern Victoria',
   'Western Victoria' ]

suburb_options = ['Abbotsford', 'Aberfeldie', 'Airport West', 'Albanvale', 'Albert Park', 'Albion',
    'Alphington', 'Altona', 'Altona Meadows', 'Altona North', 'Ardeer', 'Armadale',
    'Ascot Vale', 'Ashburton', 'Ashwood', 'Aspendale', 'Aspendale Gardens', 'Attwood',
    'Avondale Heights', 'Bacchus Marsh', 'Balaclava', 'Balwyn', 'Balwyn North', 'Beaconsfield',
    'Beaconsfield Upper', 'Beaumaris', 'Bellfield', 'Berwick', 'Black Rock', 'Blackburn',
    'Blackburn North', 'Blackburn South', 'Bonbeach', 'Boronia', 'Box Hill', 'Braybrook',
    'Briar Hill', 'Brighton', 'Brighton East', 'Broadmeadows', 'Brookfield', 'Brooklyn',
    'Brunswick', 'Brunswick East', 'Brunswick West', 'Bulleen', 'Bullengarook', 'Burnley',
    'Burnside', 'Burnside Heights', 'Burwood', 'Burwood East', 'Cairnlea', 'Camberwell',
    'Campbellfield', 'Canterbury', 'Carlton', 'Carlton North', 'Carnegie', 'Caroline Springs',
    'Carrum', 'Carrum Downs', 'Caulfield', 'Caulfield East', 'Caulfield North', 'Caulfield South',
    'Chadstone', 'Chelsea', 'Chelsea Heights', 'Cheltenham', 'Chirnside Park', 'Clarinda',
    'Clayton', 'Clayton South', 'Clifton Hill', 'Coburg', 'Coburg North', 'Collingwood',
    'Coolaroo', 'Cremorne', 'Croydon', 'Croydon Hills', 'Croydon North', 'Croydon South',
    'Dallas', 'Dandenong', 'Dandenong North', 'Deepdene', 'Deer Park', 'Delahey', 'Derrimut',
    'Diamond Creek', 'Dingley Village', 'Docklands', 'Doreen', 'Doveton', 'Eaglemont',
    'East Melbourne', 'Edithvale', 'Elsternwick', 'Eltham', 'Eltham North', 'Elwood',
    'Emerald', 'Endeavour Hills', 'Essendon', 'Essendon North', 'Essendon West', 'Fairfield',
    'Fawkner', 'Ferntree Gully', 'Fitzroy', 'Fitzroy North', 'Flemington', 'Forest Hill',
    'Gardenvale', 'Gisborne', 'Gladstone Park', 'Glen Huntly', 'Glen Iris', 'Glen Waverley',
    'Glenroy', 'Gowanbrae', 'Greensborough', 'Greenvale', 'Hadfield', 'Hallam', 'Hampton',
    'Hampton East', 'Hampton Park', 'Hawthorn', 'Hawthorn East', 'Healesville', 'Heathmont',
    'Heidelberg', 'Heidelberg Heights', 'Heidelberg West', 'Highett', 'Hillside', 'Hoppers Crossing',
    'Hughesdale', 'Huntingdale', 'Hurstbridge', 'Ivanhoe', 'Ivanhoe East', 'Jacana', 'Kensington',
    'Kealba', 'Keilor', 'Keilor Downs', 'Keilor East', 'Keilor Lodge', 'Keilor Park', 'Kew',
    'Kew East', 'Keysborough', 'Kilsyth', 'Kings Park', 'Kingsbury', 'Kingsville', 'Knoxfield',
    'Kooyong', 'Kurunjang', 'Lalor', 'Langwarrin', 'Lower Plenty', 'Maidstone', 'Malvern',
    'Malvern East', 'Maribyrnong', 'Meadow Heights', 'Melbourne', 'Melton', 'Melton South',
    'Melton West', 'Mentone', 'Mernda', 'Middle Park', 'Mill Park', 'Mitcham', 'Monbulk',
    'Mont Albert', 'Montmorency', 'Montrose', 'Moonee Ponds', 'Moorabbin', 'Mooroolbark',
    'Mordialloc', 'Mount Evelyn', 'Mount Waverley', 'Mulgrave', 'Murrumbeena', 'Narre Warren',
    'New Gisborne', 'Newport', 'Niddrie', 'Noble Park', 'North Melbourne', 'North Warrandyte',
    'Northcote', 'Notting Hill', 'Nunawading', 'Oak Park', 'Oakleigh', 'Oakleigh East',
    'Oakleigh South', 'Officer', 'Ormond', 'Pakenham', 'Parkdale', 'Parkville', 'Pascoe Vale',
    'Plumpton', 'Point Cook', 'Port Melbourne', 'Prahran', 'Preston', 'Princes Hill', 'Reservoir',
    'Richmond', 'Ringwood', 'Ringwood East', 'Ringwood North', 'Ripponlea', 'Rockbank', 'Roxburgh Park',
    'Riddells Creek', 'Rosanna', 'Rowville', 'Roxburgh Park', 'Sandhurst', 'Sandringham', 'Seabrook',
    'Seaholme', 'Seaford', 'Seddon', 'Skye', 'South Kingsville', 'South Melbourne', 'South Morang',
    'South Yarra', 'Southbank', 'Spotswood', 'Springvale', 'Springvale South', 'St Albans',
    'St Helena', 'St Kilda', 'Strathmore', 'Strathmore Heights', 'Sunbury', 'Sunshine',
    'Sunshine North', 'Sunshine West', 'Surrey Hills', 'Sydenham', 'Tarneit', 'Taylors Hill',
    'Taylors Lakes', 'Templestowe', 'Templestowe Lower', 'The Basin', 'Thomastown',
    'Thornbury', 'Toorak', 'Travancore', 'Truganina', 'Tullamarine', 'Upwey', 'Vermont',
    'Vermont South', 'Viewbank', 'Wantirna', 'Wantirna South', 'Warrandyte', 'Waterways',
    'Watsonia', 'Watsonia North', 'Wattle Glen', 'Waverley Park', 'Wendouree', 'West Footscray',
    'West Melbourne', 'Westmeadows', 'Wheelers Hill', 'Whittlesea', 'Williams Landing', 'Williamstown',
    'Williamstown North', 'Wollert', 'Wyndham Vale', 'Yallambie', ]
