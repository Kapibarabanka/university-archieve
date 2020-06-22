#pragma once

class Allocator
{

public:
	Allocator(size_t pageCount);
	~Allocator(void);
	void* mem_alloc(size_t size);
	void mem_free(void* ptr);
	void* mem_realloc(void* ptr, size_t size);
	void mem_dump();
	size_t getPageSize();
	size_t getPageCount();

private:
	static const size_t pageSize = 4096;
	void* memory;
	size_t pageCount;

};
