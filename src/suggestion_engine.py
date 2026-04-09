import wordfreq

class SuggestionEngine:
    def __init__(self, language='en'):
        self.language = language
        self.frequent_words = wordfreq.top_n_list(lang=self.language, n=50000, wordlist='best')

    def get_suggestions(self, prefix, limit=5):
        if len(prefix) < 2:
            return []
        
        prefix_lower = prefix.lower()
        matches = []
        for word in self.frequent_words:
            if word.startswith(prefix_lower):
                matches.append(word)
            if len(matches) >= limit:
                break
        return matches
