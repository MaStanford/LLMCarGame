FACTION_DATA = {   'dust_devils': {   'control': 50,
                       'description': 'Nomadic raiders who sweep through '
                                      'decaying towns like desert storms, '
                                      'leaving nothing but dust in their wake. '
                                      'Their only loyalty is to their hoard '
                                      'and the open road.',
                       'faction_boss': {   'damage_multiplier': 3.0,
                                           'hp_multiplier': 4.8,
                                           'name': 'Sand King Scorch',
                                           'vehicle': 'Technical'},
                       'hub_city_coordinates': [-3000, -3000],
                       'name': 'Dust Devils',
                       'relationships': {   'phantom_drifters': 'Hostile',
                                            'rusted_ironclads': 'Allied',
                                            'the_last_outpost': 'Neutral',
                                            'whispering_gears': 'Hostile'},
                       'units': ['Technical', 'RustySedan', 'RaiderBuggy']},
    'phantom_drifters': {   'control': 50,
                            'description': 'Ghostly figures who traverse the '
                                           'forgotten highways, their modified '
                                           'vehicles barely making a sound. '
                                           'They seek ancient knowledge and '
                                           'lost technologies, vanishing as '
                                           'quickly as they appear.',
                            'faction_boss': {   'damage_multiplier': 3.2,
                                                'hp_multiplier': 4.0,
                                                'name': 'The Whisperer',
                                                'vehicle': 'RaiderBuggy'},
                            'hub_city_coordinates': [4000, -4000],
                            'name': 'Phantom Drifters',
                            'relationships': {   'dust_devils': 'Hostile',
                                                 'rusted_ironclads': 'Hostile',
                                                 'the_last_outpost': 'Neutral',
                                                 'whispering_gears': 'Allied'},
                            'units': [   'RaiderBuggy',
                                         'MuscleCar',
                                         'Peacekeeper']},
    'rusted_ironclads': {   'control': 50,
                            'description': 'Survivors who have embraced the '
                                           'rust, forging powerful, ramshackle '
                                           'war machines from the bones of the '
                                           'old world. They believe strength '
                                           'is the only currency.',
                            'faction_boss': {   'damage_multiplier': 2.8,
                                                'hp_multiplier': 5.5,
                                                'name': 'Grand Marshall Rust',
                                                'vehicle': 'WarRig'},
                            'hub_city_coordinates': [-4000, 4000],
                            'name': 'Rusted Ironclads',
                            'relationships': {   'dust_devils': 'Allied',
                                                 'phantom_drifters': 'Hostile',
                                                 'the_last_outpost': 'Neutral',
                                                 'whispering_gears': 'Hostile'},
                            'units': ['WarRig', 'ArmoredTruck', 'Miner']},
    'the_last_outpost': {   'control': 100,
                            'description': 'A beacon in the decay, where weary '
                                           'travelers seek refuge and fleeting '
                                           'hope amidst the whispers of '
                                           'forgotten times. A neutral haven '
                                           'for all.',
                            'faction_boss': None,
                            'hub_city_coordinates': [0, 0],
                            'name': 'The Last Outpost',
                            'relationships': {   'dust_devils': 'Neutral',
                                                 'phantom_drifters': 'Neutral',
                                                 'rusted_ironclads': 'Neutral',
                                                 'whispering_gears': 'Neutral'},
                            'units': ['RustySedan', 'Technical']},
    'whispering_gears': {   'control': 50,
                            'description': 'Master mechanics and engineers, '
                                           'they salvage and restore the '
                                           'relics of a forgotten industrial '
                                           'age. Their vehicles are sleek and '
                                           'efficient, believing true power '
                                           'lies in precision and ingenuity.',
                            'faction_boss': {   'damage_multiplier': 2.5,
                                                'hp_multiplier': 5.0,
                                                'name': 'The Automaton',
                                                'vehicle': 'GuardTruck'},
                            'hub_city_coordinates': [3000, 3000],
                            'name': 'Whispering Gears',
                            'relationships': {   'dust_devils': 'Hostile',
                                                 'phantom_drifters': 'Allied',
                                                 'rusted_ironclads': 'Hostile',
                                                 'the_last_outpost': 'Neutral'},
                            'units': [   'GuardTruck',
                                         'MuscleCar',
                                         'Peacekeeper']}}
