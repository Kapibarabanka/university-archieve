#include "StdAfx.h"
#include "Allocator.h"
#include <iostream>
#include <stdlib.h>

using namespace std;

struct memoryHeader
{
	void* page16;
	size_t page16Count;
	void* page32;
	size_t page32Count;
	void* page64;
	size_t page64Count;
	void* page128;
	size_t page128Count;
	void* page256;
	size_t page256Count;
	void* page512;
	size_t page512Count;
	void* page1024;
	size_t page1024Count;
	void* page2048;
	size_t page2048Count;
	void* pageFull;
	size_t pageFullCount;
};

struct pageHeader
{
	char status;
	size_t blockSize;
	size_t freeBlocksCount;
	void* freeBlock;
	void* nextPage;
};

Allocator::Allocator(size_t pageCount)
{
	this->pageCount = pageCount;
	if (this->pageCount < 9)
	{
		this->pageCount = 9;
	}
	size_t memorySize = (pageSize + sizeof(pageHeader)) * this->pageCount + sizeof(memoryHeader);
	memory = new char[memorySize];
	struct memoryHeader* mHeader = (memoryHeader*) memory;
	mHeader->page16 = NULL;
	mHeader->page16Count = NULL;
	mHeader->page32 = NULL;
	mHeader->page32Count = NULL;
	mHeader->page64 = NULL;
	mHeader->page64Count = NULL;
	mHeader->page128 = NULL;
	mHeader->page128Count = NULL;
	mHeader->page256 = NULL;
	mHeader->page256Count = NULL;
	mHeader->page512 = NULL;
	mHeader->page512Count = NULL;
	mHeader->page1024 = NULL;
	mHeader->page1024Count = NULL;
	mHeader->page2048 = NULL;
	mHeader->page2048Count = NULL;
	mHeader->pageFull = (void*) ((size_t) memory + sizeof(memoryHeader));
	mHeader->pageFullCount = this->pageCount;
	struct pageHeader* pHeader = (pageHeader*) (mHeader->pageFull);
	for (size_t i = 0; i < this->pageCount; i++)
	{
		pHeader->status = 0;
		pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
		pHeader->freeBlocksCount = 1;
		pHeader->blockSize = pageSize;
		if (i < (this->pageCount - 1))
		{
			pHeader->nextPage = (void*) ((size_t) pHeader + sizeof(pageHeader) + pageSize);
		}
		else
		{
			pHeader->nextPage = NULL;
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
}

Allocator::~Allocator(void)
{
	delete[] memory;
}

void* Allocator::mem_alloc(size_t size)
{
	struct memoryHeader* mHeader = (memoryHeader*) memory;
	struct pageHeader* pHeader = NULL;
	if (size <= (pageSize / 2))
	{
		if (size > (pageSize / 4))
		{
			if (mHeader->page2048 != NULL)
			{
				pHeader = (pageHeader*) mHeader->page2048;
				while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
				{
					pHeader = (pageHeader*) pHeader->nextPage;
				}
				if (pHeader->freeBlock != NULL)
				{
					size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
					pHeader->freeBlock = (void*) *nextBlockPtr;
					pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
					return (void*) nextBlockPtr;
				}
				else
				{
					if (mHeader->pageFull == NULL)
					{
						return mem_alloc(4096);
					}
					else
					{
						pHeader = (pageHeader*) mHeader->pageFull;
						pHeader->status = 1;
						mHeader->pageFull = pHeader->nextPage;
						pHeader->nextPage = mHeader->page2048;
						pHeader->blockSize = 2048;
						pHeader->freeBlocksCount = pageSize / 2048;
						size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
						size_t nextBlock = NULL;
						while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
						{
							*blockPtr = nextBlock;
							nextBlock = (size_t) blockPtr;
							blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
						}
						pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
						mHeader->pageFullCount = mHeader->pageFullCount - 1;
						mHeader->page2048 = (void*) pHeader;
						mHeader->page2048Count = mHeader->page2048Count + 1;
						return mem_alloc(size);
					}
				}
			}
			else
			{
				if (mHeader->pageFullCount == 0)
				{
					return NULL;
				}
				pHeader = (pageHeader*) mHeader->pageFull;
				pHeader->status = 1;
				mHeader->pageFull = pHeader->nextPage;
				pHeader->nextPage = mHeader->page2048;
				pHeader->blockSize = 2048;
				pHeader->freeBlocksCount = pageSize / 2048;
				size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
				size_t nextBlock = NULL;
				while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
				{
					*blockPtr = nextBlock;
					nextBlock = (size_t) blockPtr;
					blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
				}
				pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
				mHeader->pageFullCount = mHeader->pageFullCount - 1;
				mHeader->page2048 = (void*) pHeader;
				mHeader->page2048Count = mHeader->page2048Count + 1;
				return mem_alloc(size);
			}
		}
		else
		{
			if (size > (pageSize / 8))
			{
				if (mHeader->page1024 != NULL)
				{
					pHeader = (pageHeader*) mHeader->page1024;
					while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
					{
						pHeader = (pageHeader*) pHeader->nextPage;
					}
					if (pHeader->freeBlock != NULL)
					{
						size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
						pHeader->freeBlock = (void*) *nextBlockPtr;
						pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
						return (void*) nextBlockPtr;
					}
					else
					{
						if (mHeader->pageFull == NULL)
						{
							return mem_alloc(2048);
						}
						else
						{
							pHeader = (pageHeader*) mHeader->pageFull;
							pHeader->status = 1;
							mHeader->pageFull = pHeader->nextPage;
							pHeader->nextPage = mHeader->page1024;
							pHeader->blockSize = 1024;
							pHeader->freeBlocksCount = pageSize / 1024;
							size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
							size_t nextBlock = NULL;
							while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
							{
								*blockPtr = nextBlock;
								nextBlock = (size_t) blockPtr;
								blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
							}
							pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
							mHeader->pageFullCount = mHeader->pageFullCount - 1;
							mHeader->page1024 = (void*) pHeader;
							mHeader->page1024Count = mHeader->page1024Count + 1;
							return mem_alloc(size);
						}
					}
				}
				else
				{
					pHeader = (pageHeader*) mHeader->pageFull;
					pHeader->status = 1;
					mHeader->pageFull = pHeader->nextPage;
					pHeader->nextPage = mHeader->page1024;
					pHeader->blockSize = 1024;
					pHeader->freeBlocksCount = pageSize / 1024;
					size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
					size_t nextBlock = NULL;
					while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
					{
						*blockPtr = nextBlock;
						nextBlock = (size_t) blockPtr;
						blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
					}
					pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
					mHeader->pageFullCount = mHeader->pageFullCount - 1;
					mHeader->page1024 = (void*) pHeader;
					mHeader->page1024Count = mHeader->page1024Count + 1;
					return mem_alloc(size);
				}
			}
			else
			{
				if (size > (pageSize / 16))
				{
					if (mHeader->page512 != NULL)
					{
						pHeader = (pageHeader*) mHeader->page512;
						while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
						{
							pHeader = (pageHeader*) pHeader->nextPage;
						}
						if (pHeader->freeBlock != NULL)
						{
							size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
							pHeader->freeBlock = (void*) *nextBlockPtr;
							pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
							return (void*) nextBlockPtr;
						}
						else
						{
							if (mHeader->pageFull == NULL)
							{
								return mem_alloc(1024);
							}
							else
							{
								pHeader = (pageHeader*) mHeader->pageFull;
								pHeader->status = 1;
								mHeader->pageFull = pHeader->nextPage;
								pHeader->nextPage = mHeader->page512;
								pHeader->blockSize = 512;
								pHeader->freeBlocksCount = pageSize / 512;
								size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
								size_t nextBlock = NULL;
								while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
								{
									*blockPtr = nextBlock;
									nextBlock = (size_t) blockPtr;
									blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
								}
								pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
								mHeader->pageFullCount = mHeader->pageFullCount - 1;
								mHeader->page512 = (void*) pHeader;
								mHeader->page512Count = mHeader->page512Count + 1;
								return mem_alloc(size);
							}
						}
					}
					else
					{
						pHeader = (pageHeader*) mHeader->pageFull;
						pHeader->status = 1;
						mHeader->pageFull = pHeader->nextPage;
						pHeader->nextPage = mHeader->page512;
						pHeader->blockSize = 512;
						pHeader->freeBlocksCount = pageSize / 512;
						size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
						size_t nextBlock = NULL;
						while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
						{
							*blockPtr = nextBlock;
							nextBlock = (size_t) blockPtr;
							blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
						}
						pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
						mHeader->pageFullCount = mHeader->pageFullCount - 1;
						mHeader->page512 = (void*) pHeader;
						mHeader->page512Count = mHeader->page512Count + 1;
						return mem_alloc(size);
					}
				}
				else
				{
					if (size > (pageSize / 32))
					{
						if (mHeader->page256 != NULL)
						{
							pHeader = (pageHeader*) mHeader->page256;
							while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
							{
								pHeader = (pageHeader*) pHeader->nextPage;
							}
							if (pHeader->freeBlock != NULL)
							{
								size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
								pHeader->freeBlock = (void*) *nextBlockPtr;
								pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
								return (void*) nextBlockPtr;
							}
							else
							{
								if (mHeader->pageFull == NULL)
								{
									return mem_alloc(512);
								}
								else
								{
									pHeader = (pageHeader*) mHeader->pageFull;
									pHeader->status = 1;
									mHeader->pageFull = pHeader->nextPage;
									pHeader->nextPage = mHeader->page256;
									pHeader->blockSize = 256;
									pHeader->freeBlocksCount = pageSize / 256;
									size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
									size_t nextBlock = NULL;
									while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
									{
										*blockPtr = nextBlock;
										nextBlock = (size_t) blockPtr;
										blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
									}
									pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
									mHeader->pageFullCount = mHeader->pageFullCount - 1;
									mHeader->page256 = (void*) pHeader;
									mHeader->page256Count = mHeader->page256Count + 1;
									return mem_alloc(size);
								}
							}
						}
						else
						{
							pHeader = (pageHeader*) mHeader->pageFull;
							pHeader->status = 1;
							mHeader->pageFull = pHeader->nextPage;
							pHeader->nextPage = mHeader->page256;
							pHeader->blockSize = 256;
							pHeader->freeBlocksCount = pageSize / 256;
							size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
							size_t nextBlock = NULL;
							while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
							{
								*blockPtr = nextBlock;
								nextBlock = (size_t) blockPtr;
								blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
							}
							pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
							mHeader->pageFullCount = mHeader->pageFullCount - 1;
							mHeader->page256 = (void*) pHeader;
							mHeader->page256Count = mHeader->page256Count + 1;
							return mem_alloc(size);
						}
					}
					else
					{
						if (size > (pageSize / 64))
						{
							if (mHeader->page128 != NULL)
							{
								pHeader = (pageHeader*) mHeader->page128;
								while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
								{
									pHeader = (pageHeader*) pHeader->nextPage;
								}
								if (pHeader->freeBlock != NULL)
								{
									size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
									pHeader->freeBlock = (void*) *nextBlockPtr;
									pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
									return (void*) nextBlockPtr;
								}
								else
								{
									if (mHeader->pageFull == NULL)
									{
										return mem_alloc(256);
									}
									else
									{
										pHeader = (pageHeader*) mHeader->pageFull;
										pHeader->status = 1;
										mHeader->pageFull = pHeader->nextPage;
										pHeader->nextPage = mHeader->page128;
										pHeader->blockSize = 128;
										pHeader->freeBlocksCount = pageSize / 128;
										size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
										size_t nextBlock = NULL;
										while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
										{
											*blockPtr = nextBlock;
											nextBlock = (size_t) blockPtr;
											blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
										}
										pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
										mHeader->pageFullCount = mHeader->pageFullCount - 1;
										mHeader->page128 = (void*) pHeader;
										mHeader->page128Count = mHeader->page128Count + 1;
										return mem_alloc(size);
									}
								}
							}
							else
							{
								pHeader = (pageHeader*) mHeader->pageFull;
								pHeader->status = 1;
								mHeader->pageFull = pHeader->nextPage;
								pHeader->nextPage = mHeader->page128;
								pHeader->blockSize = 128;
								pHeader->freeBlocksCount = pageSize / 128;
								size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
								size_t nextBlock = NULL;
								while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
								{
									*blockPtr = nextBlock;
									nextBlock = (size_t) blockPtr;
									blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
								}	
								pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
								mHeader->pageFullCount = mHeader->pageFullCount - 1;
								mHeader->page128 = (void*) pHeader;
								mHeader->page128Count = mHeader->page128Count + 1;
								return mem_alloc(size);
							}
						}
						else
						{
							if (size > (pageSize / 128))
							{
								if (mHeader->page64 != NULL)
								{
									pHeader = (pageHeader*) mHeader->page64;
									while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
									{
										pHeader = (pageHeader*) pHeader->nextPage;
									}
									if (pHeader->freeBlock != NULL)
									{
										size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
										pHeader->freeBlock = (void*) *nextBlockPtr;
										pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
										return (void*) nextBlockPtr;
									}
									else
									{
										if (mHeader->pageFull == NULL)
										{
											return mem_alloc(128);
										}
										else
										{
											pHeader = (pageHeader*) mHeader->pageFull;
											pHeader->status = 1;
											mHeader->pageFull = pHeader->nextPage;
											pHeader->nextPage = mHeader->page64;
											pHeader->blockSize = 64;
											pHeader->freeBlocksCount = pageSize / 64;
											size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
											size_t nextBlock = NULL;
											while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
											{
												*blockPtr = nextBlock;
												nextBlock = (size_t) blockPtr;
												blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
											}
											pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
											mHeader->pageFullCount = mHeader->pageFullCount - 1;
											mHeader->page64 = (void*) pHeader;
											mHeader->page64Count = mHeader->page64Count + 1;
											return mem_alloc(size);
										}
									}
								}
								else
								{
									pHeader = (pageHeader*) mHeader->pageFull;
									pHeader->status = 1;
									mHeader->pageFull = pHeader->nextPage;
									pHeader->nextPage = mHeader->page64;
									pHeader->blockSize = 64;
									pHeader->freeBlocksCount = pageSize / 64;
									size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
									size_t nextBlock = NULL;
									while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
									{
										*blockPtr = nextBlock;
										nextBlock = (size_t) blockPtr;
										blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
									}	
									pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
									mHeader->pageFullCount = mHeader->pageFullCount - 1;
									mHeader->page64 = (void*) pHeader;
									mHeader->page64Count = mHeader->page64Count + 1;
									return mem_alloc(size);
								}
							}
							else
							{
								if (size > (pageSize / 256))
								{
									if (mHeader->page32 != NULL)
									{
										pHeader = (pageHeader*) mHeader->page32;
										while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
										{
											pHeader = (pageHeader*) pHeader->nextPage;
										}
										if (pHeader->freeBlock != NULL)
										{
											size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
											pHeader->freeBlock = (void*) *nextBlockPtr;
											pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
											return (void*) nextBlockPtr;
										}
										else
										{
											if (mHeader->pageFull == NULL)
											{
												return mem_alloc(64);
											}
											else
											{
												pHeader = (pageHeader*) mHeader->pageFull;
												pHeader->status = 1;
												mHeader->pageFull = pHeader->nextPage;
												pHeader->nextPage = mHeader->page32;
												pHeader->blockSize = 32;
												pHeader->freeBlocksCount = pageSize / 32;
												size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
												size_t nextBlock = NULL;
												while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
												{
													*blockPtr = nextBlock;
													nextBlock = (size_t) blockPtr;
													blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
												}
												pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
												mHeader->pageFullCount = mHeader->pageFullCount - 1;
												mHeader->page32 = (void*) pHeader;
												mHeader->page32Count = mHeader->page32Count + 1;
												return mem_alloc(size);
											}
										}
									}
									else
									{
										pHeader = (pageHeader*) mHeader->pageFull;
										pHeader->status = 1;
										mHeader->pageFull = pHeader->nextPage;
										pHeader->nextPage = mHeader->page32;
										pHeader->blockSize = 32;
										pHeader->freeBlocksCount = pageSize / 32;
										size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
										size_t nextBlock = NULL;
										while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
										{
											*blockPtr = nextBlock;
											nextBlock = (size_t) blockPtr;
											blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
										}	
										pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
										mHeader->pageFullCount = mHeader->pageFullCount - 1;
										mHeader->page32 = (void*) pHeader;
										mHeader->page32Count = mHeader->page32Count + 1;
										return mem_alloc(size);
									}
								}
								else
								{	
									if (mHeader->page16 != NULL)
									{
										pHeader = (pageHeader*) mHeader->page16;
										while ((pHeader->freeBlock == NULL) && (pHeader->nextPage != NULL))
										{
											pHeader = (pageHeader*) pHeader->nextPage;
										}
										if (pHeader->freeBlock != NULL)
										{
											size_t* nextBlockPtr = (size_t*) pHeader->freeBlock;
											pHeader->freeBlock = (void*) *nextBlockPtr;
											pHeader->freeBlocksCount = pHeader->freeBlocksCount - 1;
											return (void*) nextBlockPtr;
										}
										else
										{
											if (mHeader->pageFull == NULL)
											{
												return mem_alloc(32);
											}
											else
											{
												pHeader = (pageHeader*) mHeader->pageFull;
												pHeader->status = 1;
												mHeader->pageFull = pHeader->nextPage;
												pHeader->nextPage = mHeader->page16;
												pHeader->blockSize = 16;
												pHeader->freeBlocksCount = pageSize / 16;
												size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
												size_t nextBlock = NULL;
												while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
												{
													*blockPtr = nextBlock;
													nextBlock = (size_t) blockPtr;
													blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
												}
												pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
												mHeader->pageFullCount = mHeader->pageFullCount - 1;
												mHeader->page16 = (void*) pHeader;
												mHeader->page16Count = mHeader->page16Count + 1;
												return mem_alloc(size);
											}
										}
									}
									else
									{
										pHeader = (pageHeader*) mHeader->pageFull;
										pHeader->status = 1;
										mHeader->pageFull = pHeader->nextPage;
										pHeader->nextPage = mHeader->page16;
										pHeader->blockSize = 16;
										pHeader->freeBlocksCount = pageSize / 16;
										size_t* blockPtr = (size_t*) ((size_t) pHeader + sizeof(pageHeader) + pageSize - pHeader->blockSize);
										size_t nextBlock = NULL;
										while ((size_t) blockPtr >= ((size_t) pHeader + sizeof(pageHeader)))
										{
											*blockPtr = nextBlock;
											nextBlock = (size_t) blockPtr;
											blockPtr = (size_t*) ((size_t) blockPtr - pHeader->blockSize);
										}	
										pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
										mHeader->pageFullCount = mHeader->pageFullCount - 1;
										mHeader->page16 = (void*) pHeader;
										mHeader->page16Count = mHeader->page16Count + 1;
										return mem_alloc(size);
									}
								}
							}
						}
					}
				}
			}
		}
	}
	else
	{
		size_t neededPages = size / pageSize;
		if ((size % pageSize) != 0)
		{
			neededPages++;
		}
		if (mHeader->pageFullCount < neededPages)
		{
			return NULL;
		}
		else
		{
			pHeader = (pageHeader*) mHeader->pageFull;
			struct pageHeader* nextPageHeader = pHeader;
			for (size_t i = 0; i < neededPages; i++)
			{
				nextPageHeader->status = 2;
				nextPageHeader->freeBlock = NULL;
				nextPageHeader->freeBlocksCount = neededPages;
				nextPageHeader = (pageHeader*) nextPageHeader->nextPage;
			}
			mHeader->pageFull = (void*) nextPageHeader;
			mHeader->pageFullCount = mHeader->pageFullCount - neededPages;
			return (void*) ((size_t) pHeader + sizeof(pageHeader));
		}
	}
}

void Allocator::mem_free(void* ptr)
{
	if (ptr == NULL)
	{
		return;
	}
	struct memoryHeader* mHeader = (memoryHeader*) memory;
	struct pageHeader* pHeader = (pageHeader*) ((size_t) memory + sizeof(memoryHeader));
	while (((size_t) ptr < (size_t) pHeader) || ((size_t) ptr > ((size_t) pHeader + sizeof(pageHeader) + pageSize)))
	{
		pHeader = (pageHeader*) ((size_t) pHeader + sizeof(pageHeader) + pageSize);
	}
	if (pHeader->status == 2)
	{
		struct pageHeader* pagePtr = pHeader;
		size_t pagePtrCount = pHeader->freeBlocksCount;
		for (size_t i = 0; i < pagePtrCount; i++)
		{
			pagePtr->status = 0;
			pagePtr->freeBlocksCount = 1;
			pagePtr->freeBlock = (void*) ((size_t) pagePtr + sizeof(pageHeader));
			if (i < (pagePtrCount - 1))
			{
				pagePtr = (pageHeader*) pagePtr->nextPage;
			}
		}
		pagePtr->nextPage = mHeader->pageFull;
		mHeader->pageFull = (void*) pHeader;
		mHeader->pageFullCount = mHeader->pageFullCount + pagePtrCount;
	}
	else
	{
		if (pHeader->status == 1)
		{
			size_t* nextBlockPtr = (size_t*) ptr;
			*nextBlockPtr = (size_t) pHeader->freeBlock;
			pHeader->freeBlock = ptr;
			pHeader->freeBlocksCount = pHeader->freeBlocksCount + 1;
			if (pHeader->freeBlocksCount == (pageSize / pHeader->blockSize))
			{
				if (pHeader->blockSize == 2048)
				{
					struct pageHeader* pagePtr = (pageHeader*) mHeader->page2048;
					if ((size_t) pHeader == (size_t) pagePtr)
					{
						mHeader->page2048 = pHeader->nextPage;
						mHeader->page2048Count = mHeader->page2048Count - 1;
						pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
						pHeader->status = 0;
						pHeader->blockSize = pageSize;
						pHeader->freeBlocksCount = 1;
						pHeader->nextPage = mHeader->pageFull;
						mHeader->pageFull = (void*) pHeader;
						mHeader->pageFullCount = mHeader->pageFullCount + 1;
					}
					else
					{
						while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
						{
							pagePtr = (pageHeader*) pHeader->nextPage;
						}
						pagePtr->nextPage = pHeader->nextPage;
						mHeader->page2048Count = mHeader->page2048Count - 1;
						pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
						pHeader->status = 0;
						pHeader->blockSize = pageSize;
						pHeader->freeBlocksCount = 1;
						pHeader->nextPage = mHeader->pageFull;
						mHeader->pageFull = (void*) pHeader;
						mHeader->pageFullCount = mHeader->pageFullCount + 1;
					}
				}
				else
				{
					if (pHeader->blockSize == 1024)
					{
						struct pageHeader* pagePtr = (pageHeader*) mHeader->page1024;
						if ((size_t) pHeader == (size_t) pagePtr)
						{
							mHeader->page1024 = pHeader->nextPage;
							mHeader->page1024Count = mHeader->page1024Count - 1;
							pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
							pHeader->status = 0;
							pHeader->blockSize = pageSize;
							pHeader->freeBlocksCount = 1;
							pHeader->nextPage = mHeader->pageFull;
							mHeader->pageFull = (void*) pHeader;
							mHeader->pageFullCount = mHeader->pageFullCount + 1;
						}
						else
						{
							while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
							{
								pagePtr = (pageHeader*) pHeader->nextPage;
							}
							pagePtr->nextPage = pHeader->nextPage;
							mHeader->page1024Count = mHeader->page1024Count - 1;
							pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
							pHeader->status = 0;
							pHeader->blockSize = pageSize;
							pHeader->freeBlocksCount = 1;
							pHeader->nextPage = mHeader->pageFull;
							mHeader->pageFull = (void*) pHeader;
							mHeader->pageFullCount = mHeader->pageFullCount + 1;
						}
					}
					else
					{
						if (pHeader->blockSize == 512)
						{
							struct pageHeader* pagePtr = (pageHeader*) mHeader->page512;
							if ((size_t) pHeader == (size_t) pagePtr)
							{
								mHeader->page512 = pHeader->nextPage;
								mHeader->page512Count = mHeader->page512Count - 1;
								pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
								pHeader->status = 0;
								pHeader->blockSize = pageSize;
								pHeader->freeBlocksCount = 1;
								pHeader->nextPage = mHeader->pageFull;
								mHeader->pageFull = (void*) pHeader;
								mHeader->pageFullCount = mHeader->pageFullCount + 1;
							}
							else
							{
								while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
								{
									pagePtr = (pageHeader*) pHeader->nextPage;
								}
								pagePtr->nextPage = pHeader->nextPage;
								mHeader->page512Count = mHeader->page512Count - 1;
								pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
								pHeader->status = 0;
								pHeader->blockSize = pageSize;
								pHeader->freeBlocksCount = 1;
								pHeader->nextPage = mHeader->pageFull;
								mHeader->pageFull = (void*) pHeader;
								mHeader->pageFullCount = mHeader->pageFullCount + 1;
							}
						}
						else
						{
							if (pHeader->blockSize == 256)
							{
								struct pageHeader* pagePtr = (pageHeader*) mHeader->page256;
								if ((size_t) pHeader == (size_t) pagePtr)
								{
									mHeader->page256 = pHeader->nextPage;
									mHeader->page256Count = mHeader->page256Count - 1;
									pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
									pHeader->status = 0;
									pHeader->blockSize = pageSize;
									pHeader->freeBlocksCount = 1;
									pHeader->nextPage = mHeader->pageFull;
									mHeader->pageFull = (void*) pHeader;
									mHeader->pageFullCount = mHeader->pageFullCount + 1;
								}
								else
								{
									while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
									{
										pagePtr = (pageHeader*) pHeader->nextPage;
									}
									pagePtr->nextPage = pHeader->nextPage;
									mHeader->page256Count = mHeader->page256Count - 1;
									pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
									pHeader->status = 0;
									pHeader->blockSize = pageSize;
									pHeader->freeBlocksCount = 1;
									pHeader->nextPage = mHeader->pageFull;
									mHeader->pageFull = (void*) pHeader;
									mHeader->pageFullCount = mHeader->pageFullCount + 1;
								}
							}
							else
							{
								if (pHeader->blockSize == 128)
								{
									struct pageHeader* pagePtr = (pageHeader*) mHeader->page128;
									if ((size_t) pHeader == (size_t) pagePtr)
									{
										mHeader->page128 = pHeader->nextPage;
										mHeader->page128Count = mHeader->page128Count - 1;
										pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
										pHeader->status = 0;
										pHeader->blockSize = pageSize;
										pHeader->freeBlocksCount = 1;
										pHeader->nextPage = mHeader->pageFull;
										mHeader->pageFull = (void*) pHeader;
										mHeader->pageFullCount = mHeader->pageFullCount + 1;
									}
									else
									{
										while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
										{
											pagePtr = (pageHeader*) pHeader->nextPage;
										}
										pagePtr->nextPage = pHeader->nextPage;
										mHeader->page128Count = mHeader->page128Count - 1;
										pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
										pHeader->status = 0;
										pHeader->blockSize = pageSize;
										pHeader->freeBlocksCount = 1;
										pHeader->nextPage = mHeader->pageFull;
										mHeader->pageFull = (void*) pHeader;
										mHeader->pageFullCount = mHeader->pageFullCount + 1;
									}
								}
								else
								{
									if (pHeader->blockSize == 64)
									{
										struct pageHeader* pagePtr = (pageHeader*) mHeader->page64;
										if ((size_t) pHeader == (size_t) pagePtr)
										{
											mHeader->page64 = pHeader->nextPage;
											mHeader->page64Count = mHeader->page64Count - 1;
											pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
											pHeader->status = 0;
											pHeader->blockSize = pageSize;
											pHeader->freeBlocksCount = 1;
											pHeader->nextPage = mHeader->pageFull;
											mHeader->pageFull = (void*) pHeader;
											mHeader->pageFullCount = mHeader->pageFullCount + 1;
										}
										else
										{
											while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
											{
												pagePtr = (pageHeader*) pHeader->nextPage;
											}
											pagePtr->nextPage = pHeader->nextPage;
											mHeader->page64Count = mHeader->page64Count - 1;
											pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
											pHeader->status = 0;
											pHeader->blockSize = pageSize;
											pHeader->freeBlocksCount = 1;
											pHeader->nextPage = mHeader->pageFull;
											mHeader->pageFull = (void*) pHeader;
											mHeader->pageFullCount = mHeader->pageFullCount + 1;
										}
									}
									else
									{
										if (pHeader->blockSize == 32)
										{
											struct pageHeader* pagePtr = (pageHeader*) mHeader->page32;
											if ((size_t) pHeader == (size_t) pagePtr)
											{
												mHeader->page32 = pHeader->nextPage;
												mHeader->page32Count = mHeader->page32Count - 1;
												pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
												pHeader->status = 0;
												pHeader->blockSize = pageSize;
												pHeader->freeBlocksCount = 1;
												pHeader->nextPage = mHeader->pageFull;
												mHeader->pageFull = (void*) pHeader;
												mHeader->pageFullCount = mHeader->pageFullCount + 1;
											}
											else
											{
												while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
												{
													pagePtr = (pageHeader*) pHeader->nextPage;
												}
												pagePtr->nextPage = pHeader->nextPage;
												mHeader->page32Count = mHeader->page32Count - 1;
												pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
												pHeader->status = 0;
												pHeader->blockSize = pageSize;
												pHeader->freeBlocksCount = 1;
												pHeader->nextPage = mHeader->pageFull;
												mHeader->pageFull = (void*) pHeader;
												mHeader->pageFullCount = mHeader->pageFullCount + 1;
											}
										}
										else
										{
											struct pageHeader* pagePtr = (pageHeader*) mHeader->page16;
											if ((size_t) pHeader == (size_t) pagePtr)
											{
												mHeader->page16 = pHeader->nextPage;
												mHeader->page16Count = mHeader->page16Count - 1;
												pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
												pHeader->status = 0;
												pHeader->blockSize = pageSize;
												pHeader->freeBlocksCount = 1;
												pHeader->nextPage = mHeader->pageFull;
												mHeader->pageFull = (void*) pHeader;
												mHeader->pageFullCount = mHeader->pageFullCount + 1;
											}
											else
											{
												while ((size_t) pHeader != (size_t) (pagePtr->nextPage))
												{
													pagePtr = (pageHeader*) pHeader->nextPage;
												}
												pagePtr->nextPage = pHeader->nextPage;
												mHeader->page16Count = mHeader->page16Count - 1;
												pHeader->freeBlock = (void*) ((size_t) pHeader + sizeof(pageHeader));
												pHeader->status = 0;
												pHeader->blockSize = pageSize;
												pHeader->freeBlocksCount = 1;
												pHeader->nextPage = mHeader->pageFull;
												mHeader->pageFull = (void*) pHeader;
												mHeader->pageFullCount = mHeader->pageFullCount + 1;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

void* Allocator::mem_realloc(void* ptr, size_t size)
{
	if (ptr == NULL)
	{
		return mem_alloc(size);
	}
	struct memoryHeader* mHeader = (memoryHeader*) memory;
	struct pageHeader* pHeader = (pageHeader*) ((size_t) memory + sizeof(memoryHeader));
	while (((size_t) ptr < (size_t) pHeader) || ((size_t) ptr > ((size_t) pHeader + sizeof(pageHeader) + pageSize)))
	{
		pHeader = (pageHeader*) ((size_t) pHeader + sizeof(pageHeader) + pageSize);
	}
	if (((pHeader->blockSize / 2) < size) && (pHeader->blockSize >= size))
	{
		return ptr;
	}
	void* resultPtr = mem_alloc(size);
	if (resultPtr == NULL)
	{
		return NULL;
	}
	char* ptr1 = (char*) ptr;
	char* ptr2 = (char*) resultPtr;
	if ((pHeader->status == 1) || ((pHeader->status == 2) && (pHeader->freeBlocksCount == 1)) || ((pHeader->status == 2) && (size <= pageSize)))
	{
		size_t copySize;
		if (size < pHeader->blockSize)
		{
			copySize = size;
		}
		else
		{
			copySize = pHeader->blockSize;
		}
		for (size_t i = 0; i < copySize; i++)
		{
			*ptr2 = *ptr1;
			ptr1++;
			ptr2++;
		}
	}
	else
	{
		struct pageHeader* copyPHeader = (pageHeader*) ((size_t) resultPtr - sizeof(pageHeader));
		size_t copyPagesCount;
		if (pHeader->freeBlocksCount < copyPHeader->freeBlocksCount)
		{
			copyPagesCount = pHeader->freeBlocksCount;
		}
		else
		{
			copyPagesCount = copyPHeader->freeBlocksCount;
		}
		for (size_t i = 0; i < copyPagesCount; i++)
		{
			for (size_t j = 0; j < pageSize; j++)
			{
				*ptr2 = *ptr1;
				ptr1++;
				ptr2++;
			}
			ptr1 = (char*) ((size_t) pHeader->nextPage + sizeof(pageHeader));
			ptr2 = (char*) ((size_t) copyPHeader->nextPage + sizeof(pageHeader));
		}
	}
	mem_free(ptr);
	return resultPtr;
}

void Allocator::mem_dump()
{
	struct memoryHeader* mHeader = (memoryHeader*) memory;
	struct pageHeader* pHeader;
	size_t totalMemory = pageCount * pageSize;
	size_t totalFreeMemory = 0;
	cout << "************************************************************************" << endl;
	cout << "Dump of memory:" << endl;
	cout << "The number of pages: " << pageCount << endl;
	cout << "The size of page: " << pageSize << endl;
	cout << "========================================================================" << endl;
	cout << "Free pages" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->pageFullCount << endl;
	pHeader = (pageHeader*) mHeader->pageFull;
	totalFreeMemory += mHeader->pageFullCount * pageSize;
	for (size_t i = 0; i < mHeader->pageFullCount; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 2048 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page2048Count << endl;
	pHeader = (pageHeader*) mHeader->page2048;
	for (size_t i = 0; i < mHeader->page2048Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 1024 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page1024Count << endl;
	pHeader = (pageHeader*) mHeader->page1024;
	for (size_t i = 0; i < mHeader->page1024Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 512 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page512Count << endl;
	pHeader = (pageHeader*) mHeader->page512;
	for (size_t i = 0; i < mHeader->page512Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 256 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page256Count << endl;
	pHeader = (pageHeader*) mHeader->page256;
	for (size_t i = 0; i < mHeader->page256Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 128 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page128Count << endl;
	pHeader = (pageHeader*) mHeader->page128;
	for (size_t i = 0; i < mHeader->page128Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 64 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page64Count << endl;
	pHeader = (pageHeader*) mHeader->page64;
	for (size_t i = 0; i < mHeader->page64Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 32 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page32Count << endl;
	pHeader = (pageHeader*) mHeader->page32;
	for (size_t i = 0; i < mHeader->page32Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Pages divided to blocks of 16 bytes" << endl;
	cout << "------------------------------------------------------------------------" << endl;
	cout << "The number of pages: " << mHeader->page16Count << endl;
	pHeader = (pageHeader*) mHeader->page16;
	for (size_t i = 0; i < mHeader->page16Count; i++)
	{
		cout << ">Page #" << i << ": " << pHeader << endl;
		cout << "The number of free blocks: " << pHeader->freeBlocksCount << endl;
		totalFreeMemory += pHeader->freeBlocksCount * pHeader->blockSize;
		void* freeBlock = pHeader->freeBlock;
		for (size_t j = 0; j < pHeader->freeBlocksCount; j++)
		{
			cout << "Block #" << j << ": " << freeBlock << endl;
			freeBlock = (void*) *((size_t*) freeBlock);
		}
		pHeader = (pageHeader*) pHeader->nextPage;
	}
	cout << "========================================================================" << endl;
	cout << "Total memory: " << totalMemory << endl;
	cout << "Total busy memory: " << (totalMemory - totalFreeMemory) << endl;
	cout << "Total free memory: " << totalFreeMemory << endl;
	cout << "************************************************************************" << endl;
}

size_t Allocator::getPageSize()
{
	return pageSize;
}

size_t Allocator::getPageCount()
{
	return pageCount;
}