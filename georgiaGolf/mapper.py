GOLF = {1: ['alfred tup holmes golf club','alfred tup holmes club','alfred tup holmes'],
        2: ['ansley golf club'],
        3: ['bear best atlanta','bears best atlanta'],
        4: ['brown mill','browns mill golf','brown mill golf course'],
        5: ['charlie yates golf','charlie yates'],
        6: ['cobblestone golf club','cobblestone','cobblestone golf','cobblestone golf course'],
        7: ['fox creek golf club'],
        8: ['golf tech driving range','golf tech'],
        9: ['marietta golf center driving range','marietta golf center','marietta golf'],
        10: ['northcrest','northcrest golf','northcrest golf range'],
        11: ['river pines golf', 'river pines golf course', 'river pines golf club'],
        12: ['bobby jones','boby jones'],
        13: ['forest hills golf club' ,'forest hills'],
        14: ['goshen plantation golf club','goshen','goshen plantation','goshen golf club','goshen club', 'goshen golf course','goshen course'],
        15: ['indian hills country club', 'indian hills'],
        16: ['fox creek golf club'],
        17: ['john a. white golf course', 'john white golf','john a white golf course','john white golf course','john a white'],
        18: ['north cherokee town and country club','north cherokee','north cherokee town'],
        19: ['wolf creek golf course','wolf creek golf'],
        20: ['candler park golf course','candler park golf'],
        21: ['cross creek golf course','cross creek'],
        22: ['top golf driving range','top golf'],
        23: ['georgia trail driving range','georgia trail'],
        24: ['peachtree golf center driving range','peachtree golf center','peachtree golf'],
        25: ['druid hills golf course','druid hills']}


GOLF_INFO = {'ft_1': "Golf Georgia - https://golfgeorgia.info/Alfred-Tup-Holmes-Golf",
             'ft_2': "Golf Georgia - https://golfgeorgia.info/ansley-golf-club",
             'ft_3': "Golf Georgia - https://golfgeorgia.info/Bears-Best-Golf",
             'ft_4': "Golf Georgia - https://golfgeorgia.info/brown-hill",
             'ft_5': "Golf Georgia - https://golfgeorgia.info/Charlie-Yates-Golf",
             'ft_6': "Golf Georgia -  https://golfgeorgia.info/Cobbleston-Golf-Club",
             'ft_7': "Golf Georgia - https://golfgeorgia.info/FoxCreek-Golf-Club",
             'ft_8': "Golf Georgia - https://golfgeorgia.info/golf-tech-driving-range",
             'ft_9': "Golf Georgia - https://golfgeorgia.info/marietta-golf-center",
             'ft_10': "Golf Georgia - https://golfgeorgia.info/northcrest-golf-range",
             'ft_11': "Golf Georgia - https://golfgeorgia.info/river-pines",
             'ft_12': "Golf Georgia - https://golfgeorgia.info/Bobby-Jones-Golf",
             'ft_13': "Golf Georgia - https://golfgeorgia.info/forest-hills-golf",
             'ft_14': "Golf Georgia - https://golfgeorgia.info/Goshen-Plantation-Golf",
             'ft_15': "Golf Georgia - https://golfgeorgia.info/Indian-Hills",
             'ft_16': "Golf Georgia - https://golfgeorgia.info/FoxCreek-Golf-Club",
             'ft_17': "Golf Georgia - https://golfgeorgia.info/John-White-Golf",
             'ft_18': "Golf Georgia - https://golfgeorgia.info/North-Cherokee-Town-Country-Club",
             'ft_19': "Golf Georgia - https://golfgeorgia.info/Wolf-Creek-Golf",
             'ft_20': "Golf Georgia - https://golfgeorgia.info/candler-park-golf-course",
             'ft_21': "Golf Georgia - https://golfgeorgia.info/cross-creek-golf-course",
             'ft_22': "Golf Georgia - https://golfgeorgia.info/top-golf-driving-range",
             'ft_23': "Golf Georgia - https://golfgeorgia.info/georiga-trail-driving-range",
             'ft_24': "Golf Georgia - https://golfgeorgia.info/peachtree-golf-center",
             'ft_25': "Golf Georgia - https://golfgeorgia.info/druid-hills-golf-course" }


def map(golf_name):
    for i in range(1,len(GOLF)+1):
        #Return dict key number
        if str(golf_name) in GOLF.get(i):
            return 'ft_' + str(i)
    return 'None'


def map_info(ft_number):
    return GOLF_INFO[ft_number]
