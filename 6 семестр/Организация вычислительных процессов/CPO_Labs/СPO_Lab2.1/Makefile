all: Allocator

Allocator: Lab2.o Allocator.o Tester.o
	g++ Lab2.o Allocator.o -o Allocator Tester.o -o Tester

Lab2.o: Lab2.cpp
	g++ -c Lab2.cpp

Allocator.o: Allocator.cpp
	g++ -c Allocator.cpp

Tester.o: Tester.cpp
	g++ -c Tester.cpp

clean:
	rm -rf *.o *.exe Allocator