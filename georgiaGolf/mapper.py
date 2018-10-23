GOLF = {1: ['alfred tup holmes golf club','alfred tup holmes club','alfred tup holmes'],
        2: ['ansley golf club'],
        3: ['bear best atlanta','bears best atlanta'],
        4: ['brown mill','browns mill golf'],
        5: ['charlie yates golf','charlie yates'],
        6: ['cobblestone golf club','cobblestone','cobblestone golf'],
        7: ['fox creek golf club'],
        8: ['golf tech driving range','golf tech'],
        9: ['marietta golf center driving range','marietta golf center','marietta golf'],
        10: ['northcrest','northcrest golf','northcrest golf range'],
        11: ['river pines golf', 'river pines golf course', 'river pines golf club']
        }

def map(golf_name):
    for i in range(1,len(GOLF)+1):
        #Return dict key number
        if str(golf_name) in GOLF.get(i):
            return 'ft_' + str(i)
    return 'None'
