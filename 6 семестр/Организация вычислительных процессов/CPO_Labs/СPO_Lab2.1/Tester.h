#pragma once

#include "Allocator.h"

class Tester
{

public:
	Tester(Allocator* allocator);
	~Tester(void);
	void test(size_t iterCount, void** ptrs, size_t* ptrsCount);

private:
	Allocator* allocator;

};
