class ZTE_Object:

    # ----------------------------------------------------------------------------------
    def __init__(self, folder_object):
        self.__zipfiles_list = folder_object.zipfiles_list
        self.__instructions_file = folder_object.formula
        self.__primary_keys_file = folder_object.keys
        self.__counters = self.__class__.__extract_counters_from_formulas(self.__instructions_file)
        self.__metrics = self.__class__.__extract_metrics_from_file(self.__instructions_file)
        self.__metrics_names = list(self.__metrics.keys())
        self.__primary_keys = self.__class__.__extract_primary_keys_from_file(self.__primary_keys_file)

    # ----------------------------------------------------------------------------------
    @staticmethod
    def __extract_formulas_from_file(instructions_file):
        with open(instructions_file, 'rt') as f:
            formulas = [formulas_temp.strip() for formulas_temp in f.readlines() if not formulas_temp.isspace()]  # checking for empty lines
        return formulas

    # ----------------------------------------------------------------------------------
    @staticmethod
    def __extract_primary_keys_from_file(primary_keys_file):
        with open(primary_keys_file, 'rt') as f:
            primary_keys = [keys_temp.strip() for keys_temp in f.readlines() if not keys_temp.isspace()]  # checking for empty lines
        return primary_keys

    # ----------------------------------------------------------------------------------
    @classmethod
    def __extract_metrics_from_file(cls, instructions_file):
        metrica_dic = {}
        formulas = cls.__extract_formulas_from_file(instructions_file)
        for formula in formulas:
            metrica = formula[: formula.find('=')].strip()  # formula name (before first '=' )
            expression = formula[formula.find('=') + 1 :]  # formula expression (after first '=' )
            metrica_dic[metrica] = expression.strip()
        return metrica_dic

    # ----------------------------------------------------------------------------------
    @classmethod
    def __extract_counters_from_formulas(cls, instructions_file):
        formulas = cls.__extract_formulas_from_file(instructions_file)  # getting dict with formula name as key and expression as value
        all_counters = []
        for formula in formulas:
            expression = formula[formula.find('=') + 1 :]
            bad_words = '+-/*:.,()!@#$%^&'  # possible bad words in formula expression
            for word in bad_words:
                expression = expression.replace(word, ' ')  # getting rid of possible bad words
            text_list = [
                word.strip() for word in expression.split() if word[0].isalpha() and word[1:].isdigit()
            ]  # counter definiton is word with letter as first char and digits for the leftover
            all_counters += text_list
        return list(set(all_counters))  # list of counters without duplicates

    # ----------------------------------------------------------------------------------
    @property
    def counters(self):
        return self.__counters

    @property
    def metrics(self):
        return self.__metrics

    @property
    def primary_keys(self):
        return self.__primary_keys

    @property
    def zipfiles_list(self):
        return self.__zipfiles_list

    @property
    def metrics_names(self):
        return self.__metrics_names


# ----------------------------------------------------------------------------------
