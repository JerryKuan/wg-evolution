import unittest
import json

from pandas.util.testing import assert_frame_equal

from implementations.code_df.reviews_github import ReviewsGitHub


def read_file(path):
    """
    Given a line-by-line JSON file, this function converts it to
    a Python dictionary and returns all such lines as a list.

    :param path: the path to the JSON file

    :returns items: a list of dictionaries read from the JSON file
    """

    items = list()
    with open(path, 'r') as raw_data:
        for line in raw_data:
            line = json.loads(line)

            items.append(line)
    return items


class TestReviewsGitHub(unittest.TestCase):

    def setUp(self):
        """
        Run before each test to read the test data file
        """

        self.items = read_file('data/test_pulls_data.json')

    def test_compute_trivial(self):
        """
        Test the compute method of a ReviewsGitHub
        object with default parameters.
        """

        reviews = ReviewsGitHub(self.items)
        expected_count = 20
        count = reviews.compute()
        self.assertEqual(expected_count, count)

    def test_compute_with_duplicate(self):
        """
        Test the compute method of a ReviewsGitHub
        object with default parameters but with a
        duplicate item in the test data.
        """

        items_temp = self.items
        items_temp.append(self.items[0])
        reviews = ReviewsGitHub(items_temp)
        expected_count = 20
        count = reviews.compute()
        self.assertEqual(expected_count, count)

    def test__agg(self):
        """
        Test the _agg method of a ReviewsGitHub
        object with default parameters when re-sampling
        on a weekly basis.
        """

        reviews = ReviewsGitHub(self.items)
        reviews.df = reviews.df.set_index('created_date')
        test_df = reviews.df
        test_df = test_df.resample('W')['category'].agg(['count'])

        reviews.df = reviews._agg(reviews.df, 'W')
        assert_frame_equal(test_df, reviews.df)

    def test__get_params(self):
        """
        Test whether the _get_params method correctly returns
        the expected parameters for plotting a timeseries plot
        for the Reviews metric.
        """

        changes = ReviewsGitHub(self.items)
        params = changes._get_params()

        expected_params = {
            'x': None,
            'y': 'count',
            'title': "Trends in Reviews Created",
            'use_index': True
        }

        self.assertEqual(expected_params, params)


if __name__ == '__main__':
    unittest.main(verbosity=2)
