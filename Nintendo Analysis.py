import pandas as pd


#================================CREATING DATAFRAMES===============================
nintendo_balance_sheet_data = pd.read_csv('Nintendo_Balance_Sheet.csv')
nintendo_income_statement_data = pd.read_csv('Nintendo_Income_Statement.csv')
nintendo_cash_flow_data = pd.read_csv('Nintendo_Cash_Flows.csv')
nintendoIS = pd.DataFrame(nintendo_income_statement_data)
nintendoBS = pd.DataFrame(nintendo_balance_sheet_data)
nintendoCF = pd.DataFrame(nintendo_cash_flow_data)
#===================================================================================

#================================INDEX LOCATIONS FOR ROWS AND COLUMNS===============
rows_nintendoIS = list(nintendoIS.index)
columns_nintendoIS = list(nintendoIS.columns)
rows_nintendoBS = list(nintendoBS.index)
columns_nintendoBS = list(nintendoBS.columns)
rows_nintendoCF = list(nintendoCF.index)
columns_nintendoCF = list(nintendoCF.columns)

#DATA FRAME BY YEAR
FY18 = '3/31/18'
FY17 = '3/31/17'
FY16 = '3/31/16'
FY15 = '3/31/15'
data_frame_columns = [FY18,FY17,FY16,FY15]

"""
for row in enumerate(rows_nintendoBS):
    print(row)
for row in enumerate(rows_nintendoIS):
    print(row)
"""


#=================================CLEANING DATAFRAMES===============================
#Cleaning Income Statement
nintendoIS = nintendoBS.where(nintendoBS != '-', 0)
nintendoIS = nintendoIS.apply(pd.to_numeric)

#Cleaning Balance Sheet
nintendoBS = nintendoBS.where(nintendoBS != '-', 0)
nintendoBS = nintendoBS.apply(pd.to_numeric)

#Cleaning Cash Flows
nintendoCF = nintendoCF.where(nintendoCF != '-',0)
nintendoCF = nintendoBS.apply(pd.to_numeric)
#====================================================================================
#========================Ratio Lists=================================================
dictionary_of_ratios = {"Current Ratio": [],
                        "Quick Ratio" : [],
                        "Cash Ratio" : [],
                        "Total Debt Ratio" : [],
                        "Equity Multiplier" : [],
                        "Debt-Equity Ratio" : [],
                        "Times Interest Earned Ratio" : [],
                        "Cash Coverage Ratio" : [],
                        "Inventory Turnover": [],
                        "Days Sales in Inventory" : [],
                        "Receivables Turnover" : [],
                        "Payables Turnover" : [],
                        "Days Sales in Receivables" : [],
                        "Days Costs in Payables" : [],
                        "Total Asset Turnover" : [],
                        "Capital Intensity" : [],
                        "Profit Margin" : [],
                        "Return on Assets" : [],
                        "Return on Equity" : []
                        }

#====================================================================================
#========================COMMON FINANCIAL ANALYSIS RATIOS============================

