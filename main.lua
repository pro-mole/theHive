-- And this is the game
DEBUG=true
require("hive")
require("render")

-- Begin by spawning a hive

HexTile( 0,  0,  0, {terrain='Hive'})
HexTile( 1,  0,  0, {terrain='Hive'})
HexTile(-1,  0,  0, {terrain='Hive'})
HexTile( 0,  1,  0, {terrain='Hive'})
HexTile( 0, -1,  0, {terrain='Hive'})
HexTile( 0,  0,  1, {terrain='Hive'})
HexTile( 0,  0, -1, {terrain='Hive'})

for i,H in pairs(HexMap) do
	print(H)
end
