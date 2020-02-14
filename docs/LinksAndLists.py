month_swap_dict = {'janvier': 'Jan',
                   'février': 'Feb',
                   'mars': 'Mar',
                   'avril': 'Apr',
                   'mai': 'May',
                   'juin': 'Jun',
                   'juillet': 'Jul',
                   'août': 'Aug',
                   'septembre': 'Sep',
                   'octobre': 'Oct',
                   'novembre': 'Nov',
                   'décembre': 'Dec'
                   }
# url_dict = {
#     '1week Euribor': "https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-1-semaine.aspx",
#     '1month Euribor': "https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-1-mois.aspx",
#     '3month Euribor': "https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-3-mois.aspx",
#     '6month Euribor': "https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-6-mois.aspx",
#     '12month Euribor': "https://fr.global-rates.com/taux-de-interets/euribor/taux-de-interets-euribor-12-mois.aspx",
#     'EONIA': "https://fr.global-rates.com/taux-de-interets/eonia/eonia.aspx",
#     '1week LiborEUR': "https://fr.global-rates.com/taux-de-interets/libor/euro-europeen/eur-libor-interets-1-semaine.aspx",
#     '1month LiborEUR': "https://fr.global-rates.com/taux-de-interets/libor/euro-europeen/eur-libor-interets-1-mois.aspx",
#     '3month LiborEUR': "https://fr.global-rates.com/taux-de-interets/libor/euro-europeen/eur-libor-interets-3-mois.aspx",
#     '6month LiborEUR': "https://fr.global-rates.com/taux-de-interets/libor/euro-europeen/eur-libor-interets-6-mois.aspx",
#     '12month LiborEUR': "https://fr.global-rates.com/taux-de-interets/libor/euro-europeen/eur-libor-interets-12-mois.aspx",
#     'Overnight LiborEUR': "https://fr.global-rates.com/taux-de-interets/libor/euro-europeen/eur-libor-interets-overnight.aspx",
#     '1week LiborUSD': "https://fr.global-rates.com/taux-de-interets/libor/dollar-americain/usd-libor-interets-1-semaine.aspx",
#     '1month LiborUSD': "https://fr.global-rates.com/taux-de-interets/libor/dollar-americain/usd-libor-interets-1-mois.aspx",
#     '3month LiborUSD': "https://fr.global-rates.com/taux-de-interets/libor/dollar-americain/usd-libor-interets-3-mois.aspx",
#     '6month LiborUSD': "https://fr.global-rates.com/taux-de-interets/libor/dollar-americain/usd-libor-interets-6-mois.aspx",
#     '12month LiborUSD': "https://fr.global-rates.com/taux-de-interets/libor/dollar-americain/usd-libor-interets-12-mois.aspx",
#     'Overnight LiborUSD': "https://fr.global-rates.com/taux-de-interets/libor/dollar-americain/usd-libor-interets-overnight.aspx",
#     '1week LiborGBP': "https://fr.global-rates.com/taux-de-interets/libor/livre-sterling-britannique/gbp-libor-interets-1-semaine.aspx",
#     '1month LiborGBP': "https://fr.global-rates.com/taux-de-interets/libor/livre-sterling-britannique/gbp-libor-interets-1-mois.aspx",
#     '3month LiborGBP': "https://fr.global-rates.com/taux-de-interets/libor/livre-sterling-britannique/gbp-libor-interets-3-mois.aspx",
#     '6month LiborGBP': "https://fr.global-rates.com/taux-de-interets/libor/livre-sterling-britannique/gbp-libor-interets-6-mois.aspx",
#     '12month LiborGBP': "https://fr.global-rates.com/taux-de-interets/libor/livre-sterling-britannique/gbp-libor-interets-12-mois.aspx",
#     'Overnight LiborGBP': "https://fr.global-rates.com/taux-de-interets/libor/livre-sterling-britannique/gbp-libor-interets-overnight.aspx",
#     }

