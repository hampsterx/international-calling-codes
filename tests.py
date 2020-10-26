import yaml
import itertools
import json
import pprint
from deepdiff import DeepDiff
from unittest import TestCase
from collections import Counter


class BaseTests(TestCase):

    @staticmethod
    def dump(data, stop=True):
        print(json.dumps(data, indent=True))
        if stop:
            raise

    def assertDictEqual(self, before, after):
        diff = DeepDiff(before, after, ignore_order=True)

        if diff:
            pprint.pprint(diff)
            return self.assertTrue(False)
        return self.assertTrue(True)


class LocationTests(BaseTests):
    """
    Location Tests
    """

    def setUp(self) -> None:
        self.locations = yaml.load(open('locations.yaml'), Loader=yaml.Loader)

    def test_nz(self):
        items = {k: v for k, v in self.locations.items() if any(c for c in v.values() if c['iso'] == 'NZL')}

        # self.dump(items)

        self.assertDictEqual(
            {
                64: {
                    "New Zealand": {
                        "iso": "NZL",
                        "aliases": []
                    },
                    "Pitcairn": {
                        "iso": "PCN",
                        "aliases": []
                    }
                },
                64240: {
                    "Scott Base (New Zealand)": {
                        "iso": "NZL",
                        "aliases": [
                            "Scott Base",
                            "NEW ZEALAND Scott Base"
                        ]
                    }
                }
            },
            items
        )

    def test_duplicate_codes(self):
        items = {k: list(v.keys()) for k, v in self.locations.items() if len(v) > 1}

        # self.dump(items)

        self.assertDictEqual(
            {
                1: [
                    "Canada",
                    "USA"
                ],
                212: [
                    "Morocco",
                    "Western Sahara"
                ],
                246: [
                    "British Indian Ocean Territory",
                    "Diego Garcia"
                ],
                262: [
                    "Mayotte",
                    "Reunion"
                ],
                358: [
                    "Finland",
                    "Aland Islands"
                ],
                590: [
                    "Saint Barthelemy",
                    "Saint Martin",
                    "Guadeloupe"
                ],
                599: [
                    "Curacao",
                    "Caribbean Netherlands"
                ],
                61891: [
                    "Christmas Island",
                    "Cocos Islands"
                ],
                64: [
                    "New Zealand",
                    "Pitcairn"
                ]
            },
            items
        )

    def test_duplicate_countries(self):
        countries = [k for k, count in Counter(itertools.chain(*[v for k, v in self.locations.items()])).items() if
                     count > 1]

        items = {k: list(v.keys()) for k, v in self.locations.items() if any(x for x in v if x in countries)}

        # self.dump(items)

        self.assertDictEqual(
            {
                1658: [
                    "Jamaica"
                ],
                1787: [
                    "Puerto Rico"
                ],
                1809: [
                    "Dominican Republic"
                ],
                1829: [
                    "Dominican Republic"
                ],
                1849: [
                    "Dominican Republic"
                ],
                1876: [
                    "Jamaica"
                ],
                1939: [
                    "Puerto Rico"
                ],
                76: [
                    "Kazakhstan"
                ],
                77: [
                    "Kazakhstan"
                ]
            },
            items
        )