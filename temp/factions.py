FACTION_DATA = {   'amber_clad': {   'control': 50,
                      'description': 'A mysterious and slow-moving faction '
                                     'that encases their vehicles in thick, '
                                     'hardened sap from colossal, ancient '
                                     'trees, making them nearly '
                                     'indestructible.',
                      'faction_boss': {   'damage_multiplier': 2.5,
                                          'hp_multiplier': 5.5,
                                          'name': 'The Amber Tyrant',
                                          'vehicle': 'WarRig'},
                      'hub_city_coordinates': [-35, 40],
                      'name': 'Amber-Clad',
                      'relationships': {   'glow_spore_cult': 'Neutral',
                                           'nectar_thorns': 'Hostile',
                                           'root_bound_salvagers': 'Allied',
                                           'the_verdant_wardens': 'Neutral'},
                      'units': ['Van', 'Sedan', 'WarRig']},
    'glow_spore_cult': {   'control': 50,
                           'description': 'Zealots who worship the '
                                          'psychoactive, bio-luminescent '
                                          "fungi. They see the 'Veridian "
                                          "Overgrowth' as a divine entity and "
                                          'seek to spread its spores across '
                                          'the wasteland.',
                           'faction_boss': {   'damage_multiplier': 3.0,
                                               'hp_multiplier': 4.0,
                                               'name': 'Prophet of the Bloom',
                                               'vehicle': 'Technical'},
                           'hub_city_coordinates': [45, -30],
                           'name': 'Glow-Spore Cult',
                           'relationships': {   'amber_clad': 'Neutral',
                                                'nectar_thorns': 'Hostile',
                                                'root_bound_salvagers': 'Hostile',
                                                'the_verdant_wardens': 'Neutral'},
                           'units': ['RustySedan', 'RaiderBuggy', 'Technical']},
    'nectar_thorns': {   'control': 50,
                         'description': 'Swift and deadly hunters who utilize '
                                        'a potent paralytic nectar from giant '
                                        'carnivorous flowers. Their vehicles '
                                        'are built for speed and ambush '
                                        'tactics.',
                         'faction_boss': {   'damage_multiplier': 3.5,
                                             'hp_multiplier': 3.5,
                                             'name': 'Queen Briar',
                                             'vehicle': 'SportsCar'},
                         'hub_city_coordinates': [25, 50],
                         'name': 'Nectar-Thorns',
                         'relationships': {   'amber_clad': 'Hostile',
                                              'glow_spore_cult': 'Hostile',
                                              'root_bound_salvagers': 'Neutral',
                                              'the_verdant_wardens': 'Neutral'},
                         'units': ['Hatchback', 'SportsCar', 'Hotrod']},
    'root_bound_salvagers': {   'control': 50,
                                'description': 'Hardy engineers who reinforce '
                                               'their vehicles with the '
                                               'incredibly durable, iron-like '
                                               'roots of the mega-flora. They '
                                               'are masters of defense and '
                                               'attrition.',
                                'faction_boss': {   'damage_multiplier': 2.0,
                                                    'hp_multiplier': 6.0,
                                                    'name': 'Old Man Ironwood',
                                                    'vehicle': 'Miner'},
                                'hub_city_coordinates': [-50, -25],
                                'name': 'Root-Bound Salvagers',
                                'relationships': {   'amber_clad': 'Allied',
                                                     'glow_spore_cult': 'Hostile',
                                                     'nectar_thorns': 'Neutral',
                                                     'the_verdant_wardens': 'Neutral'},
                                'units': ['Miner', 'PanelWagon', 'Truck']},
    'the_verdant_wardens': {   'control': 100,
                               'description': "Guardians of the 'Heartwood,' "
                                              'the oldest and most sacred '
                                              'grove in the reclaimed world. '
                                              'They act as neutral arbiters '
                                              'and protectors of the natural '
                                              'balance.',
                               'faction_boss': None,
                               'hub_city_coordinates': [0, 0],
                               'name': 'The Verdant Wardens',
                               'relationships': {   'amber_clad': 'Neutral',
                                                    'glow_spore_cult': 'Neutral',
                                                    'nectar_thorns': 'Neutral',
                                                    'root_bound_salvagers': 'Neutral'},
                               'units': ['Truck', 'Sedan']}}