url_dict_inflation = {
    'Inflation Germany' : "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/allemagne.aspx",
    'Inflation China': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/chine.aspx",
    'Inflation US': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/bresil.aspx",
    'Inflation France': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/france.aspx",
    'Inflation GB': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/grande-bretagne.aspx",
    'Inflation India': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/inde.aspx",
    'Inflation Italy': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/italie.aspx",
    'Inflation Japan': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/japon.aspx",
    'Inflation Russia': "https://fr.global-rates.com/statistiques-economiques/inflation/indice-des-prix-a-la-consommation/ipc/russie.aspx",
    }

listFTSE = ['ADM.L', 'AAL.L', 'ANTO.L', 'AHT.L', 'ABF.L', 'AZN.L', 'AUTO.L', 'AVV.L', 'AV.L', 'BA.L', 'BARC.L',
            'BDEV.L', 'BKG.L', 'BHP.L', 'BP.L', 'BATS.L', 'BLND.L', 'BNZL.L', 'BRBY.L', 'CCL.L', 'CNA.L', 'CCH.L',
            'CPG.L', 'CRH.L', 'CRDA.L', 'DCC.L', 'DGE.L', 'EVR.L', 'EXPN.L', 'FERG.L', 'FLTR.L', 'FRES.L', 'GSK.L',
            'GLEN.L', 'HLMA.L', 'HL.L', 'HSX.L', 'HSBA.L', 'HIK.L', 'IMB.L', 'INF.L', 'IHG.L', 'IAG.L', 'ITRK.L',
            'ITV.L', 'JD.L', 'JMAT.L', 'KGF.L', 'LAND.L', 'LGEN.L', 'LLOY.L', 'LSE.L', 'MNG.L', 'MGGT.L', 'MRO.L',
            'MNDI.L', 'MRW.L', 'NG.L', 'NXT.L', 'NMC.L', 'OCDO.L', 'PSON.L', 'PSN.L', 'PHNX.L', 'POLY.L', 'PRU.L',
            'RB.L', 'REL.L', 'RTO.L', 'RIO.L', 'RMV.L', 'RR.L', 'RBS.L', 'RDSA.L', 'RSA.L', 'SGE.L', 'SBRY.L', 'SDR.L',
            'SMT.L', 'SGRO.L', 'SVT.L', 'SN.L', 'SMDS.L', 'SMIN.L', 'SKG.L', 'SPX.L', 'SSE.L', 'STAN.L', 'SLA.L',
            'STJ.L', 'TW.L', 'TSCO.L', 'TUI.L', 'ULVR.L', 'UU.L', 'VOD.L', 'WTB.L', 'WPP.L']

listCAC40 = ['AC.PA', 'AI.PA', 'AIR.PA', 'MT.AS', 'ATO.PA', 'CS.PA', 'BNP.PA', 'EN.PA', 'CAP.PA', 'CA.PA', 'ACA.PA',
             'BN.PA', 'DSY.PA', 'ENGI.PA', 'EL.PA', 'RMS.PA', 'KER.PA', 'OR.PA', 'LR.PA', 'MC.PA', 'ML.PA', 'ORA.PA',
             'RI.PA', 'UG.PA', 'PUB.PA', 'RNO.PA', 'SAF.PA', 'SGO.PA', 'SAN.PA', 'SU.PA', 'GLE.PA', 'SW.PA', 'STM.PA',
             'FTI', 'HO.PA', 'FP.PA', 'URW.AS', 'VIE.PA', 'DG.PA', 'VIV.PA']

