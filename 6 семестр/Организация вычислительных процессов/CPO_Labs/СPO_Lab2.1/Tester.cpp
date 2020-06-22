#include "StdAfx.h"
#include "Tester.h"
#include <iostream>
#include <stdlib.h>
#include <time.h>

using namespace std;

Tester::Tester(Allocator* allocator)
{
	this->allocator = allocator;
	srand((unsigned) time(NULL));
}

Tester::~Tester(void) {}

void Tester::test(size_t iterCount, void** ptrs, size_t* ptrsCount)
{
	for (size_t i = 0; i < iterCount; i++)
	{
		cout << "*******************************************************\n";
		cout << (i + 1);
		cout << " iteration\n";
		int a;
		if (*ptrsCount == 0)
		{
			a = 0;
		}
		else
		{
			a = (int) rand() * 3 / RAND_MAX;
			if (a == 3)
			{
				a--;
			}
		}
		switch (a)
		{
			case 0:
			{	
				size_t sizeClass = (size_t)( rand() * 4 / RAND_MAX);
				if (sizeClass == 4)
				{
					sizeClass--;
				}
				size_t s;
				srand((unsigned) time(NULL));
				switch (sizeClass)
				{
					case 0:
					{
						s = (size_t)( rand() * (allocator->getPageSize() / 32) / RAND_MAX);
						break;
					}
					case 1:
					{
						s = (size_t)( rand() * (allocator->getPageSize() / 2) / RAND_MAX);
						break;
					}
					case 2:
					{
						s = (size_t)( rand() * (4 * allocator->getPageSize()) / RAND_MAX);
						break;
					}
					case 3:
					{
						s = (size_t)( rand() * (allocator->getPageSize() * allocator->getPageCount()) / RAND_MAX);
						break;
					}
				}
				if (s == 0)
				{
					s++;
				}
				cout << "mem_alloc(";
				cout << s;
				cout << ")\n";
				void* ptr = allocator->mem_alloc(s);
				if (ptr != NULL)
				{
					ptrs[*ptrsCount] = ptr;
					*ptrsCount = *ptrsCount + 1;
				}
				cout << "ptr = ";
				cout << ptr;
				cout << "\n";
				break;
			}
			case 1:
			{	
				size_t e = (size_t) (rand() * (*ptrsCount) / RAND_MAX);
				cout << "mem_free(";
				cout << ptrs[e];
				cout << ")\n";
				allocator->mem_free(ptrs[e]);
				for (size_t i = e + 1; i < *ptrsCount; i++)
				{
					ptrs[i - 1] = ptrs[i];
				}
				*ptrsCount = *ptrsCount - 1;
				break;
			}
			case 2:
			{	
				size_t sizeClass = (size_t)( rand() * 4 / RAND_MAX);
				if (sizeClass == 4)
				{
					sizeClass--;
				}
				size_t s;
				srand((unsigned) time(NULL));
				switch (sizeClass)
				{
					case 0:
					{
						s = (size_t)( rand() * (allocator->getPageSize() / 32) / RAND_MAX);
						break;
					}
					case 1:
					{
						s = (size_t)( rand() * (allocator->getPageSize() / 2) / RAND_MAX);
						break;
					}
					case 2:
					{
						s = (size_t)( rand() * (4 * allocator->getPageSize()) / RAND_MAX);
						break;
					}
					case 3:
					{
						s = (size_t)( rand() * (allocator->getPageSize() * allocator->getPageCount()) / RAND_MAX);
						break;
					}
				}
				srand((unsigned) time(NULL));
				size_t e = (size_t) (rand() * (*ptrsCount) / RAND_MAX);
				cout << "mem_realloc(";
				cout << ptrs[e];
				cout << ", ";
				cout << s;
				cout << ")\n";
				void* ptr = allocator->mem_realloc(ptrs[e], s);
				if (ptr != NULL)
				{
					ptrs[e] = ptr;
				}
				cout << "ptr = ";
				cout << ptr;
				cout << "\n";
				break;
			}
		}
		allocator->mem_dump();
		cout << "*******************************************************\n";
	}
}