"""
Real-World Dehradun Road Network Graph
Modeled following Google Maps Graph Structure:
- nodes: Array of [x, y] coordinates (latitude, longitude)
- edges: Array of dictionaries [{s: source, d: destination, w: distance_in_meters, name: road_name}, ...]
Origin: UPES Bidholi Campus (Point A)
Destination: Clock Tower / Ghanta Ghar (Point B)
"""

# 1. NODES: Array of [x, y] coordinate pairs (Latitude, Longitude)
NODES_COORDS = [
    [30.41589, 77.96644],  # Node 00: UPES Bidholi Campus (Origin - Point A)
    [30.41050, 77.96820],  # Node 01: Bidholi Village Chowk
    [30.39810, 77.97350],  # Node 02: Kandoli UPES Campus (Knowledge Acres)
    [30.38550, 77.97820],  # Node 03: Pondha Junction
    [30.37520, 77.95540],  # Node 04: Dunga Bypass Junction
    [30.36810, 77.96520],  # Node 05: Manduwala Chowk
    [30.35480, 77.95100],  # Node 06: Dhoolkot Forest Checkpost
    [30.34750, 77.95760],  # Node 07: Nanda Ki Chowki (Chakrata Road)
    [30.33960, 77.96850],  # Node 08: Premnagar Main Market
    [30.33410, 77.98620],  # Node 09: IMA (Indian Military Academy)
    [30.33820, 78.00530],  # Node 10: FRI (Forest Research Institute) Gate
    [30.33910, 78.02050],  # Node 11: Ballupur Chowk Flyover
    [30.33470, 78.03080],  # Node 12: Kishan Nagar Chowk
    [30.32860, 78.03620],  # Node 13: Bindal Bridge
    [30.35120, 78.03150],  # Node 14: Garhi Cantt (Birpur Army Area)
    [30.34150, 78.03320],  # Node 15: Kaulagarh / ONGC Tel Bhavan
    [30.29820, 78.00550],  # Node 16: Majra / Shimla Bypass
    [30.28860, 78.00920],  # Node 17: ISBT Dehradun
    [30.31520, 78.03210],  # Node 18: Saharanpur Chowk
    [30.31850, 78.03820],  # Node 19: Prince Chowk (Railway Station Road)
    [30.32443, 78.04184],  # Node 20: Clock Tower (Ghanta Ghar, Destination - Point B)

    # Specific POI Stop Nodes (Petrol Pump, Friend's House, Restaurant)
    [30.38050, 77.97400],  # Node 21: Indian Oil Petrol Pump (Pondha)
    [30.36850, 77.96580],  # Node 22: Friend's House (Manduwala)
    [30.36100, 77.96250],  # Node 23: The Village Restaurant & Cafe (Manduwala)
    [30.34780, 77.95850],  # Node 24: HP Petrol Pump (Nanda Ki Chowki)
    [30.33550, 78.01850],  # Node 25: Friend's House (Vasant Vihar / Ballupur)
    [30.33700, 78.02400],  # Node 26: Black Pepper / Kalsang Restaurant (Chakrata Rd)

    # Extended Highway Corridor to Haridwar, Rishikesh & Delhi
    [30.12450, 78.18950],  # Node 27: Doiwala / Nepali Farm Junction
    [30.10420, 78.29820],  # Node 28: Rishikesh (Triveni Ghat / Ganga River)
    [29.95620, 78.17060],  # Node 29: Haridwar (Har Ki Pauri / Ganga River)
    [29.86650, 77.89320],  # Node 30: Roorkee (IIT Roorkee / NH-334)
    [29.47270, 77.70850],  # Node 31: Muzaffarnagar (Rampur Tiraha Junction)
    [28.98450, 77.70640],  # Node 32: Meerut Bypass (Partapur Interchange)
    [28.62890, 77.27850],  # Node 33: Delhi / NCR (Akshardham / Anand Vihar / CP)

    # Highway Corridor POIs (Restaurants, Fuel Plazas, Ganga River Spots)
    [29.28250, 77.73200],  # Node 34: Cheetal Grand Highway Resort & Dhaba (Khatauli)
    [29.35120, 77.71980],  # Node 35: Namaste Midway Highway Food Plaza (Mansurpur)
    [29.83200, 77.85400],  # Node 36: Indian Oil Swagat Highway Plaza & Fuel (Roorkee Bypass)
    [28.89500, 77.68200],  # Node 37: HP Auto Care Oasis Mega Plaza (Meerut Expressway)
    [30.11800, 78.30900],  # Node 38: Chotiwala Authentic Ganga Restaurant (Rishikesh)

    # Mussoorie Hill Station & Rajpur Road Corridor
    [30.45980, 78.06440],  # Node 39: Mussoorie (Mall Road / Library Chowk)
    [30.37800, 78.07500],  # Node 40: Mussoorie Diversion / Rajpur Road
]

