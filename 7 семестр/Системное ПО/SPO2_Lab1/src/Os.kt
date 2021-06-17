import kotlin.math.roundToInt

class Os {
    private val processes = List(PROCESSES) {createProcess(it)}
    private val physicalPages = List(PHYS_PAGES){PhysicalPage()}
    private val swap = mutableListOf<String>()
    private var allocatedPages: Int = 0
    private var clock: Int = 1
    private var pageFaults: Int = 0
    private var pageSuccesses: Int = 0

    fun go() {
        println("==== OS CONFIGURATION ====")
        println("$PHYS_PAGES physical pages")
        println("$PROCESSES processes:")
        for (process in processes)
        {
            println("\t* p${process.id} with ${process.vm.pages.count()} virtual pages")
        }
        println()
        println("===== SIMULATION LOG =====")
        for (i in 1..TOTAL_TIME) {
            val currentProcess = processes[i % PROCESSES]

            val demandedPage = currentProcess.demandPage()

            val accessed = tryAccess(currentProcess.id, demandedPage, (0..1).random().bool)
            if (accessed == null) println ("UNEXPECTED ERROR")

            clock++
            if (clock % CLEAR_TIME == 0) clearR()
        }
        println()
        println("======= STATISTICS =======")
        println("Page faults: $pageFaults")
        println("Page fault ratio: ${(pageFaults/TOTAL_TIME.toDouble()*100).roundToInt()}%")
}

    private fun tryAccess(pid: Int, pageIdx:Int, write: Boolean): Int? {
        val procIdx = processes.indexOfFirst { p -> p.id == pid }

        // Check if the demanded page is present
        val direct = tryTranslate(procIdx,pageIdx, write)

        if (direct != null) return direct

        // Check if there're any free physical pages
        val allocated = tryAllocate(procIdx, pageIdx, write)

        if (allocated != null) return allocated

        // Find page by the NRU algorithm
        return tryReplace(procIdx, pageIdx, write)
    }

    private fun tryTranslate(procIdx: Int, pageIdx:Int, write: Boolean): Int?{
        val process = processes[procIdx]
        val pid = process.id
        val page = process.vm.pages[pageIdx]
        return if (!page.present) {
            println("$clock. Page miss for p$pid: $pageIdx -> ???")
            pageFaults++
            null
        } else {
            println("$clock.Page hit for p$pid: $pageIdx -> ${page.ppn}")
            pageSuccesses++
            page.R = true
            if (write) {
                page.M = true
            }
            page.ppn
        }
    }

    private fun tryAllocate(procIdx: Int, pageIdx:Int, write: Boolean): Int? {
        return if (allocatedPages < PHYS_PAGES) {
            val process = processes[procIdx]
            val pid = process.id
            mapPage(procIdx, pageIdx, write, allocatedPages)
            println("\tAllocated page for p$pid: $pageIdx -> $allocatedPages")
            allocatedPages++
        } else null
    }

    private fun tryReplace(procIdx: Int, pageIdx:Int, write: Boolean): Int? {
        val process = processes[procIdx]
        val pid = process.id
        for (i in 0 until 4) {
            val oldPageIdx = process.vm.getPageOfClass(i)?: continue
            val oldPage = process.vm.pages[oldPageIdx]

            val ppn = oldPage.ppn

            // Move the data of the less used page to the swap
            swap.add(physicalPages[ppn].data)

            oldPage.present = false
            oldPage.ppn = -1
            println("\tEvicted page $ppn of class $i, owned by p$pid page $oldPageIdx")

            mapPage(procIdx, pageIdx, write, ppn)
            println("\t\tMapped page for p$pid: $pageIdx -> $ppn")

            return ppn
        }

        return null
    }

    private fun mapPage(procIdx: Int, pageIdx:Int, write: Boolean, dst:Int) {
        val page = processes[procIdx].vm.pages[pageIdx]

        page.present = true
        page.ppn = dst
        page.R = true
        if (write) {
            page.M = true
        }
    }

    private fun clearR() {
        for (process in processes) {
            process.vm.clearR()
        }
        println("CLEARED BIT R")
    }

    private fun createProcess(id: Int): Process {return Process(id, (PHYS_PAGES - 2..PHYS_PAGES + 2).random())}
}