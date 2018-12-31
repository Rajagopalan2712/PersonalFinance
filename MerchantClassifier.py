import pandas as pd
import copy

def classify(data:pd.DataFrame, classifier: dict):
    merchants = data.Description.unique()
    new_cat = copy.deepcopy(classifier)
    for merchant in merchants:
        category_tuple = get_category(merchant, classifier)
        if category_tuple[0]:
            data.loc[data['Description'] == merchant, "Labels"] = category_tuple[1]
        else:
            category = input("Please classify Merchant : " + merchant + " : ")
            if category in new_cat:
                new_cat[category].append(merchant)
            else:
                new_cat[category] = [merchant]

            data.loc[data['Description'] == merchant, "Labels"] = category
    return data, new_cat


def get_category(merchant, classifier:dict):
    categories = classifier.keys()
    for category in categories:
        if merchant in classifier[category]:
            return True, category
    return False, None
