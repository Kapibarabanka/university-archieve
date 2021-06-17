class PhysicalPage {
    var count: Int = 0
    val data: String
        get() = "Data #${count++}"
}