listSP500 = ['MMM', 'ABT', 'ABBV', 'ABMD', 'ACN', 'ATVI', 'ADBE', 'AMD', 'AAP', 'AES', 'AMG', 'AFL', 'A', 'APD', 'AKAM',
             'ALK', 'ALB', 'ARE', 'ALXN', 'ALGN', 'ALLE', 'AGN', 'ADS', 'LNT', 'ALL', 'GOOGL', 'GOOG', 'MO', 'AMZN',
             'AMCR', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP', 'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS',
             'ANTM', 'AON', 'AOS', 'APA', 'AIV', 'AAPL', 'AMAT', 'APTV', 'ADM', 'ARNC', 'ANET', 'AJG', 'AIZ', 'ATO',
             'T', 'ADSK', 'ADP', 'AZO', 'AVB', 'AVY', 'BKR', 'BLL', 'BAC', 'BK', 'BAX', 'BDX', 'BBY', 'BIIB',
             'BLK', 'BA', 'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'CHRW', 'COG', 'CDNS', 'CPB', 'COF',
             'CPRI', 'CAH', 'KMX', 'CCL', 'CAT', 'CBOE', 'CBRE', 'CDW', 'CE', 'CNC', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW',
             'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'XEC', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CTXS', 'CLX', 'CME',
             'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CAG', 'CXO', 'COP', 'ED', 'STZ', 'COO', 'CPRT', 'GLW', 'CTVA',
             'COST', 'COTY', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE', 'DAL', 'XRAY', 'DVN', 'FANG',
             'DLR', 'DFS', 'DISCA', 'DISCK', 'DISH', 'DG', 'DLTR', 'D', 'DOV', 'DOW', 'DTE', 'DUK', 'DRE', 'DD', 'DXC',
             'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'EMR', 'ETR', 'EOG', 'EFX', 'EQIX', 'EQR', 'ESS',
             'EL', 'EVRG', 'ES', 'RE', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FB', 'FAST', 'FRT', 'FDX', 'FIS',
             'FITB', 'FE', 'FRC', 'FISV', 'FLT', 'FLIR', 'FLS', 'FMC', 'F', 'FTNT', 'FTV', 'FBHS', 'FOXA', 'FOX', 'BEN',
             'FCX', 'GPS', 'GRMN', 'IT', 'GD', 'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'GWW', 'HRB', 'HAL',
             'HBI', 'HOG', 'HIG', 'HAS', 'HCA', 'PEAK', 'HP', 'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HFC', 'HOLX', 'HD',
             'HON', 'HRL', 'HST', 'HPQ', 'HUM', 'HBAN', 'HII', 'IEX', 'IDXX', 'INFO', 'ITW', 'ILMN', 'IR', 'INTC',
             'ICE', 'IBM', 'INCY', 'IP', 'IPG', 'IFF', 'INTU', 'ISRG', 'IVZ', 'IPGP', 'IQV', 'IRM', 'JKHY',
             'JBHT', 'SJM', 'JNJ', 'JCI', 'JPM', 'JNPR', 'KSU', 'K', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC', 'KSS',
             'KHC', 'KR', 'LB', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LEG', 'LDOS', 'LEN', 'LLY', 'LNC', 'LIN', 'LKQ',
             'LMT', 'L', 'LOW', 'LYB', 'MTB', 'MAC', 'M', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MKC',
             'MXIM', 'MCD', 'MCK', 'MDT', 'MRK', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', 'MHK', 'TAP', 'MDLZ',
             'MNST', 'MCO', 'MS', 'MOS', 'MSI', 'MSCI', 'MYL', 'NDAQ', 'NOV', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA',
             'NWS', 'NEE', 'NLSN', 'NKE', 'NI', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NLOK', 'NCLH', 'NRG', 'NUE',
             'NVDA', 'NVR', 'ORLY', 'OXY', 'ODFL', 'OMC', 'OKE', 'ORCL', 'PCAR', 'PKG', 'PH', 'PAYX', 'PYPL', 'PNR',
             'PBCT', 'PEP', 'PKI', 'PRGO', 'PFE', 'PM', 'PSX', 'PNW', 'PXD', 'PNC', 'PPG', 'PPL', 'PFG', 'PG', 'PGR',
             'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'PVH', 'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTN', 'O', 'REG',
             'REGN', 'RF', 'RSG', 'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX',
             'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SLG', 'SNA', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'SYK', 'SIVB',
             'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TGT', 'TEL', 'FTI', 'TFX', 'TXN', 'TXT', 'TMO',
             'TIF', 'TJX', 'TSCO', 'TDG', 'TRV', 'TRIP', 'TFC', 'TWTR', 'TSN', 'UDR', 'ULTA', 'USB', 'UAA', 'UA', 'UNP',
             'UAL', 'UNH', 'UPS', 'URI', 'UTX', 'UHS', 'UNM', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX',
             'VIAC', 'V', 'VNO', 'VMC', 'WRB', 'WAB', 'WMT', 'WBA', 'DIS', 'WM', 'WAT', 'WEC', 'WFC', 'WELL',
             'WDC', 'WU', 'WRK', 'WY', 'WHR', 'WMB', 'WLTW', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XYL', 'YUM', 'ZBH', 'ZION',
             'ZTS']  # Delisted ["BRK.B","BF.B", "JEC"]

