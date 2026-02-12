FACTION_DATA = {   'chrome_phantoms': {   'control': 45,
                           'description': 'Ghost riders of the megalopolis who '
                                          'vanish into neon fog after every '
                                          "heist. They strip rivals' vehicles "
                                          'for parts and leave only burning '
                                          'chassis in their wake, their '
                                          'reflective chrome wraps making them '
                                          'near-invisible under city lights.',
                           'faction_boss': {   'damage_multiplier': 2.0,
                                               'hp_multiplier': 5.5,
                                               'name': 'Spectra Nine',
                                               'vehicle': 'ArmoredTruck'},
                           'hub_city_coordinates': [4000, -3000],
                           'name': 'Chrome Phantoms',
                           'relationships': {   'gaslight_union': 'Hostile',
                                                'neon_serpents': 'Hostile',
                                                'the_underpass': 'Neutral',
                                                'volt_yakuza': 'Neutral'},
                           'units': [   'RustySedan',
                                        'Technical',
                                        'ArmoredTruck',
                                        'RaiderBuggy']},
    'gaslight_union': {   'control': 40,
                          'description': 'Old-school gearheads who reject the '
                                         'neon excess and swear by combustion '
                                         'engines and analog gauges. They hold '
                                         'the industrial dockyards where the '
                                         'last reserves of refined fuel are '
                                         'stored, and they defend them with '
                                         'armored blockades.',
                          'faction_boss': {   'damage_multiplier': 2.5,
                                              'hp_multiplier': 5.0,
                                              'name': 'Big Diesel Mara',
                                              'vehicle': 'Miner'},
                          'hub_city_coordinates': [-3000, -4000],
                          'name': 'Gaslight Union',
                          'relationships': {   'chrome_phantoms': 'Hostile',
                                               'neon_serpents': 'Neutral',
                                               'the_underpass': 'Allied',
                                               'volt_yakuza': 'Hostile'},
                          'units': [   'Technical',
                                       'RustBucket',
                                       'Miner',
                                       'ArmoredTruck']},
    'neon_serpents': {   'control': 55,
                         'description': 'A ruthless syndicate of drift racers '
                                        'who control the rain-slicked highways '
                                        "beneath the city's flickering "
                                        'holographic billboards. Their cars '
                                        'glow with stolen reactor light, and '
                                        'loyalty is measured in lap times.',
                         'faction_boss': {   'damage_multiplier': 3.0,
                                             'hp_multiplier': 4.5,
                                             'name': 'Viper Kazuya',
                                             'vehicle': 'MuscleCar'},
                         'hub_city_coordinates': [-4000, 3000],
                         'name': 'Neon Serpents',
                         'relationships': {   'chrome_phantoms': 'Hostile',
                                              'gaslight_union': 'Neutral',
                                              'the_underpass': 'Neutral',
                                              'volt_yakuza': 'Hostile'},
                         'units': ['MuscleCar', 'RaiderBuggy', 'Technical']},
    'the_underpass': {   'control': 100,
                         'description': 'A sprawling neutral zone beneath the '
                                        "city's central interchange, where all "
                                        'factions come to trade, gamble, and '
                                        'hire mercenaries. Neon signs in every '
                                        'color mark its rain-puddled '
                                        'corridors, and an unspoken truce '
                                        'keeps the peace—most nights.',
                         'faction_boss': None,
                         'hub_city_coordinates': [0, 0],
                         'name': 'The Underpass',
                         'relationships': {   'chrome_phantoms': 'Neutral',
                                              'gaslight_union': 'Allied',
                                              'neon_serpents': 'Neutral',
                                              'volt_yakuza': 'Neutral'},
                         'units': ['RustySedan', 'GuardTruck']},
    'volt_yakuza': {   'control': 60,
                       'description': 'An elite criminal syndicate that runs '
                                      'the underground circuit from penthouse '
                                      'garages above the smog line. They '
                                      'enforce their territory with '
                                      'militarized convoys and consider street '
                                      'racing a sacred ritual of honor.',
                       'faction_boss': {   'damage_multiplier': 2.5,
                                           'hp_multiplier': 6.0,
                                           'name': 'Oyabun Raiden',
                                           'vehicle': 'WarRig'},
                       'hub_city_coordinates': [3000, 4000],
                       'name': 'Volt Yakuza',
                       'relationships': {   'chrome_phantoms': 'Neutral',
                                            'gaslight_union': 'Hostile',
                                            'neon_serpents': 'Hostile',
                                            'the_underpass': 'Neutral'},
                       'units': ['WarRig', 'GuardTruck', 'Peacekeeper']}}
