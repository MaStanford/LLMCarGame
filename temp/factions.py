FACTION_DATA = {   'helios_zealots': {   'control': 50,
                          'description': 'Fanatical sun-worshippers who '
                                         'believe the solar catastrophe was a '
                                         "divine event. They seek to 'purify' "
                                         'the shadowed lands with fire.',
                          'faction_boss': {   'damage_multiplier': 3.5,
                                              'hp_multiplier': 3.0,
                                              'name': 'Matriarch Sol',
                                              'vehicle': 'SportsCar'},
                          'hub_city_coordinates': [30, 20],
                          'name': 'Helios Zealots',
                          'relationships': {   'sun_scorched_nomads': 'Neutral',
                                               'the_dynamo_collective': 'Hostile',
                                               'the_umbral_guard': 'Hostile',
                                               'twilight_traders': 'Neutral'},
                          'units': ['SportsCar', 'Hotrod', 'RaiderBuggy']},
    'sun_scorched_nomads': {   'control': 50,
                               'description': 'Hardened survivors who '
                                              'constantly move across the '
                                              'scorched plains, masters of '
                                              'hit-and-run tactics and '
                                              'salvage.',
                               'faction_boss': {   'damage_multiplier': 3.0,
                                                   'hp_multiplier': 4.0,
                                                   'name': 'Scourge',
                                                   'vehicle': 'Technical'},
                               'hub_city_coordinates': [60, -30],
                               'name': 'Sun-Scorched Nomads',
                               'relationships': {   'helios_zealots': 'Neutral',
                                                    'the_dynamo_collective': 'Hostile',
                                                    'the_umbral_guard': 'Hostile',
                                                    'twilight_traders': 'Neutral'},
                               'units': [   'RaiderBuggy',
                                            'RustySedan',
                                            'Hotrod']},
    'the_dynamo_collective': {   'control': 50,
                                 'description': 'A collective of brilliant '
                                                'engineers who have built '
                                                'their society around '
                                                'geothermal vents. They are '
                                                'the primary source of new '
                                                'energy tech.',
                                 'faction_boss': {   'damage_multiplier': 1.5,
                                                     'hp_multiplier': 6.0,
                                                     'name': 'Chief Engineer '
                                                             'Valerius',
                                                     'vehicle': 'Miner'},
                                 'hub_city_coordinates': [-50, -40],
                                 'name': 'The Dynamo Collective',
                                 'relationships': {   'helios_zealots': 'Hostile',
                                                      'sun_scorched_nomads': 'Hostile',
                                                      'the_umbral_guard': 'Neutral',
                                                      'twilight_traders': 'Neutral'},
                                 'units': ['Truck', 'Van', 'Miner']},
    'the_umbral_guard': {   'control': 50,
                            'description': 'Guardians of the last shaded city, '
                                           'possessing advanced '
                                           'energy-shielding technology. They '
                                           'are disciplined and view outsiders '
                                           'with suspicion.',
                            'faction_boss': {   'damage_multiplier': 2.0,
                                                'hp_multiplier': 5.5,
                                                'name': 'Warden Lux',
                                                'vehicle': 'WarRig'},
                            'hub_city_coordinates': [-40, 50],
                            'name': 'The Umbral Guard',
                            'relationships': {   'helios_zealots': 'Hostile',
                                                 'sun_scorched_nomads': 'Hostile',
                                                 'the_dynamo_collective': 'Neutral',
                                                 'twilight_traders': 'Neutral'},
                            'units': ['Sedan', 'PanelWagon', 'Technical']},
    'twilight_traders': {   'control': 100,
                            'description': 'A neutral faction of merchants and '
                                           'information brokers operating from '
                                           'the largest underground '
                                           'crossroads. They serve all, for a '
                                           'price.',
                            'faction_boss': None,
                            'hub_city_coordinates': [0, 0],
                            'name': 'Twilight Traders',
                            'relationships': {   'helios_zealots': 'Neutral',
                                                 'sun_scorched_nomads': 'Neutral',
                                                 'the_dynamo_collective': 'Neutral',
                                                 'the_umbral_guard': 'Neutral'},
                            'units': ['Hatchback', 'Truck']}}