listDAX = ['ADS.DE', 'ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'CON.DE', '1COV.DE', 'DAI.DE', 'DBK.DE',
           'DB1.DE', 'LHA.DE', 'DPW.DE', 'DTE.DE', 'EOAN.DE', 'FRE.DE', 'FME.DE', 'HEI.DE', 'HEN3.DE', 'IFX.DE',
           'LIN.DE', 'MRK.DE', 'MTX.DE', 'MUV2.DE', 'RWE.DE', 'SAP.DE', 'SIE.DE', 'VOW3.DE', 'VNA.DE', 'WDI.DE']

Indices = dict({'^DJI': 'Dow Jones Industrial',
                '^GSPC': 'S&P500',
                '^IXIC': 'NASDAQ composite',
                '^GDAXI': 'DAX',
                '^FCHI': 'CAC40',
                '^FTSE': 'FTSE',
                '^STOXX50E': 'STOXX50',
                'GC=F': 'L\'OR',
                '^XAU': 'L\'argent',
                'WTI': 'West Texas Intermediate',
                'BZ=F': 'Brent',
                'ZC=F': 'Corn',
                'ZW=F': 'Wheat'
                })  # DELISTED Global dow (^GDOW)

rootDir="./"
pickledDataDirectoryPath="./pickledFiles"
repositoryDirectory = "./Image_Directory"
rateFileDirectory="./RateFiles"
Maturities_Instant_Forward=['IF_3M','IF_6M', 'IF_9M', 'IF_1Y', 'IF_2Y', 'IF_3Y', 'IF_4Y', 'IF_5Y', 'IF_6Y', 'IF_7Y', 'IF_8Y', 'IF_9Y', 'IF_10Y', 'IF_11Y', 'IF_12Y', 'IF_13Y', 'IF_14Y', 'IF_15Y', 'IF_16Y', 'IF_17Y', 'IF_18Y', 'IF_19Y', 'IF_20Y', 'IF_21Y', 'IF_22Y', 'IF_23Y', 'IF_24Y', 'IF_25Y', 'IF_26Y', 'IF_27Y', 'IF_28Y', 'IF_29Y','IF_30Y']
Maturities_Spot_Rate=['SR_3M','SR_6M', 'SR_9M', 'SR_1Y', 'SR_2Y', 'SR_3Y', 'SR_4Y', 'SR_5Y', 'SR_6Y', 'SR_7Y', 'SR_8Y', 'SR_9Y', 'SR_10Y', 'SR_11Y', 'SR_12Y', 'SR_13Y', 'SR_14Y', 'SR_15Y', 'SR_16Y', 'SR_17Y', 'SR_18Y', 'SR_19Y', 'SR_20Y', 'SR_21Y', 'SR_22Y', 'SR_23Y', 'SR_24Y', 'SR_25Y', 'SR_26Y', 'SR_27Y', 'SR_28Y', 'SR_29Y','SR_30Y']