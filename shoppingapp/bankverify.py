from bankdetails.decdata import bankdata

def verify(c, d, cvv):
    bank_data = bankdata()
    res=False
    if c == bank_data['cardnumber'] and d == bank_data['date'] and cvv == bank_data['cvv']:
        res = True
    
    return res
