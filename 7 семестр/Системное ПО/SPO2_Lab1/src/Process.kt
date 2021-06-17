class Process(val id: Int, pagesCount: Int) {
    val vm = VirtualMemory(pagesCount)

    fun demandPage(): Int {return (0 until vm.pages.count()).random()}
}