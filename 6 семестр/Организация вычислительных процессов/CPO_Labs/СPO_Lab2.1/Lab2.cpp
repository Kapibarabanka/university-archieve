#include "stdafx.h"
#include "Allocator.h"
#include "Tester.h"
#include <iostream>
#include <stdlib.h>

using namespace std;

int _tmain(int argc, _TCHAR* argv[])
{
	const size_t pageCount = 128;
	Allocator allocator(pageCount);
	Tester tester(&allocator);
	void* ptrs[1000];
	size_t ptrsCount = 0;
	int a = -1;
	while (a != 0)
	{
		allocator.mem_dump();
		cout << "Choose the action:\n";
		cout << "1 - Test allocator\n";
		cout << "2 - Allocate memory\n";
		if (ptrsCount != 0)
		{
			cout << "3 - Free memory\n";
			cout << "4 - Reallocate memory\n";
		}
		cout << "0 - Exit\n";
		cout << "> ";
		cin >> a;
		switch (a)
		{
			case 1:
			{
				size_t iterCount;
				cout << "Enter the number of iterations.\n";
				cout << "> ";
				cin >> iterCount;
				tester.test(iterCount, ptrs, &ptrsCount);
				break;
			}
			case 2:
			{
				size_t size;
				cout << "Enter the size of memory to allocate.\n";
				cout << "> ";
				cin >> size;
				void* ptr = allocator.mem_alloc(size);
				if (ptr != NULL)
				{
					ptrs[ptrsCount++] = ptr;
				}
				cout << "ptr = ";
				cout << ptr;
				cout << "\n";
				break;
			}
			case 3:
			{	
				cout << "Choose block of memory to free:\n";
				for (size_t i = 0; i < ptrsCount; i++)
				{
					cout << i;
					cout << " - ";
					cout << ptrs[i];
					cout << "\n";
				}
				cout << "> ";
				size_t n;
				cin >> n;
				if (n < ptrsCount)
				{
					allocator.mem_free(ptrs[n]);
					for (size_t i = n + 1; i < ptrsCount; i++)
					{
						ptrs[i - 1] = ptrs[i];
					}
					ptrsCount--;
				}
				break;
			}
			case 4:
			{
				cout << "Choose block of memory to reallocate:\n";
				for (size_t i = 0; i < ptrsCount; i++)
				{
					cout << i;
					cout << " - ";
					cout << ptrs[i];
					cout << "\n";
				}
				cout << "> ";
				size_t n;
				cin >> n;
				if (n < ptrsCount)
				{
					size_t size;
					cout << "Enter the size of memory to reallocate.\n";
					cout << "> ";
					cin >> size;
					void* ptr = allocator.mem_realloc(ptrs[n], size);
					if (ptr != NULL)
					{
						ptrs[n] = ptr;
					}
					cout << "ptr = ";
					cout << ptr;
					cout << "\n";
				}
				break;
			}
		}
		cin.get();
	}
	return 0;
}