# Metadata array matching NODES_COORDS by index (No emojis)
NODES_META = [
    {"name": "UPES Bidholi Campus", "type": "education", "category": "education", "icon": "", "desc": "UPES Bidholi Campus, Dehradun foothills."},
    {"name": "Bidholi Village Chowk", "type": "junction", "category": "junction", "icon": "", "desc": "Connecting UPES campus to Pondha and Dunga bypass."},
    {"name": "Kandoli UPES Campus", "type": "education", "category": "education", "icon": "", "desc": "UPES Knowledge Acres Campus in Kandoli."},
    {"name": "Pondha Junction", "type": "junction", "category": "junction", "icon": "", "desc": "Key intersection leading towards Manduwala and Garhi Cantt."},
    {"name": "Dunga Bypass Junction", "type": "junction", "category": "junction", "icon": "", "desc": "Scenic rural connector connecting western outer Dehradun."},
    {"name": "Manduwala Chowk", "type": "junction", "category": "junction", "icon": "", "desc": "Major transit hub for students, local buses, and taxis."},
    {"name": "Dhoolkot Forest Checkpost", "type": "junction", "category": "transit", "icon": "", "desc": "Forest corridor linking Dunga road to Chakrata Highway."},
    {"name": "Nanda Ki Chowki", "type": "junction", "category": "junction", "icon": "", "desc": "Junction connecting Bidholi feeder road to NH-7 (Chakrata Road)."},
    {"name": "Premnagar Main Market", "type": "market", "category": "market", "icon": "", "desc": "Bustling market square with commercial activity."},
    {"name": "IMA (Indian Military Academy)", "type": "landmark", "category": "landmark", "icon": "", "desc": "Historic military academy along national highway."},
    {"name": "FRI Gate", "type": "landmark", "category": "landmark", "icon": "", "desc": "Forest Research Institute main entrance on Chakrata Road."},
    {"name": "Ballupur Chowk Flyover", "type": "junction", "category": "junction", "icon": "", "desc": "Major multi-level flyover connecting Cantt & City center."},
    {"name": "Kishan Nagar Chowk", "type": "junction", "category": "junction", "icon": "", "desc": "Urban junction leading towards Bindal bridge."},
    {"name": "Bindal Bridge", "type": "bridge", "category": "transit", "icon": "", "desc": "Historic bridge crossing Bindal river into inner city."},
    {"name": "Garhi Cantt (Birpur Army Area)", "type": "transit", "category": "transit", "icon": "", "desc": "Peaceful army cantonment zone alternate route."},
    {"name": "Kaulagarh / ONGC Tel Bhavan", "type": "landmark", "category": "landmark", "icon": "", "desc": "Headquarters of ONGC with wide tree-lined avenues."},
    {"name": "Majra / Shimla Bypass", "type": "junction", "category": "transit", "icon": "", "desc": "Southern artery bypassing the inner city center."},
    {"name": "ISBT Dehradun", "type": "terminal", "category": "transit", "icon": "", "desc": "Inter-State Bus Terminal connecting Uttarakhand."},
    {"name": "Saharanpur Chowk", "type": "junction", "category": "junction", "icon": "", "desc": "Historic southern entrance to Dehradun old bazaar."},
    {"name": "Prince Chowk", "type": "junction", "category": "junction", "icon": "", "desc": "Transit square connecting railway station road to Clock Tower."},
    {"name": "Clock Tower (Ghanta Ghar)", "type": "landmark", "category": "landmark", "icon": "", "desc": "The iconic 6-faced clock tower at the heart of Dehradun."},

    # Specific POI Stop Nodes
    {"name": "Indian Oil Petrol Pump (Pondha)", "type": "fuel", "category": "petrol_pump", "icon": "", "desc": "Refueling stop along the Bidholi-Pondha route."},
    {"name": "Friend's House (Manduwala)", "type": "home", "category": "friends_house", "icon": "", "desc": "Residential home stop in Manduwala student enclave."},
    {"name": "The Village Cafe & Restaurant", "type": "food", "category": "restaurant", "icon": "", "desc": "Popular highway food stop for snacks and meals."},
    {"name": "HP Petrol Pump (Nanda Ki Chowki)", "type": "fuel", "category": "petrol_pump", "icon": "", "desc": "Highway fueling station at Chakrata Road junction."},
    {"name": "Friend's House (Ballupur)", "type": "home", "category": "friends_house", "icon": "", "desc": "Residential stop in central Dehradun Vasant Vihar colony."},
    {"name": "Kalsang / Black Pepper Restaurant", "type": "food", "category": "restaurant", "icon": "", "desc": "Famous dining destination for authentic food."},

    # Extended Highway Corridor Metadata
    {"name": "Doiwala / Nepali Farm Junction", "type": "junction", "category": "junction", "icon": "", "desc": "Key highway junction connecting Dehradun, Rishikesh & Haridwar."},
    {"name": "Rishikesh (Triveni Ghat / Ganga Bank)", "type": "spiritual", "category": "river_ganga", "icon": "", "desc": "Sacred confluence on the banks of holy Ganga with evening Aarti."},
    {"name": "Haridwar (Har Ki Pauri / Ganga River)", "type": "spiritual", "category": "river_ganga", "icon": "", "desc": "World-famous holy Ganga River ghat where thousands gather for Ganga Aarti."},
    {"name": "Roorkee (IIT Roorkee / NH-334)", "type": "junction", "category": "junction", "icon": "", "desc": "Historic engineering university town and highway junction on NH-334."},
    {"name": "Muzaffarnagar (Rampur Tiraha Junction)", "type": "junction", "category": "junction", "icon": "", "desc": "Crucial junction on the Delhi-Dehradun economic corridor."},
    {"name": "Meerut Bypass (Partapur Interchange)", "type": "junction", "category": "junction", "icon": "", "desc": "Access point for the 14-lane Delhi-Meerut Expressway."},
    {"name": "Delhi / NCR (Anand Vihar / Connaught Place)", "type": "city", "category": "destination", "icon": "", "desc": "National Capital Region terminal and central business district."},

    # Highway POIs (Restaurants, Petrol Pumps, Ganga River Spots)
    {"name": "Cheetal Grand Highway Resort & Dhaba (Khatauli)", "type": "food", "category": "highway_restaurant", "icon": "", "desc": "Iconic multi-cuisine highway resort renowned for paneer pakodas & South Indian meals."},
    {"name": "Namaste Midway Food Plaza (Mansurpur)", "type": "food", "category": "highway_restaurant", "icon": "", "desc": "Premier highway oasis with Haldiram's, McDonald's, Costa Coffee & clean restrooms."},
    {"name": "Indian Oil Swagat Highway Plaza & Fuel (Roorkee Bypass)", "type": "fuel", "category": "highway_fuel", "icon": "", "desc": "24/7 highway fueling, EV hyper-charging, convenience store & driver lounge."},
    {"name": "HP Auto Care Oasis Mega Plaza (Meerut Expressway)", "type": "fuel", "category": "highway_fuel", "icon": "", "desc": "State-of-the-art expressway oasis with high-speed EV chargers and food court."},
    {"name": "Chotiwala Authentic Ganga Restaurant (Rishikesh)", "type": "food", "category": "highway_restaurant", "icon": "", "desc": "Heritage 1958 vegetarian dining landmark right beside the sacred Ganga river."},

    # Mussoorie Metadata
    {"name": "Mussoorie (Mall Road / Library Chowk)", "type": "hill_station", "category": "landmark", "icon": "", "desc": "Famous Queen of the Hills hill station overlooking the Doon Valley."},
    {"name": "Mussoorie Diversion / Rajpur Road", "type": "junction", "category": "junction", "icon": "", "desc": "Gateway junction connecting Dehradun city center to Mussoorie Hill Road."},
]

