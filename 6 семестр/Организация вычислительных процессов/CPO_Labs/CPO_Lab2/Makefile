all: Allocator

Allocator: Allocator_test.o Allocator.o
	g++ Allocator_test.o Allocator.o -o Allocator

Allocator_test.o: Allocator_test.cpp
	g++ -c Allocator_test.cpp

Allocator.o: Allocator.cpp
	g++ -c Allocator.cpp

clean:
	rm -rf *.o *.exe Allocator