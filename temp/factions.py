FACTION_DATA = {   'ashen_highwaymen': {   'control': 50,
                            'description': 'Nomadic mercenaries who patrol the '
                                           'overgrown highways, trading and '
                                           'raiding as opportunity dictates. '
                                           'They value freedom and the open '
                                           'road above all else.',
                            'faction_boss': {   'damage_multiplier': 3.5,
                                                'hp_multiplier': 4.0,
                                                'name': 'Road Captain Fury',
                                                'vehicle': 'SportsCar'},
                            'hub_city_coordinates': [-20, -35],
                            'name': 'Ashen Highwaymen',
                            'relationships': {   'gaian_disciples': 'Hostile',
                                                 'reclaimers_of_rust': 'Neutral',
                                                 'the_crossroads': 'Neutral',
                                                 'verdant_wardens': 'Neutral'},
                            'units': ['Hotrod', 'SportsCar', 'Technical']},
    'gaian_disciples': {   'control': 50,
                           'description': 'Fanatical eco-zealots who believe '
                                          "the planet's reclamation is a "
                                          'sacred event. They adorn their '
                                          'vehicles with vines and moss, '
                                          'viewing steel as a necessary evil.',
                           'faction_boss': {   'damage_multiplier': 2.0,
                                               'hp_multiplier': 5.5,
                                               'name': 'Arch-Druid Theron',
                                               'vehicle': 'WarRig'},
                           'hub_city_coordinates': [-30, 40],
                           'name': 'Gaian Disciples',
                           'relationships': {   'ashen_highwaymen': 'Hostile',
                                                'reclaimers_of_rust': 'Hostile',
                                                'the_crossroads': 'Neutral',
                                                'verdant_wardens': 'Neutral'},
                           'units': ['RaiderBuggy', 'Technical', 'Hatchback']},
    'reclaimers_of_rust': {   'control': 50,
                              'description': 'Pragmatic survivors who believe '
                                             "humanity's best chance is to "
                                             'salvage and rebuild using the '
                                             'technology of the old world. '
                                             'They see the Gaians as dangerous '
                                             'luddites.',
                              'faction_boss': {   'damage_multiplier': 2.5,
                                                  'hp_multiplier': 6.0,
                                                  'name': 'Foreman Valerius',
                                                  'vehicle': 'Miner'},
                              'hub_city_coordinates': [45, -25],
                              'name': 'Reclaimers of Rust',
                              'relationships': {   'ashen_highwaymen': 'Neutral',
                                                   'gaian_disciples': 'Hostile',
                                                   'the_crossroads': 'Neutral',
                                                   'verdant_wardens': 'Hostile'},
                              'units': ['Truck', 'Van', 'Miner']},
    'the_crossroads': {   'control': 100,
                          'description': 'The last bastion of true neutrality. '
                                         'A sprawling marketplace built in the '
                                         'shadow of a ruined highway '
                                         'cloverleaf, where all factions can '
                                         'trade under a tense truce.',
                          'faction_boss': None,
                          'hub_city_coordinates': [0, 0],
                          'name': 'The Crossroads',
                          'relationships': {   'ashen_highwaymen': 'Neutral',
                                               'gaian_disciples': 'Neutral',
                                               'reclaimers_of_rust': 'Neutral',
                                               'verdant_wardens': 'Allied'},
                          'units': ['Sedan', 'Truck', 'Hatchback']},
    'verdant_wardens': {   'control': 50,
                           'description': 'A secluded group dedicated to '
                                          'preserving and cultivating the new '
                                          'wilderness, not through worship, '
                                          'but through understanding. They are '
                                          'wary of outsiders but not '
                                          'inherently hostile.',
                           'faction_boss': {   'damage_multiplier': 2.5,
                                               'hp_multiplier': 4.5,
                                               'name': 'Warden Elara',
                                               'vehicle': 'PanelWagon'},
                           'hub_city_coordinates': [30, 30],
                           'name': 'Verdant Wardens',
                           'relationships': {   'ashen_highwaymen': 'Neutral',
                                                'gaian_disciples': 'Neutral',
                                                'reclaimers_of_rust': 'Hostile',
                                                'the_crossroads': 'Allied'},
                           'units': ['PanelWagon', 'Sedan', 'RustySedan']}}
