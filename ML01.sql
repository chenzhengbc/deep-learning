use ScAiMaster
--SPDBSSCP005

/*
select distinct
	b.VendorItemIdClean as VMID,
	ivl.ManufacturerItemIdClean as MMID,
	i.ItemDesc,
	v.VendorDesc,
	m.ManufacturerDesc,
	pm.ProductMasterId,
	identity(int ,1,1) as id
	into #1
from dbo.Item_ProductMasterNate pm
		left join scdm.psm.ItemVendor b on b.ItemKey = pm.ItemKey and b.ItemVendorPriority = 1
		left join scdm.psm.ItemVendorLocation ivl on ivl.ItemKey = pm.ItemKey
		left join scdm.psm.Item i  on i.ItemKey = pm.ItemKey
		left join scdm.psm.Vendor v on v.VendorKey = b.VendorKey
		left join scdm.psm.Manufacturer m on m.ManufacturerKey = ivl.ManufacturerKey
order by ProductMasterId,1,2,3

*/


;with x0 as
(
	select distinct ProductMasterID from #1 
),
x1 as 
(
	select top 1000 ProductMasterID
	from x0
	order by newid()
)
select b.* 
from x1
	inner join #1 b on x1.ProductMasterID = b.ProductMasterID

--select cast((select count(*) from #1) as bigint) * (select count(*) from #1)

--58,903,290,000
----select * from dbo.ProductMasterJack

;with x0 as
(
select 
	iif(isnull(a.ProductMasterId, '') = isnull(b.ProductMasterID, '$%^*)*&'), 1, 0) ProductMasterIdMached,
	iif(isnull(a.VMID, '') = isnull(b.VMID, '$%^*)*&'), 1, 0) VMIDMatched,
	iif(isnull(a.MMID, '') = isnull(b.MMID, '$%^*)*&'), 1, 0) MMIDMatched,
	iif(isnull(a.ItemDesc, '') = isnull(b.ItemDesc, '$%^*)*&'), 1, 0) ItemDescMatched,
	iif(isnull(a.VendorDesc, '') = isnull(b.VendorDesc, '$%^*)*&'), 1, 0) VendorDescMatched,
	iif(isnull(a.ManufacturerDesc, '') = isnull(b.ManufacturerDesc, '$%^*)*&'), 1, 0) ManufacturerDescMatched,

	iif(isnull(a.VMID, '') = isnull(b.MMID, '$%^*)*&'), 1, 0) VMIDMMIDMatched,
	iif(isnull(a.MMID, '') = isnull(b.VMID, '$%^*)*&'), 1, 0) MMIDVMIDMatched,
	a.*, b.id as bid, b.VMID as bVMID, b.MMID as bMMID, b.ItemDesc as bItemDesc, b.VendorDesc as bVendorDesc, b.ManufacturerDesc as bManufacturerDesc
from #1 a
	inner join #1 b on a.id <> b.id
)
select count(*)
from x0 
--where ProductMasterIdMached = 1



--select *
--from #1
--where id in (86175,150634)

