import sys
sys.path.insert(0, ".")
import unittest

from coalib.parsing.StringProcessing import position_is_escaped


class StringProcessingTest(unittest.TestCase):
    def setUp(self):
        # The backslash character. Needed since there are limitations when
        # using backslashes at the end of raw-strings in front of the
        # terminating " or '.
        self.bs = "\\"

        # Basic test strings all StringProcessing functions should test.
        self.test_strings = [
            r"out1 'escaped-escape:        \\ ' out2",
            r"out1 'escaped-quote:         \' ' out2",
            r"out1 'escaped-anything:      \X ' out2",
            r"out1 'two escaped escapes: \\\\ ' out2",
            r"out1 'escaped-quote at end:   \'' out2",
            r"out1 'escaped-escape at end:  \\' out2",
            r"out1           'str1' out2 'str2' out2",
            r"out1 \'        'str1' out2 'str2' out2",
            r"out1 \\\'      'str1' out2 'str2' out2",
            r"out1 \\        'str1' out2 'str2' out2",
            r"out1 \\\\      'str1' out2 'str2' out2",
            r"out1         \\'str1' out2 'str2' out2",
            r"out1       \\\\'str1' out2 'str2' out2",
            r"out1           'str1''str2''str3' out2",
            r"",
            r"out1 out2 out3",
            self.bs,
            2 * self.bs]

        # Test string for multi-pattern tests (since we want to variate the
        # pattern, not the test string).
        self.multi_pattern_test_string = (r"abcabccba###\\13q4ujsabbc\+'**'ac"
                                          r"###.#.####-ba")
        # Multiple patterns for the multi-pattern tests.
        self.multi_patterns = [r"abc",
                               r"ab",
                               r"ab|ac",
                               2 * self.bs,
                               r"#+",
                               r"(a)|(b)|(#.)",
                               r"(?:a(b)*c)+",
                               r"1|\+"]

        # Test strings for the remove_empty_matches feature (alias auto-trim).
        self.auto_trim_test_pattern = r";"
        self.auto_trim_test_strings = [
            r";;;;;;;;;;;;;;;;",
            r"\\;\\\\\;\\#;\\\';;\;\\\\;+ios;;",
            r"1;2;3;4;5;6;",
            r"1;2;3;4;5;6;7",
            r"",
            r"Hello world",
            r"\;",
            r"\\;",
            r"abc;a;;;;;asc"]

    def assertResultsEqual(self,
                           func,
                           invocation_and_results,
                           postprocess=lambda result: result):
        """
        Tests each given invocation against the given results with the
        specified function.

        :param func:                   The function to test.
        :param invocation_and_results: A dict containing the invocation tuple
                                       as key and the result as value.
        :param postprocess:            A function that shall process the
                                       returned result from the tested
                                       function. The function must accept only
                                       one parameter as postprocessing input.
                                       Performs no postprocessing by default.
        """
        for args, result in invocation_and_results.items():
            self.assertEqual(postprocess(func(*args)), result)

    def assertResultsEqualEx(self,
                             func,
                             invocation_and_results,
                             postprocess=lambda result: result):
        """
        Tests each given invocation against the given results with the
        specified function. This is an extended version of assertResultsEqual()
        that supports also **kwargs.

        :param func:                   The function to test.
        :param invocation_and_results: A dict containing the invocation tuple
                                       as key and the result as value. The
                                       tuple contains (args, kwargs).
        :param postprocess:            A function that shall process the
                                       returned result from the tested
                                       function. The function must accept only
                                       one parameter as postprocessing input.
                                       Performs no postprocessing by default.
        """
        for (args, kwargs), result in invocation_and_results.items():
            self.assertEqual(postprocess(func(*args, **kwargs)), result)

    def assertIteratorElementsEqual(self, iterator1, iterator2):
        """
        Checks whether each element in the iterators and their length do equal.

        :param iterator1: The first iterator.
        :param iterator2: The second iterator.
        """
        for x in iterator1:
            self.assertEqual(x, next(iterator2))

        self.assertRaises(StopIteration, next, iterator2)

    # Test the position_is_escaped() function with a basic test string.
    def test_position_is_escaped(self):
        test_string = r"\\\\\abcabccba###\\13q4ujsabbc\+'**'ac###.#.####-ba"
        result_dict = {
            0: False,
            1: True,
            2: False,
            3: True,
            4: False,
            5: True,
            6: False,
            7: False,
            17: False,
            18: True,
            19: False,
            30: False,
            31: True,
            50: False,
            51: False,
            6666666: False,
            -1: False,
            -20: True,
            -21: False}
        for position, value in result_dict.items():
            self.assertEqual(position_is_escaped(test_string, position), value)

    # Test the position_is_escaped() with more test strings from this class.
    def test_position_is_escaped_advanced(self):
        expected_results = [
            30 * [False] + [True] + 7 * [False],
            30 * [False] + [True] + 7 * [False],
            30 * [False] + [True] + 7 * [False],
            28 * [False] + [True, False, True] + 7 * [False],
            31 * [False] + [True] + 6 * [False],
            31 * [False] + [True] + 6 * [False],
            38 * [False],
            6 * [False] + [True] + 31 * [False],
            6 * [False] + [True, False, True] + 29 * [False],
            6 * [False] + [True] + 31 * [False],
            6 * [False] + [True, False, True] + 29 * [False],
            14 * [False] + [True] + 23 * [False],
            12 * [False] + [True, False, True] + 23 * [False],
            38 * [False],
            [],
            14 * [False],
            [False],
            [False, True]]

        results = [[position_is_escaped(test_string, i)
                    for i in range(len(test_string))]
                   for test_string in self.test_strings]

        zipped = [zip(x, y) for x, y in zip(expected_results, results)]
        flattened = [item for sublist in zipped for item in sublist]

        for elem in flattened:
            self.assertEqual(elem[0], elem[1])

if __name__ == '__main__':
    unittest.main(verbosity=2)

