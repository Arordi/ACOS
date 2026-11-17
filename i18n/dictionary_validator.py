from dataclasses import dataclass


@dataclass
class DictionaryCheck:
    dictionary_name: str
    word: str
    found: bool
    score: float
    details: str = ""


class DictionaryValidator:

    def __init__(self):
        self.dictionaries = []

    def register_dictionary(self, dictionary):
        self.dictionaries.append(dictionary)

    def check_word(
        self,
        word: str,
        language: str,
    ) -> list[DictionaryCheck]:

        results = []

        for dictionary in self.dictionaries:
            result = dictionary.check(
                word,
                language,
            )

            results.append(result)

        return results

    def aggregate_score(
        self,
        results: list[DictionaryCheck],
    ) -> float:

        if not results:
            return 0.0

        return round(
            sum(
                result.score
                for result in results
            ) / len(results),
            2,
        )


dictionary_validator = DictionaryValidator()
