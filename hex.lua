-- Hex model and math
require ("math")


-- Hex coordinates: 3 axis I,J,K defined as 3 lines with an angle of 120 degrees between each 
Hex = {
	i = 0, j = 0, k = 0
}

-- Create hex vectors, of course
function Hex.new(I, J, K) 
	H = {
		i = I or 0,
		j = J or 0,
		k = K or 0
	}

	return setmetatable(H, Hex.meta)
end

-- Normalize hex vector; very important operation
-- This makes sure that every Hex vector is represented in one single way (as the Hex vector with smallest norm, basically)
function Hex:normalize()
	if not self.normalized then
		I,J,K = self.i, self.j, self.k

		-- Based on the principle that I+J+K = 0...
		repeat 
			dH = math.abs(I) + math.abs(J) + math.abs(K)
			dHPlus = math.abs(I+1) + math.abs(J+1) + math.abs(K+1)
			dHMinus = math.abs(I-1) + math.abs(J-1) + math.abs(K-1)

			if dHPlus < dHMinus and dHPlus < dH then
				I,J,K = I+1, J+1, K+1
			end

			if dHMinus < dHPlus and dHMinus < dH then
				I,J,K = I-1, J-1, K-1
			end
		until dH < dHPlus and dH < dHMinus

		self.normalized = Hex.new(I, J, K)
	end

	return self.normalized
end

-- Norm, works just like vectors
-- Norm 1 (default) defines the step distance
function Hex:norm(n)
	self:normalize()

	exp = n or 1
	if (exp == 1) then
		return math.abs(self.normalized.i) + math.abs(self.normalized.j) + math.abs(self.normalized.k)
	end

	return math.pow(math.pow(math.abs(self.normalized.i), exp) + math.pow(math.abs(self.normalized.j), exp) + math.pow(math.abs(self.normalized.k), exp), 1.0/exp)
end

-- Cartesian distance
-- Now this is for actual geometric space distance
function Hex:distance()
	self:toXY()
	return math.sqrt(math.pow(self.XY.x, 2), math.pow(self.XY.y, 2))
end

-- Convert Hex to Cartesian coordinates
function Hex:toXY()
	if not self.XY then
		self.XY = {
			x = self.i * Hex.I.XY.x + self.j * Hex.J.XY.x + self.k * Hex.K.XY.x, 
			y = self.i * Hex.I.XY.y + self.j * Hex.J.XY.y + self.k * Hex.K.XY.y
		}
	end

	return self.XY
end
	
Hex.meta = {
	__index = Hex,
	__call = Hex.new,

	-- Arithmetic operations
	__add = function(a, b)
		return Hex.new(a.i + b.i, a.j + b.j, a.k + b.k)
	end,
	__sub = function(a, b)
		return Hex.new(a.i - b.i, a.j - b.j, a.k - b.k)
	end,
	__unm = function(a)
		return Hex.new(-a.i, -a.j, -a.k)
	end,
	__eq = function(a,b)
		a:normalize()
		b:normalize()

		return a.normalized.i == b.normalized.i and a.normalized.j == b.normalized.j and a.normalized.k == b.normalized.k
	end,

	-- Representation
	__tostring = function(self)
		return "HEX(" .. self.i .. ";" .. self.j .. ";" .. self.k .. ")";
	end
}

-- Definition of the unitary hex vectors and their respective X/Y conversion functions
Hex.Zero = Hex.new(0,0,0)
Hex.Zero.XY = {x = 0, y = 0}
Hex.I = Hex.new(1,0,0)
Hex.I.XY = {x = 1, y = 0}
Hex.J = Hex.new(0,1,0)
Hex.J.XY = {x = -0.5, y = -1/3}
Hex.K = Hex.new(0,0,1)
Hex.K.XY = {x = -0.5, y = 1/3}

-- Mathematical assertions!
assert(Hex.I + Hex.J == -Hex.K, "I + J != -K")
assert(Hex.I + Hex.K == -Hex.J, "I + K != -J")
assert(Hex.J + Hex.K == -Hex.I, "J + K != -I")
assert(Hex.J + Hex.K + Hex.I == Hex.Zero, "I + J + K != 0")
assert((Hex.I + Hex.J + Hex.K):norm() == Hex.Zero:norm(), "|I + J + K| != 0")