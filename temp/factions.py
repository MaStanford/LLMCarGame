FACTION_DATA = {   'haven': {   'control': 100,
                 'description': 'A pocket of unnerving calm in the swirling '
                                'madness. Haven is a sanctuary for those who '
                                'have not yet succumbed to the whispers on the '
                                'radio, a place where reality holds, however '
                                'tenuously.',
                 'faction_boss': None,
                 'hub_city_coordinates': [0, 0],
                 'name': 'Haven',
                 'relationships': {   'the_glimmering_host': 'Neutral',
                                      'the_road_wardens': 'Neutral',
                                      'the_signal_keepers': 'Neutral',
                                      'the_whispering_choir': 'Neutral'},
                 'units': ['Sedan', 'Truck', 'Hatchback']},
    'the_glimmering_host': {   'control': 50,
                               'description': 'Victims of the cosmic horror '
                                              'who have been warped into '
                                              'something new. Their vehicles '
                                              'are adorned with crystalline '
                                              'growths and emit a strange, '
                                              'hypnotic light, luring '
                                              'travelers to their doom.',
                               'faction_boss': {   'damage_multiplier': 3.5,
                                                   'hp_multiplier': 3.5,
                                                   'name': 'The Luminary',
                                                   'vehicle': 'SportsCar'},
                               'hub_city_coordinates': [30, 50],
                               'name': 'The Glimmering Host',
                               'relationships': {   'haven': 'Hostile',
                                                    'the_road_wardens': 'Hostile',
                                                    'the_signal_keepers': 'Hostile',
                                                    'the_whispering_choir': 'Neutral'},
                               'units': ['Sedan', 'SportsCar', 'Van']},
    'the_road_wardens': {   'control': 50,
                            'description': 'Grim survivalists who patrol the '
                                           'shifting roads. They see the '
                                           'cosmic horror as just another '
                                           'predator and trust only in '
                                           'firepower and fortified vehicles '
                                           'to keep it at bay.',
                            'faction_boss': {   'damage_multiplier': 2.0,
                                                'hp_multiplier': 6.0,
                                                'name': 'Warden SILAS',
                                                'vehicle': 'Miner'},
                            'hub_city_coordinates': [-20, -45],
                            'name': 'The Road Wardens',
                            'relationships': {   'haven': 'Neutral',
                                                 'the_glimmering_host': 'Hostile',
                                                 'the_signal_keepers': 'Allied',
                                                 'the_whispering_choir': 'Hostile'},
                            'units': ['Truck', 'Technical', 'WarRig']},
    'the_signal_keepers': {   'control': 50,
                              'description': 'A collective of scientists and '
                                             'technicians desperately trying '
                                             'to decipher the radio signals, '
                                             'believing they hold the key to '
                                             'stopping the encroaching '
                                             'madness. They operate from '
                                             'fortified radio towers.',
                              'faction_boss': {   'damage_multiplier': 3.0,
                                                  'hp_multiplier': 4.0,
                                                  'name': 'Lead Researcher '
                                                          'Aris',
                                                  'vehicle': 'Van'},
                              'hub_city_coordinates': [-50, 20],
                              'name': 'The Signal Keepers',
                              'relationships': {   'haven': 'Neutral',
                                                   'the_glimmering_host': 'Hostile',
                                                   'the_road_wardens': 'Allied',
                                                   'the_whispering_choir': 'Hostile'},
                              'units': [   'PanelWagon',
                                           'Technical',
                                           'Hatchback']},
    'the_whispering_choir': {   'control': 50,
                                'description': 'Devotees to the dissonant '
                                               'symphony of the cosmos. They '
                                               'believe the cryptic signals '
                                               'are a holy text and seek to '
                                               "'convert' others by shattering "
                                               'their sanity through '
                                               'broadcasts from their armored '
                                               'vehicles.',
                                'faction_boss': {   'damage_multiplier': 2.5,
                                                    'hp_multiplier': 4.5,
                                                    'name': 'The Conductor',
                                                    'vehicle': 'WarRig'},
                                'hub_city_coordinates': [40, -30],
                                'name': 'The Whispering Choir',
                                'relationships': {   'haven': 'Neutral',
                                                     'the_glimmering_host': 'Neutral',
                                                     'the_road_wardens': 'Hostile',
                                                     'the_signal_keepers': 'Hostile'},
                                'units': [   'Hotrod',
                                             'RustySedan',
                                             'RaiderBuggy']}}
