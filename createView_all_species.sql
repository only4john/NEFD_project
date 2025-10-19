-- 步骤 1: 首先删除所有依赖视图，解锁表格
DROP VIEW IF EXISTS "all_species_view";

-- 步骤 2: 删除所有由我们的项目创建的表格（包括所有错误的版本）
DROP TABLE IF EXISTS "All_species"; -- 大小写错误
DROP TABLE IF EXISTS "all_species";
DROP TABLE IF EXISTS "cypress_species";
DROP TABLE IF EXISTS "douglas_fir";
DROP TABLE IF EXISTS "eucalypts";
DROP TABLE IF EXISTS "other_hardwoods";
DROP TABLE IF EXISTS "other_softwoods";
DROP TABLE IF EXISTS "radiata_pine";
DROP TABLE IF EXISTS "radiata_pine_pruned_"; -- 名字被截断
DROP TABLE IF EXISTS "radiata_pine_pruned_with_thinning";
DROP TABLE IF EXISTS "radiata_pine_pruned_without_thinning";
DROP TABLE IF EXISTS "radiata_pine_unprune"; -- 名字被截断
DROP TABLE IF EXISTS "radiata_pine_unpruned_with_thinning";
DROP TABLE IF EXISTS "radiata_pine_unpruned_without_thinning";
DROP TABLE IF EXISTS "raidata_pine"; -- 拼写错误
DROP TABLE IF EXISTS "territorial_authorities";
DROP TABLE IF EXISTS "territorial_authority_re"; -- 名字被截断
DROP TABLE IF EXISTS "territorial_authority_relationships";
DROP TABLE IF EXISTS "wood_supply_regions";