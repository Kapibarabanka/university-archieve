class VirtualPage {
    var present: Boolean = false
    // Physical page number
    var ppn: Int = -1
    var R: Boolean = false
    var M: Boolean = false
    val state: Int
        get() = R.int * 2 + M.int
}