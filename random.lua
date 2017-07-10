-- Randomness with hex values

-- Seed Lua's random engine, first of all
SEED = 0
random.randomseed(SEED)

function seedForHex(i,j,k)
	rndI, rndJ, rndK = i, j, k
	
	for _ in ipairs(i)
		rndI = rndI * math.random()
	end
	for _ in ipairs(j)
		rndJ = rndJ * math.random()
	end
	for _ in ipairs(k)
		rndK = rndK * math.random()
	end

	return rndI * rndJ * rndK
end
