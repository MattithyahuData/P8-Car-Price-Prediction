-- P8 
/*
- Converting Selling_price columns to GBP based on the year of selling
- Converting Present_price 
1 Lakhs = Rupees 100,000

1. Convert to Rupee * 100,000
2. Multiple by GBP(average) [1 rupee ro GBP]

Finding AVG Exchange rates for every year from 2000 to 2017 
2000

*/

SELECT	P8Car_Prices.*, 
		P8IND_to_GBP.Conversion, 
		(P8Car_Prices.Selling_Price * Conversion)*100000 AS GBP_Selling_Price,
		(P8Car_Prices.Present_Price * 100000) * (SELECT P8IND_to_GBP.Conversion
												FROM P8IND_to_GBP
												WHERE Year = 2017) AS GBP_Present_Price
FROM P8Car_Prices 
INNER JOIN P8IND_to_GBP 
ON P8Car_Prices.Year = P8IND_to_GBP.Year;

