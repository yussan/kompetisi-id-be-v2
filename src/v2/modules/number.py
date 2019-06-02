def convertToRelativeCurrency(currency):
  if (currency > 1000000000): 
    currency = str(currency / 1000000000) + " milyar"
  elif (currency > 1000000): 
    currency = str(currency / 1000000) + " juta"
  elif (currency > 100000): 
    currency = str(currency / 1000) + " ribu"
  return "IDR " + str(currency)