-- The Hive World model
require("hex")
require("terrain")

-- HexTile: a tile in our Hex world
HexTile = {
}

HexMap = {}

-- Attempt to get existing tile, or create a new one
function HexTile.get(self, i, j, k, data)
	tile = HexMap[{i, j, k}]

	if tile == nil then
		tile = HexTile.new(i, j, k, data)
	end

	return tile
end

-- Create a new tile in position H(i,j,k) with given data
function HexTile.new(i, j, k, data)
	H = Hex(i,j,k)

	tile = {
		pos = H:normalize(),
		known = false,
		data = {}
	}

	setmetatable(tile, HexTile.meta)

	if data == nil then
		-- Generate data here
		math.randomseed()
	else
		-- Parse and process the data input
		for key,this in pairs(data) do
			if key == "terrain" then
				if type(this) == "string" then Terrain(this):set(tile) end
				if type(this) == "table" then this:set(tile) end
			else
				tile.data[key] = this
			end
		end
	end

	HexMap[{tile.pos.i, tile.pos.j, tile.pos.k}] = tile

	return tile
end

-- Add stuff onto this tile
function HexTile:add(datatype, data)
	if self.data[datatype] == nil then
		self.data[datatype] = {}
	end

	if type(data) == "string" then
		table.insert(self.data[datatype], data)
	end

	if type(data) == "table" then
		for i,value in ipairs(data) do
			table.insert(self.data[datatype], data)
		end
	end
end

function HexTile:addSmell(smells)
	self:add("smell", smells)
end

function HexTile:addLiquid(liquids)
	self:add("liquid", liquid)
end

function HexTile:addDust(dust)
	self:add("dust", dust)
end

setmetatable(HexTile, { __call = HexTile.get })

HexTile.meta = {
	__index = HexTile,

	-- Representation
	__tostring = function(self)
		str = "Tile at " .. self.pos
		str = str .. "\nMetadata: {"
		if self.data ~= nil then
			for k,v in pairs(self.data) do
				str = str .. string.format("\n  %s => %s", k, v)
			end
		end
		str = str .. "\n}"
		return str
	end
}
