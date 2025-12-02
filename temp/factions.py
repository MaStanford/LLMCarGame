FACTION_DATA = {   'acid_merchants': {   'control': 50,
                          'description': 'Traders dealing in hazardous '
                                         'chemicals, mutagenic agents, and '
                                         'specialized gear for navigating '
                                         'toxic environments. They play all '
                                         'sides, but have a soft spot for '
                                         'those who can get them rare samples.',
                          'faction_boss': {   'damage_multiplier': 3.5,
                                              'hp_multiplier': 4.0,
                                              'name': 'The Purifier',
                                              'vehicle': 'Technical'},
                          'hub_city_coordinates': [-4000, 3000],
                          'name': 'Acid Merchants',
                          'relationships': {   'bio_scavengers': 'Hostile',
                                               'bloom_nexus': 'Neutral',
                                               'spore_sovereignty': 'Neutral',
                                               'toxic_crawlers': 'Allied'},
                          'units': [   'Peacekeeper',
                                       'Technical',
                                       'WarRig',
                                       'Miner']},
    'bio_scavengers': {   'control': 50,
                          'description': 'Resourceful gangs who brave the '
                                         'overgrown ruins to extract rare, '
                                         'bioluminescent materials, often '
                                         'clashing with others over prime '
                                         'scavenging grounds.',
                          'faction_boss': {   'damage_multiplier': 3.0,
                                              'hp_multiplier': 4.5,
                                              'name': 'Glowfang Gus',
                                              'vehicle': 'Hatchback'},
                          'hub_city_coordinates': [3000, 4000],
                          'name': 'Bio-Scavengers',
                          'relationships': {   'acid_merchants': 'Hostile',
                                               'bloom_nexus': 'Neutral',
                                               'spore_sovereignty': 'Hostile',
                                               'toxic_crawlers': 'Hostile'},
                          'units': ['RustySedan', 'Hatchback', 'Technical']},
    'bloom_nexus': {   'control': 100,
                       'description': 'A neutral sanctuary at the heart of the '
                                      'overgrown world, where all factions '
                                      'occasionally trade and recuperate, '
                                      'under the watchful eye of a mysterious, '
                                      'ancient intelligence.',
                       'faction_boss': None,
                       'hub_city_coordinates': [0, 0],
                       'name': 'The Bloom Nexus',
                       'relationships': {   'acid_merchants': 'Neutral',
                                            'bio_scavengers': 'Neutral',
                                            'spore_sovereignty': 'Neutral',
                                            'toxic_crawlers': 'Neutral'},
                       'units': ['RustySedan', 'MuscleCar']},
    'spore_sovereignty': {   'control': 50,
                             'description': 'A collective of mutated survivors '
                                            'and plant-human hybrids, they '
                                            "seek to spread the 'bloom' across "
                                            'the wasteland, believing it to be '
                                            'the next stage of evolution.',
                             'faction_boss': {   'damage_multiplier': 2.8,
                                                 'hp_multiplier': 5.5,
                                                 'name': 'Queen Mycelia',
                                                 'vehicle': 'WarRig'},
                             'hub_city_coordinates': [4000, -3000],
                             'name': 'Spore Sovereignty',
                             'relationships': {   'acid_merchants': 'Neutral',
                                                  'bio_scavengers': 'Hostile',
                                                  'bloom_nexus': 'Neutral',
                                                  'toxic_crawlers': 'Hostile'},
                             'units': [   'Technical',
                                          'RaiderBuggy',
                                          'RustySedan']},
    'toxic_crawlers': {   'control': 50,
                          'description': 'Hardened survivors who thrive in the '
                                         'most irradiated and '
                                         'chemically-polluted zones, their '
                                         'vehicles are crude but resilient, '
                                         'often coated in corrosive '
                                         'byproducts.',
                          'faction_boss': {   'damage_multiplier': 2.2,
                                              'hp_multiplier': 6.0,
                                              'name': 'Lord Corrosive',
                                              'vehicle': 'ArmoredTruck'},
                          'hub_city_coordinates': [-3000, -4000],
                          'name': 'Toxic Crawlers',
                          'relationships': {   'acid_merchants': 'Allied',
                                               'bio_scavengers': 'Hostile',
                                               'bloom_nexus': 'Neutral',
                                               'spore_sovereignty': 'Hostile'},
                          'units': ['Miner', 'ArmoredTruck', 'GuardTruck']}}
