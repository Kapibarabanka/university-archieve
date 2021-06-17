class VirtualMemory(pagesCount: Int) {
    val pages = List(pagesCount) {VirtualPage()}

    fun clearR() {
        for (page in pages) {
            page.R = false
        }
    }

    fun getPageOfClass(n: Int): Int? {
        val pagesOfClass = mutableListOf<Int>()
        for (i in 0 until pages.count()) {
            val page = pages[i]
            if ( page.present && page.state == n ) pagesOfClass.add(i)
        }
        return if (pagesOfClass.isEmpty()) null else pagesOfClass.random()
    }
}