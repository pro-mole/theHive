-- Terrain definition and database

Terrain = {}

TerrainDabatase = {}

function Terrain.new(name, features)
	terrain = {
		name = name
	}

	for k,v in pairs(features) do
		terrain[k] = v
	end

	setmetatable(terrain, Terrain.meta)
	TerrainDabatase[name] = terrain

	return terrain
end

function Terrain.get(name)
	return TerrainDabatase[name]
end

-- Set Terrain data onto tile
function Terrain:set(tile)
	tile.data.terrain = self
	
	tile.data.capacity = self.capacity or 0
	tile:addSmell(tile.data.smell)
	tile:addLiquid(tile.data.liquid)
	tile:addDust(tile.data.dist)
end

setmetatable(Terrain, {
	__call = function(self,name)
		terrain = Terrain.get(name)
		if terrain == nil then
			terrain = Terrain.new(name)
		end
		return terrain
	end
})

Terrain.meta = {
	__index = Terrain,

	--Representation
	__tostring = function(self)
		return self.name
	end
}

-- Populate the Terrain Database
Terrain.new("Hive", {
	smell = "home",
	capacity = 50
})