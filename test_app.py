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

            json_response = response.get_json()

            self.assertIn('game_id', json_response)
            self.assertIn('board', json_response) #how to check if contains list of lists?

    def test_api_score_word(self):
        """Test scoring a word from a JSON request"""

        # Your test function will need to use the
        # /api/new-game route, since that makes a new game and returns the game id.

        with app.test_client() as client:


            # Create a new game instance to get the game_id & board

            new_game_response = client.post('/api/new-game')
            new_game_dict = new_game_response.get_json()
            game_id = new_game_dict['game_id']
            word = "PLANT"

            new_game_dict['board'] = [
                ["P", "L", "A", "N", "T"]
            ]

            breakpoint()

            # Test scoring a word for the test game instance

            word_to_score = {"game_id" : game_id, "word" : word}

            score_word_response = client.post(
                '/api/score-word',
                json=word_to_score
            )

            score_word_json = score_word_response.get_json()

            breakpoint()

            self.assertEqual(score_word_json['result'], "ok")








