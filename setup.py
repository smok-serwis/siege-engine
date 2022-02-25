from setuptools import setup


setup(version='1.2',
      entry_points = {
        'my_ep_group_id': [
            'siegeengine = siege_engine.run:run'
        ]
    })