# 2. EDGES: Array of dictionaries [{s: source, d: destination, w: distance_in_meters, name: road_name, coords: [[lat, lng], ...]}, ...]
EDGES_DICTS = [
    # Main Arterial Corridor: Bidholi -> Kandoli -> Pondha -> Manduwala -> Nanda Ki Chowki
    {
        "s": 0, "d": 1, "w": 800, "name": "Bidholi Campus Road",
        "coords": [[30.41589, 77.96644], [30.41480, 77.96660], [30.41360, 77.96700], [30.41230, 77.96750], [30.41120, 77.96790], [30.41050, 77.96820]]
    },
    {
        "s": 1, "d": 2, "w": 1600, "name": "Bidholi-Kandoli Road",
        "coords": [[30.41050, 77.96820], [30.40880, 77.96880], [30.40710, 77.96970], [30.40540, 77.97060], [30.40360, 77.97150], [30.40180, 77.97230], [30.40000, 77.97300], [30.39810, 77.97350]]
    },
    {
        "s": 2, "d": 3, "w": 1800, "name": "Kandoli-Pondha Road",
        "coords": [[30.39810, 77.97350], [30.39600, 77.97420], [30.39380, 77.97500], [30.39150, 77.97600], [30.38920, 77.97690], [30.38720, 77.97760], [30.38550, 77.97820]]
    },
    {
        "s": 3, "d": 5, "w": 2300, "name": "Pondha-Manduwala Link",
        "coords": [[30.38550, 77.97820], [30.38260, 77.97600], [30.37950, 77.97320], [30.37620, 77.97050], [30.37300, 77.96820], [30.37020, 77.96650], [30.36810, 77.96520]]
    },
    {
        "s": 5, "d": 7, "w": 2700, "name": "Manduwala to Nanda Ki Chowki",
        "coords": [[30.36810, 77.96520], [30.36460, 77.96370], [30.36120, 77.96240], [30.35780, 77.96100], [30.35420, 77.95980], [30.35080, 77.95860], [30.34750, 77.95760]]
    },

    # Dunga & Dhoolkot Forest Bypass
    {
        "s": 1, "d": 4, "w": 4200, "name": "Dunga Access Road",
        "coords": [[30.41050, 77.96820], [30.40420, 77.96400], [30.39600, 77.96020], [30.38720, 77.95720], [30.37980, 77.95580], [30.37520, 77.95540]]
    },
    {
        "s": 4, "d": 5, "w": 1500, "name": "Dunga-Manduwala Crossroad",
        "coords": [[30.37520, 77.95540], [30.37280, 77.95880], [30.37020, 77.96220], [30.36810, 77.96520]]
    },
    {
        "s": 4, "d": 6, "w": 2800, "name": "Dunga-Dhoolkot Forest Stretch",
        "coords": [[30.37520, 77.95540], [30.36920, 77.95360], [30.36200, 77.95200], [30.35480, 77.95100]]
    },
    {
        "s": 6, "d": 7, "w": 1600, "name": "Dhoolkot to Nanda Ki Chowki",
        "coords": [[30.35480, 77.95100], [30.35220, 77.95320], [30.34960, 77.95560], [30.34750, 77.95760]]
    },

    # Chakrata Road (NH-7) Corridor
    {
        "s": 7, "d": 8, "w": 1400, "name": "Chakrata Road (NH-7) to Premnagar",
        "coords": [[30.34750, 77.95760], [30.34500, 77.96100], [30.34280, 77.96400], [30.34100, 77.96660], [30.33960, 77.96850]]
    },
    {
        "s": 8, "d": 9, "w": 2000, "name": "Premnagar to IMA Gate",
        "coords": [[30.33960, 77.96850], [30.33800, 77.97340], [30.33650, 77.97820], [30.33500, 77.98260], [30.33410, 77.98620]]
    },
    {
        "s": 9, "d": 10, "w": 2100, "name": "IMA to FRI Main Gate",
        "coords": [[30.33410, 77.98620], [30.33510, 77.99180], [30.33620, 77.99700], [30.33740, 78.00160], [30.33820, 78.00530]]
    },
    {
        "s": 10, "d": 11, "w": 1600, "name": "FRI to Ballupur Chowk",
        "coords": [[30.33820, 78.00530], [30.33850, 78.01050], [30.33880, 78.01560], [30.33910, 78.02050]]
    },
    {
        "s": 11, "d": 12, "w": 1200, "name": "Ballupur to Kishan Nagar",
        "coords": [[30.33910, 78.02050], [30.33760, 78.02400], [30.33620, 78.02720], [30.33520, 78.02940], [30.33470, 78.03080]]
    },
    {
        "s": 12, "d": 13, "w": 850, "name": "Kishan Nagar to Bindal Bridge",
        "coords": [[30.33470, 78.03080], [30.33250, 78.03280], [30.33040, 78.03460], [30.32860, 78.03620]]
    },
    {
        "s": 13, "d": 20, "w": 750, "name": "Bindal Bridge to Clock Tower",
        "coords": [[30.32860, 78.03620], [30.32700, 78.03820], [30.32550, 78.04020], [30.32443, 78.04184]]
    },

    # Garhi Cantt / Birpur Northern Bypass
    {
        "s": 3, "d": 14, "w": 6500, "name": "Pondha-Birpur Cantt Pass",
        "coords": [[30.38550, 77.97820], [30.38020, 77.98960], [30.37400, 78.00200], [30.36680, 78.01380], [30.35820, 78.02440], [30.35120, 78.03150]]
    },
    {
        "s": 11, "d": 14, "w": 1900, "name": "Ballupur to Garhi Cantt",
        "coords": [[30.33910, 78.02050], [30.34320, 78.02440], [30.34750, 78.02820], [30.35120, 78.03150]]
    },
    {
        "s": 14, "d": 15, "w": 1300, "name": "Garhi Cantt to Kaulagarh",
        "coords": [[30.35120, 78.03150], [30.34720, 78.03230], [30.34380, 78.03290], [30.34150, 78.03320]]
    },
    {
        "s": 15, "d": 12, "w": 1100, "name": "Kaulagarh to Kishan Nagar",
        "coords": [[30.34150, 78.03320], [30.33820, 78.03240], [30.33600, 78.03150], [30.33470, 78.03080]]
    },
    {
        "s": 15, "d": 20, "w": 1800, "name": "Kaulagarh to Clock Tower Direct Link",
        "coords": [[30.34150, 78.03320], [30.33520, 78.03680], [30.32950, 78.03980], [30.32443, 78.04184]]
    },

    # Southern Bypass via Premnagar -> Majra -> ISBT -> Saharanpur Chowk
    {
        "s": 8, "d": 16, "w": 5800, "name": "Premnagar to Majra (Shimla Bypass)",
        "coords": [[30.33960, 77.96850], [30.32620, 77.97880], [30.31180, 77.99220], [30.29820, 78.00550]]
    },
    {
        "s": 16, "d": 17, "w": 1200, "name": "Majra to ISBT Dehradun",
        "coords": [[30.29820, 78.00550], [30.29300, 78.00760], [30.28860, 78.00920]]
    },
    {
        "s": 17, "d": 18, "w": 3600, "name": "ISBT to Saharanpur Chowk",
        "coords": [[30.28860, 78.00920], [30.29720, 78.01780], [30.30620, 78.02550], [30.31520, 78.03210]]
    },
    {
        "s": 18, "d": 19, "w": 800, "name": "Saharanpur Chowk to Prince Chowk",
        "coords": [[30.31520, 78.03210], [30.31680, 78.03540], [30.31850, 78.03820]]
    },
    {
        "s": 19, "d": 20, "w": 900, "name": "Prince Chowk to Clock Tower",
        "coords": [[30.31850, 78.03820], [30.32140, 78.04020], [30.32443, 78.04184]]
    },
    {
        "s": 18, "d": 13, "w": 1600, "name": "Saharanpur Chowk to Bindal Bridge",
        "coords": [[30.31520, 78.03210], [30.32160, 78.03440], [30.32860, 78.03620]]
    },
    {
        "s": 12, "d": 18, "w": 2400, "name": "Kishan Nagar to Saharanpur Chowk link",
        "coords": [[30.33470, 78.03080], [30.32480, 78.03160], [30.31520, 78.03210]]
    },

    # POI Connections (Petrol Pump, Friend's House, Restaurant)
    # Node 21: Indian Oil Petrol Pump (Pondha)
    {
        "s": 3, "d": 21, "w": 600, "name": "Pondha Petrol Pump Approach",
        "coords": [[30.38550, 77.97820], [30.38280, 77.97580], [30.38050, 77.97400]]
    },
    {
        "s": 21, "d": 5, "w": 1700, "name": "Petrol Pump to Manduwala Link",
        "coords": [[30.38050, 77.97400], [30.37520, 77.97000], [30.37100, 77.96700], [30.36810, 77.96520]]
    },

    # Node 22: Friend's House (Manduwala)
    {
        "s": 5, "d": 22, "w": 200, "name": "Manduwala Colony Lane",
        "coords": [[30.36810, 77.96520], [30.36830, 77.96550], [30.36850, 77.96580]]
    },
    {
        "s": 4, "d": 22, "w": 1400, "name": "Dunga to Friend's Residence",
        "coords": [[30.37520, 77.95540], [30.37150, 77.96100], [30.36850, 77.96580]]
    },

    # Node 23: The Village Restaurant & Cafe (Manduwala Road)
    {
        "s": 5, "d": 23, "w": 900, "name": "Manduwala to Village Restaurant",
        "coords": [[30.36810, 77.96520], [30.36420, 77.96360], [30.36100, 77.96250]]
    },
    {
        "s": 23, "d": 7, "w": 1800, "name": "Village Restaurant to Nanda Ki Chowki",
        "coords": [[30.36100, 77.96250], [30.35620, 77.96060], [30.35150, 77.95890], [30.34750, 77.95760]]
    },

    # Node 24: HP Petrol Pump (Nanda Ki Chowki)
    {
        "s": 7, "d": 24, "w": 150, "name": "Nanda Ki Chowki HP Fuel Station",
        "coords": [[30.34750, 77.95760], [30.34780, 77.95850]]
    },
    {
        "s": 24, "d": 8, "w": 1250, "name": "HP Pump to Premnagar Market",
        "coords": [[30.34780, 77.95850], [30.34320, 77.96380], [30.33960, 77.96850]]
    },

    # Node 25: Friend's House (Vasant Vihar / Ballupur)
    {
        "s": 11, "d": 25, "w": 500, "name": "Ballupur to Vasant Vihar Lane",
        "coords": [[30.33910, 78.02050], [30.33700, 78.01940], [30.33550, 78.01850]]
    },
    {
        "s": 25, "d": 12, "w": 900, "name": "Vasant Vihar to Kishan Nagar",
        "coords": [[30.33550, 78.01850], [30.33490, 78.02480], [30.33470, 78.03080]]
    },

    # Node 26: Black Pepper / Kalsang Restaurant (Chakrata Road)
    {
        "s": 11, "d": 26, "w": 400, "name": "Ballupur to Restaurant Avenue",
        "coords": [[30.33910, 78.02050], [30.33780, 78.02240], [30.33700, 78.02400]]
    },
    {
        "s": 26, "d": 12, "w": 800, "name": "Restaurant to Kishan Nagar Chowk",
        "coords": [[30.33700, 78.02400], [30.33560, 78.02760], [30.33470, 78.03080]]
    },

    # =========================================================================
    # Extended Highway Corridor: Dehradun -> Haridwar -> Roorkee -> Delhi
    # =========================================================================
    # Dehradun to Nepali Farm Junction (NH-7)
    {
        "s": 17, "d": 27, "w": 22000, "name": "Dehradun ISBT to Nepali Farm (NH-7)",
        "coords": [[30.28860, 78.00920], [30.24500, 78.08200], [30.18500, 78.14500], [30.12450, 78.18950]]
    },
    {
        "s": 19, "d": 27, "w": 24000, "name": "Prince Chowk to Nepali Farm via Rispana",
        "coords": [[30.31850, 78.03820], [30.28500, 78.06500], [30.19200, 78.14000], [30.12450, 78.18950]]
    },

    # Nepali Farm to Rishikesh & Haridwar
    {
        "s": 27, "d": 28, "w": 16000, "name": "Nepali Farm to Rishikesh (Triveni Ghat)",
        "coords": [[30.12450, 78.18950], [30.11800, 78.24500], [30.10420, 78.29820]]
    },
    {
        "s": 27, "d": 29, "w": 24000, "name": "Nepali Farm to Haridwar (Har Ki Pauri)",
        "coords": [[30.12450, 78.18950], [30.06500, 78.17800], [30.00500, 78.17200], [29.95620, 78.17060]]
    },
    {
        "s": 28, "d": 29, "w": 21000, "name": "Rishikesh to Haridwar (Chilla Ganga Corridor)",
        "coords": [[30.10420, 78.29820], [30.05200, 78.22500], [29.98500, 78.18200], [29.95620, 78.17060]]
    },
    {
        "s": 28, "d": 38, "w": 1200, "name": "Triveni Ghat to Chotiwala Ganga Restaurant",
        "coords": [[30.10420, 78.29820], [30.11200, 78.30400], [30.11800, 78.30900]]
    },

    # Haridwar to Roorkee
    {
        "s": 29, "d": 30, "w": 32000, "name": "Haridwar to Roorkee (NH-334)",
        "coords": [[29.95620, 78.17060], [29.91200, 78.05500], [29.88500, 77.96500], [29.86650, 77.89320]]
    },

    # Roorkee to Muzaffarnagar (with Indian Oil Swagat Plaza)
    {
        "s": 30, "d": 36, "w": 3500, "name": "Roorkee to Indian Oil Swagat Highway Plaza",
        "coords": [[29.86650, 77.89320], [29.84500, 77.87200], [29.83200, 77.85400]]
    },
    {
        "s": 36, "d": 31, "w": 41500, "name": "Swagat Plaza to Muzaffarnagar (NH-334)",
        "coords": [[29.83200, 77.85400], [29.68500, 77.78500], [29.56200, 77.73500], [29.47270, 77.70850]]
    },
    {
        "s": 30, "d": 31, "w": 45000, "name": "Roorkee to Muzaffarnagar Direct",
        "coords": [[29.86650, 77.89320], [29.72000, 77.79500], [29.58000, 77.74000], [29.47270, 77.70850]]
    },

    # Muzaffarnagar to Meerut (with Namaste Midway & Cheetal Grand)
    {
        "s": 31, "d": 35, "w": 14000, "name": "Muzaffarnagar to Namaste Midway Food Plaza",
        "coords": [[29.47270, 77.70850], [29.41200, 77.71400], [29.35120, 77.71980]]
    },
    {
        "s": 35, "d": 34, "w": 12000, "name": "Namaste Midway to Cheetal Grand Resort (Khatauli)",
        "coords": [[29.35120, 77.71980], [29.31500, 77.72600], [29.28250, 77.73200]]
    },
    {
        "s": 34, "d": 32, "w": 32000, "name": "Cheetal Grand to Meerut Bypass Interchange",
        "coords": [[29.28250, 77.73200], [29.15500, 77.72200], [29.04500, 77.71200], [28.98450, 77.70640]]
    },
    {
        "s": 31, "d": 32, "w": 58000, "name": "Muzaffarnagar to Meerut Bypass Direct",
        "coords": [[29.47270, 77.70850], [29.32000, 77.72400], [29.12000, 77.71800], [28.98450, 77.70640]]
    },

    # Meerut to Delhi / NCR via Delhi-Meerut Expressway (NE-3)
    {
        "s": 32, "d": 37, "w": 12000, "name": "Meerut to HP Auto Care Oasis Mega Plaza",
        "coords": [[28.98450, 77.70640], [28.93800, 77.69400], [28.89500, 77.68200]]
    },
    {
        "s": 37, "d": 33, "w": 50000, "name": "HP Oasis Plaza to Delhi / NCR (Expressway)",
        "coords": [[28.89500, 77.68200], [28.78500, 77.54500], [28.69200, 77.41200], [28.62890, 77.27850]]
    },
    {
        "s": 32, "d": 33, "w": 62000, "name": "Delhi-Meerut Expressway (NE-3) Direct",
        "coords": [[28.98450, 77.70640], [28.82500, 77.59500], [28.71000, 77.43500], [28.62890, 77.27850]]
    },

    # Mussoorie Hill Road Connections
    {
        "s": 39, "d": 40, "w": 18000, "name": "Mussoorie to Rajpur Diversion (Hill Highway)",
        "coords": [[30.45980, 78.06440], [30.43500, 78.07200], [30.40800, 78.08100], [30.37800, 78.07500]]
    },
    {
        "s": 40, "d": 20, "w": 6800, "name": "Mussoorie Diversion to Clock Tower via Rajpur Road",
        "coords": [[30.37800, 78.07500], [30.35500, 78.06100], [30.33800, 78.05100], [30.32443, 78.04184]]
    },
    {
        "s": 40, "d": 14, "w": 5200, "name": "Mussoorie Diversion to Garhi Cantt",
        "coords": [[30.37800, 78.07500], [30.36400, 78.05200], [30.35120, 78.03150]]
    },
]

