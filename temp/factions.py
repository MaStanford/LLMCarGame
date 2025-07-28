FACTION_DATA = {   'canopy_stalkers': {   'control': 50,
                           'description': 'Remnants of an elite military unit, '
                                          'they have adapted to the new world '
                                          'by becoming apex predators. They '
                                          'use speed and stealth to hunt both '
                                          'mutated beasts and rival factions '
                                          'in the dense, city-sized forests.',
                           'faction_boss': {   'damage_multiplier': 3.5,
                                               'hp_multiplier': 3.8,
                                               'name': 'Colonel Vine',
                                               'vehicle': 'SportsCar'},
                           'hub_city_coordinates': [-50, -40],
                           'name': 'The Canopy Stalkers',
                           'relationships': {   'gilded_mycelium': 'Allied',
                                                'rust_bloom_scavengers': 'Hostile',
                                                'the_root_wardens': 'Neutral',
                                                'thorn_sworn': 'Hostile'},
                           'units': ['SportsCar', 'Hotrod', 'RaiderBuggy']},
    'gilded_mycelium': {   'control': 50,
                           'description': 'A strange collective that '
                                          'cultivates and harvests '
                                          'psychoactive fungi from the ruins. '
                                          'They trade their valuable spores '
                                          'for resources, their minds and '
                                          'goals often as alien as the network '
                                          'of fungus they tend to.',
                           'faction_boss': {   'damage_multiplier': 3.0,
                                               'hp_multiplier': 4.0,
                                               'name': 'Spore-Prophet',
                                               'vehicle': 'PanelWagon'},
                           'hub_city_coordinates': [-35, 20],
                           'name': 'The Gilded Mycelium',
                           'relationships': {   'canopy_stalkers': 'Allied',
                                                'rust_bloom_scavengers': 'Neutral',
                                                'the_root_wardens': 'Neutral',
                                                'thorn_sworn': 'Hostile'},
                           'units': ['Hatchback', 'Van', 'Miner']},
    'rust_bloom_scavengers': {   'control': 50,
                                 'description': 'Pragmatic survivors who see '
                                                'the overgrown world as a '
                                                'treasure trove. They expertly '
                                                'navigate the treacherous '
                                                'wilds to salvage old-world '
                                                'tech, their vehicles '
                                                'reinforced with scrap metal '
                                                'and blooming with parasitic, '
                                                'metal-leaching fungi.',
                                 'faction_boss': {   'damage_multiplier': 2.2,
                                                     'hp_multiplier': 6.0,
                                                     'name': 'Old Man Rust',
                                                     'vehicle': 'Miner'},
                                 'hub_city_coordinates': [25, 50],
                                 'name': 'The Rust-Bloom Scavengers',
                                 'relationships': {   'canopy_stalkers': 'Hostile',
                                                      'gilded_mycelium': 'Neutral',
                                                      'the_root_wardens': 'Neutral',
                                                      'thorn_sworn': 'Hostile'},
                                 'units': ['Truck', 'Technical', 'RustySedan']},
    'the_root_wardens': {   'control': 100,
                            'description': 'Guardians of the central, '
                                           'overgrown city, they seek to live '
                                           'in harmony with the new world, '
                                           'protecting the balance of the '
                                           'Verdant Rot. They are a neutral '
                                           'faction, trading with all who come '
                                           'in peace.',
                            'faction_boss': None,
                            'hub_city_coordinates': [0, 0],
                            'name': 'The Root Wardens',
                            'relationships': {   'canopy_stalkers': 'Neutral',
                                                 'gilded_mycelium': 'Neutral',
                                                 'rust_bloom_scavengers': 'Neutral',
                                                 'thorn_sworn': 'Neutral'},
                            'units': ['Van', 'PanelWagon', 'Sedan']},
    'thorn_sworn': {   'control': 50,
                       'description': 'Fanatical devotees of the Verdant Rot, '
                                      'they believe the rampant growth is a '
                                      'cleansing fire. They adorn their '
                                      'vehicles with razor-sharp vines and '
                                      'thorns, seeing technology as a blight '
                                      'to be purged.',
                       'faction_boss': {   'damage_multiplier': 2.8,
                                           'hp_multiplier': 5.5,
                                           'name': 'Matron of Thorns',
                                           'vehicle': 'WarRig'},
                       'hub_city_coordinates': [40, -30],
                       'name': 'The Thorn-Sworn',
                       'relationships': {   'canopy_stalkers': 'Hostile',
                                            'gilded_mycelium': 'Hostile',
                                            'rust_bloom_scavengers': 'Hostile',
                                            'the_root_wardens': 'Hostile'},
                       'units': ['RaiderBuggy', 'RustySedan', 'Technical']}}
