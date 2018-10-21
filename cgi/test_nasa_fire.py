import unittest

import nasa_fire

class TestNasaFire(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_data_loader(self):
        here = {'lat': 41.4161, 'lon': -81.8583}

        edataset24 = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_24h", here, 24)
        edataset48 = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_48h", here, 48)
        edataset7d = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_7d", here, 7*24)

        self.assertNotEqual(len(edataset24), len(edataset48))
        self.assertNotEqual(len(edataset24), len(edataset7d))
        self.assertNotEqual(len(edataset48), len(edataset7d))

    def test_dist(self):
        here = {'lat': 41.4161, 'lon': -81.8583}
        
        edataset7d = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_7d", here, 7*24)

        self.assertTrue(edataset7d[0]['distance'] < 20)

    def test_distance(self):
        p1 = {'lat': 52.2296756, 'lon': 21.0122287}
        p2 = {'lat': 52.406374, 'lon': 16.9251681}

        self.assertTrue(nasa_fire.distance(p1, p2) < 278.546)
        self.assertTrue(nasa_fire.distance(p1, p2) > 278.545)

    def test_speed(self):
        d2 = {'distance': 2, 'time_frame': 2}
        d1 = {'distance': 1, 'time_frame': 1}

        d0 = {'distance': 0, 'time_frame': 2}

        speed_result = nasa_fire.speed(d1, d2)
        velocity_result = nasa_fire.velocity(d1, d2)

        self.assertEqual(speed_result, 1)
        self.assertEqual(velocity_result, 1)

        speed_result = nasa_fire.speed(      d1, d0)
        velocity_result = nasa_fire.velocity(d1, d0)

        self.assertEqual(speed_result, 1)
        self.assertEqual(velocity_result, -1)

    def test_vadd_velocity(self):
        d2 = {'distance': 2, 'time_frame': 2}
        d1 = {'distance': 1, 'time_frame': 1}

        d0 = {'distance': 0, 'time_frame': 2}

        should_be_d1 = nasa_fire.add_velocity([d1], [d2])

        self.assertEqual(d1, should_be_d1)
    def test_nearest_moving_fire(self):
        here = {'lat': 41.4161, 'lon': -81.8583}

        edataset24 = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_24h", here, 24)
        edataset48 = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_48h", here, 48)
        edataset7d = nasa_fire.load_to_enhanced_plots( r"C:\Users\ATeg\Desktop\kata\firedata\MODIS_C6_USA_contiguous_and_Hawaii_7d", here, 7*24)

        most_recent_dataset = nasa_fire.add_velocity(edataset48, edataset7d)

        closest_moving_fire = nasa_fire.nearest_moving_fire(most_recent_dataset)

        self.assertNotEqual(len(edataset24), len(edataset48))
        self.assertNotEqual(len(edataset24), len(edataset7d))
        self.assertNotEqual(len(edataset48), len(edataset7d))


if __name__ == '__main__':
    unittest.main()