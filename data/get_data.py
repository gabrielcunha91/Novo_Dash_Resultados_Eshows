import pandas as pd

def initialize_data(id):
    # Dicionário com dados de entrada
    data = {
        "generalRevenue" : pd.DataFrame(),
        "groupsCompanies" : pd.DataFrame(),
        "generalRevenueProposal" : pd.DataFrame(),
        "generalCosts" : pd.DataFrame(),
        "costDetails" : pd.DataFrame(),
        "ratingsRank" : pd.DataFrame(),
        "ratingsRankDetails" : pd.DataFrame(),
        "generalCostsBlueme" : pd.DataFrame(),
        "costsBluemeDetails" : pd.DataFrame(),
        "ratingsRankBlueme" : pd.DataFrame(),
        "ratingsRankDetailsBlueme" : pd.DataFrame(),
        "id": id
    }

    return data