# Combined list for backwards compatibility
NODES = [
    {
        "id": i,
        "name": NODES_META[i]["name"],
        "lat": NODES_COORDS[i][0],
        "lng": NODES_COORDS[i][1],
        "coord": NODES_COORDS[i],
        "desc": NODES_META[i]["desc"],
        "type": NODES_META[i]["type"],
        "category": NODES_META[i]["category"],
        "icon": NODES_META[i]["icon"],
    }
    for i in range(len(NODES_COORDS))
]

# Simple edge tuples for existing matrix builder: (s, d, w, name)
EDGES = [(e["s"], e["d"], e["w"], e["name"]) for e in EDGES_DICTS]


def build_dehradun_distance_matrix() -> list[list[int]]:
    """
    Constructs a V x V adjacency matrix from EDGES_DICTS.
    0 on diagonals, positive edge weights in meters, and 0 for non-adjacent nodes.
    """
    n = len(NODES_COORDS)
    matrix = [[0] * n for _ in range(n)]

    for e in EDGES_DICTS:
        u = e["s"]
        v = e["d"]
        w = e["w"]
        matrix[u][v] = w
        matrix[v][u] = w  # Bidirectional roads

    return matrix


def get_selectable_waypoints() -> list[dict]:
    """Returns all nodes that can be selected as origins, destinations, or intermediate stops."""
    return [
        {
            "id": i,
            "name": NODES_META[i]["name"],
            "coord": NODES_COORDS[i],
            "lat": NODES_COORDS[i][0],
            "lng": NODES_COORDS[i][1],
            "category": NODES_META[i]["category"],
            "icon": NODES_META[i]["icon"],
            "desc": NODES_META[i]["desc"],
            "type": NODES_META[i].get("type", "junction"),
        }
        for i in range(len(NODES_COORDS))
    ]


def get_graph_representation() -> dict:
    """
    Returns graph representation matching Google Maps / classroom requirements:
    - nodes: array of [x, y] coordinates
    - edges: array of dictionaries [{s: source, d: destination, w: weight, name: road_name}, ...]
    """
    return {
        "nodes": NODES_COORDS,
        "edges": EDGES_DICTS,
        "nodes_metadata": NODES_META
    }
