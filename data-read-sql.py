# %%
import pandas as pd
import pyodbc

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'SPDBSSCP005'
database = 'ScAiMaster'
driver = 'SQL Server'

# Windows "Driver=SQL Server;Server=.;Database=nameOfDatabase;Trusted_Connection=Yes;"
cnxn = pyodbc.connect('Driver={driver};Server={server};Database={database};Trusted_Connection=Yes'.format(
    driver=driver, server=server, database=database))
cursor = cnxn.cursor()
query = '''
SELECT
       Item_ProductMasterJack.[ItemKey]
       ,Item_ProductMasterJack.[SourceId]
       ,Item_ProductMasterJack.[ItemSetId]
       ,Item_ProductMasterJack.[ItemId]
       ,[ProductMasterId]
       --,[ItemMapSource] = Item_ProductMasterJack.[MapSource]
       ,[VMID] = ItemVendor.VendorItemIdClean
       ,[MMID] = ItemVendorLocation.ManufacturerItemIdClean
       ,Item.ItemDesc
       ,VendorMaster.VendorDesc
       ,ManufacturerMaster.ManufacturerDesc
FROM [ScAiMaster].[dbo].[Item_ProductMasterTraining] AS Item_ProductMasterJack
       LEFT JOIN SCDM.psm.ItemVendor AS ItemVendor ON
              ItemVendor.ItemKey = Item_ProductMasterJack.ItemKey
              AND ItemVendor.ItemVendorPriority = 1
       LEFT JOIN SCDM.psm.ItemVendorLocation AS ItemVendorLocation ON
              ItemVendorLocation.ItemKey = Item_ProductMasterJack.ItemKey
       LEFT JOIN SCDM.psm.Item AS Item ON
              Item.ItemKey = Item_ProductMasterJack.ItemKey
       LEFT JOIN SCDM.psm.Vendor AS Vendor ON
              Vendor.VendorKey = ItemVendor.VendorKey
       LEFT JOIN SCDM.psm.Vendor_VendorMaster AS Vendor_VendorMaster ON
              Vendor_VendorMaster.VendorKey = Vendor.VendorKey
       LEFT JOIN ScMaster.dbo.VendorMaster AS VendorMaster ON
              VendorMaster.VendorMasterId = Vendor_VendorMaster.VendorMasterId
       LEFT JOIN SCDM.psm.Manufacturer AS Manufacturer ON
              Manufacturer.ManufacturerKey = ItemVendorLocation.ManufacturerKey
       LEFT JOIN SCDM.psm.Manufacturer_ManufacturerMaster AS Manufacturer_ManufacturerMaster ON
              Manufacturer_ManufacturerMaster.ManufacturerKey = Manufacturer.ManufacturerKey
       LEFT JOIN ScMaster.dbo.ManufacturerMaster AS ManufacturerMaster ON
              ManufacturerMaster.ManufacturerMasterId = Manufacturer_ManufacturerMaster.ManufacturerMasterId
'''
df = pd.read_sql(query, cnxn)
df.to_csv('items_all.csv', index=False)


# %%
print(df.info())


# %%
