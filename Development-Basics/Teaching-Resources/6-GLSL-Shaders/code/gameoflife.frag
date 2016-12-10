/*
A GLSL implementation of Conway's Game of Life.

Written for Nic Wolf's Development Basics TouchDesigner workshop.

Author
----------
Nicholas Wolf
*/

out vec4 fragColor;

// Constants for cell states
const int ALIVE = 1;
const int DEAD = 0;

vec2 input2DOffset(int texIndex, int xOffset, int yOffset) 
{
	/* 
	This function calculates texture coordinate offset from 
	pixel coordinate offset. 

	Parameters
	---------
		texIndex : int
			Input texture index
		xOffset : int
			X-offset in pixel coordinates
		yOffset : int
			Y-offset in pixel coordinates

	Returns
	----------
		vec2
			XY-offset in texture coordinates
	*/
	return vec2(
		float(xOffset) * uTD2DInfos[texIndex].res.s,
		float(yOffset) * uTD2DInfos[texIndex].res.t
	);
}

int getState(vec2 uv) 
{
	/* 
	Gets the state of a cell at a specific UV-coordinate. 

	Parameters
	---------
		uv : vec2
			UV-coordinate of cell

	Returns
	----------
		int
			State of cell at UV-coordinate
	*/
	return int(texture(sTD2DInputs[0], uv).x);
}

int computeAllFieldSum(vec2 uv) 
{
	/* 
	Computes the all-field sum around the cell at `uv`.

	Parameters
	---------
		uv : vec2
			UV-coordinate of center cell

	Returns
	----------
		int
			Number of living cells around, and including, the cell at `uv`.
	*/
	int sum = 0;
	for (int i = -1; i <= 1; i++) {
		for (int j = -1; j <= 1; j ++) {
			vec2 neighborUV = uv + input2DOffset(0, i, j);
			sum += getState(neighborUV);
		}
	}
	return sum;
}

int computeNextState(int currentState, int allFieldSum)
{
	/* 
	Computes the state of a cell in the next generation.

	Parameters
	---------
		currentState : int
		allFieldSum : int

	Returns
	----------
		int
			State of the cell in the next generation.
	*/
	// If the all-field sum is 3 the cell will always be alive in the
	// next generation.
	if (allFieldSum == 3) {
		return ALIVE; 
	}
	else if (allFieldSum == 4) {
		// If the all-field sum is 4 the cell will always retain its current
		// state in the next generation. 
		return currentState; 
	}
	else {
		// Any other all-field sum means the cell will be dead in the next
		// generation. 
		return DEAD; 
	}
}

void main()
{
	int currentState = getState(vUV.st);
	int allFieldSum = computeAllFieldSum(vUV.st);
	int nextState = computeNextState(currentState, allFieldSum);
	fragColor = vec4(nextState);
}
	