class common_financial_ratios():
    def short_term_solvency(self,current_liabilities,current_assets,inventory,cash):
        self.current_liabilities = current_liabilities
        self.current_assets = current_assets
        self.inventory = inventory
        self.cash = cash
        dictionary_of_ratios['Current Ratio'].append(round(self.current_assets / self.current_liabilities,2))
        dictionary_of_ratios['Quick Ratio'].append(round((self.current_assets - self.inventory) / self.current_liabilities,2))
        dictionary_of_ratios['Cash Ratio'].append(round(self.cash / self.current_liabilities,2))

    def long_term_solvency(self,total_assets,total_equity,EBIT,interest,depreciation):
        self.total_assets = total_assets
        self.total_equity = total_equity
        self.EBIT = EBIT
        self.interest = interest
        self.depreciation = depreciation
        total_debt = self.total_assets - self.total_equity
        dictionary_of_ratios['Total Debt Ratio'].append(round(total_debt / self.total_assets,2))
        dictionary_of_ratios['Debt-Equity Ratio'].append(round(total_debt / self.total_equity,2))
        dictionary_of_ratios['Equity Multiplier'].append(round(self.total_assets / self.total_equity,2))
        dictionary_of_ratios['Times Interest Earned Ratio'].append(round(self.EBIT/self.interest,2))
        dictionary_of_ratios['Cash Coverage Ratio'].append(round((self.EBIT + self.depreciation) / self.interest,2))


    def asset_utilization(self,cost_of_goods_sold,inventory,sales,accounts_recievables,accounts_payable,total_assets):
        days = 365
        self.cost_of_goods_sold = cost_of_goods_sold
        self.inventory = inventory
        self.sales = sales
        self.accounts_recivables = accounts_recievables
        self.accounts_payable = accounts_payable
        self.total_assets = total_assets
        #Inventory Turnover Ratios
        inventory_turnover = round((self.cost_of_goods_sold / self.inventory),2)
        dictionary_of_ratios['Inventory Turnover'].append(inventory_turnover)
        dictionary_of_ratios['Days Sales in Inventory'].append(round((days / inventory_turnover),2))
        #Accounts Receivables Turnover Ratios
        receivables_turnover = round((self.sales / self.accounts_recivables),2)
        dictionary_of_ratios['Receivables Turnover'].append(receivables_turnover)
        dictionary_of_ratios['Days Sales in Receivables'].append(round((days / receivables_turnover),2))
        #Accounts Payable Turnover Ratios
        accounts_payable_turnover = round(self.cost_of_goods_sold / self.accounts_payable,2)
        dictionary_of_ratios['Payables Turnover'].append(accounts_payable_turnover)
        dictionary_of_ratios['Days Costs in Payables'].append(round(days / accounts_payable_turnover,2))
        #Intensity
        dictionary_of_ratios['Total Asset Turnover'].append(round(self.sales / self.total_assets,2))
        dictionary_of_ratios['Capital Intensity'].append(round(self.total_assets / self.sales,2))
        pass
    def profitability(self,net_income,sales,total_assets,total_equity):
        self.net_income = net_income
        self.sales = sales
        self.total_assets = total_assets
        self.total_equity = total_equity
        dictionary_of_ratios['Profit Margin'].append(round((self.net_income / self.sales),2))
        dictionary_of_ratios['Return on Assets'].append(round((self.net_income / self.total_assets) * 100,2))
        dictionary_of_ratios['Return on Equity'].append(round((self.net_income / self.total_equity) * 100,2))

#===================================================================================


#====================FINANCIAL RATIO REQUESTS=======================================
#INITIALIZING CLASS
nintendo_analysis = common_financial_ratios()

#SHORT TERM SOLVENCY
for FY in data_frame_columns:
    nintendo_analysis.short_term_solvency(nintendoBS[FY][17],nintendoBS[FY][5],nintendoBS[FY][3],nintendoBS[FY][0])

#LONG TERM SOLVENCY
for FY in data_frame_columns:
    nintendo_analysis.long_term_solvency(nintendoBS[FY][13],nintendoBS[FY][32],nintendoIS[FY][10],nintendoIS[FY][11],nintendoCF[FY][0])

#ASSET UTILIZATION
for FY in data_frame_columns:
    nintendo_analysis.asset_utilization(nintendoIS[FY][1],nintendoBS[FY][3],nintendoIS[FY][0],nintendoBS[FY][2],nintendoBS[FY][14],nintendoBS[FY][13])

#PROFITABLITY
for FY in data_frame_columns:
    nintendo_analysis.profitability(nintendoIS[FY][16],nintendoIS[FY][0],nintendoBS[FY][13],nintendoBS[FY][32])





#===================FINANCIAL RATIO DATAFRAME=======================================
ratio_dataframe = pd.DataFrame(columns=["FY18","FY17","FY16","FY15"],index= ["Current Ratio","Quick Ratio", "Cash Ratio","Total Debt Ratio","Debt-Equity Ratio","Equity Multiplier",
                                                                             "Times Interest Earned Ratio", "Cash Coverage Ratio", "Inventory Turnover","Days Sales in Inventory",
                                                                             "Receivables Turnover","Payables Turnover", "Days Sales in Receivables", "Days Costs in Payables",
                                                                             "Total Asset Turnover","Capital Intensity", "Profit Margin", "Return on Assets","Return on Equity"])
#Dataframe Appending

i = 0
while i < len(dictionary_of_ratios):
    for key in dictionary_of_ratios:
        ratio_dataframe.iloc[i]=dictionary_of_ratios[key]
        i+=1

print(ratio_dataframe)

#HardCode Appendning
"""
ratio_dataframe.iloc[0] = dictionary_of_ratios['Current Ratio']
ratio_dataframe.iloc[1] = dictionary_of_ratios['Quick Ratio']
ratio_dataframe.iloc[2] = dictionary_of_ratios['Cash Ratio']
"""
#===================================================================================
ratio_dataframe.to_csv('Nintendo Financial Analysis.csv')



