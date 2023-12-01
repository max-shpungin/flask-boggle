from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<table', html)
            # someone might change class.
            # The table for sure needs to be there so '<table' will search
            # ... if this string exists. Not looking for valid HTML

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:

            # the route returns JSON with a string game id,
            #   and a list-of-lists for the board

            # the route stores the new game in the games dictionary

            response = client.post('/api/new-game')

            json = response.get_json()

            self.assertIn('gameId', json)
            self.assertIn('board', json) #how to check if contains list of lists?


