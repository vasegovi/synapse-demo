IF NOT EXISTS (SELECT * FROM sys.objects O JOIN sys.schemas S ON O.schema_id = S.schema_id WHERE O.NAME = 'Predictions' AND O.TYPE = 'U' AND S.NAME = 'ML')
CREATE TABLE ML.Predictions
	(
	 [CustomerKey] bigint,
	 [GeographyKey] bigint,
	 [CustomerAlternateKey] nvarchar(4000),
	 [MaritalStatus] nvarchar(4000),
	 [Gender] nvarchar(4000),
	 [SalaryYear] bigint,
	 [TotalChildren] bigint,
	 [NumberChildrenAtHome] bigint,
	 [EnglishEducation] nvarchar(4000),
	 [EnglishOccupation] nvarchar(4000),
	 [HouseOwnerFlag] bigint,
	 [NumberCarsOwned] bigint,
	 [CommuteDistance] nvarchar(4000),
	 [Region] nvarchar(4000),
	 [Age] bigint,
	 [BikeBuyer] bigint
	)
WITH
	(
	DISTRIBUTION = ROUND_ROBIN,
	 CLUSTERED COLUMNSTORE INDEX
	 -- HEAP
	)
GO

--Uncomment the 4 lines below to create a stored procedure for data pipeline orchestration​
--CREATE PROC bulk_load_Predictions
--AS
--BEGIN
COPY INTO ML.Predictions
(CustomerKey 1, GeographyKey 2, CustomerAlternateKey 3, MaritalStatus 4, Gender 5, SalaryYear 6, TotalChildren 7, NumberChildrenAtHome 8, EnglishEducation 9, EnglishOccupation 10, HouseOwnerFlag 11, NumberCarsOwned 12, CommuteDistance 13, Region 14, Age 15, BikeBuyer 16)
FROM 'https://streamdatalake.dfs.core.windows.net/datalake/TargetMail.csv'
WITH
(
	FILE_TYPE = 'CSV'
	,MAXERRORS = 0
	,FIRSTROW = 11	
)
--END
GO

SELECT TOP 100 * FROM ML.Predictions
GO